import numpy as np
import trimesh
import matplotlib.pyplot as plt
import os
import random

def start_point_generate(n, m):
    """Функция выбора точки начала лабиринта"""
    if random.choice([True, False]):
        if random.choice([True, False]):
            start = (0, random.randint(0, m - 1))
        else:
            start = (n - 1, random.randint(0, m - 1))
    else:
        if random.choice([True, False]):
            start = (random.randint(0, n - 1), 0)
        else:
            start = (random.randint(0, n - 1), m - 1)
    return start

def finish_point_generate(start, n, m):
    """Выбор точки конца лабиринта"""
    return n - 1 - start[0], m - 1 - start[1]

def transition_choice(x, y, rm):
    """Функция выбора дальнейшего пути в генерации лабиринта"""
    choice_list = []
    if x > 0:
        if not rm[x - 1][y]:
            choice_list.append((x - 1, y))
    if x < len(rm) - 1:
        if not rm[x + 1][y]:
            choice_list.append((x + 1, y))
    if y > 0:
        if not rm[x][y - 1]:
            choice_list.append((x, y - 1))
    if y < len(rm[0]) - 1:
        if not rm[x][y + 1]:
            choice_list.append((x, y + 1))
    if choice_list:
        nx, ny = random.choice(choice_list)
        if x == nx:
            if ny > y:
                tx, ty = x * 2, ny * 2 - 1
            else:
                tx, ty = x * 2, ny * 2 + 1
        else:
            if nx > x:
                tx, ty = nx * 2 - 1, y * 2
            else:
                tx, ty = nx * 2 + 1, y * 2
        return nx, ny, tx, ty
    else:
        return -1, -1, -1, -1

def create_labyrinth(n=5, m=5):
    """Генерация лабиринта"""
    reach_matrix = []
    for i in range(n):  # создаём матрицу достижимости ячеек
        reach_matrix.append([])
        for j in range(m):
            reach_matrix[i].append(False)
    transition_matrix = []
    for i in range(n * 2 - 1):  # заполнение матрицы переходов
        transition_matrix.append([])
        for j in range(m * 2 - 1):
            if i % 2 == 0 and j % 2 == 0:
                transition_matrix[i].append(True)
            else:
                transition_matrix[i].append(False)
    start = start_point_generate(n, m)
    finish = finish_point_generate(start, n, m)
    list_transition = [start]
    x, y = start
    reach_matrix[x][y] = True
    x, y, tx, ty = transition_choice(x, y, reach_matrix)
    for i in range(1, m * n):
        while not (x >= 0 and y >= 0):
            x, y = list_transition[-1]
            list_transition.pop()
            x, y, tx, ty = transition_choice(x, y, reach_matrix)
        reach_matrix[x][y] = True
        list_transition.append((x, y))
        transition_matrix[tx][ty] = True
        x, y, tx, ty = transition_choice(x, y, reach_matrix)
    return transition_matrix, start, finish  # возвращаем матрицу проходов и начальную точку

def generate_labyrinth(width, height, depth, labyrinth_matrix):
    # Добавляем стены по лабиринту
    cell_width = 10
    labyrinth_height = height - 10
    labyrinth_depth = depth - 10
    labyrinth_width = width - 10
    vertices = []
    faces = []
    for i in range(len(labyrinth_matrix)):
        for j in range(len(labyrinth_matrix[i])):
            if not labyrinth_matrix[i][j]:
                # Если это стена, то добавляем ее в список вершин и граней
                x = 5 + j * cell_width
                y = labyrinth_height
                z = 5 + i * cell_width
                vertices.extend([
                    [x, y, z],
                    [x + cell_width, y, z],
                    [x + cell_width, y, z + cell_width],
                    [x, y, z + cell_width],
                    [x, y - cell_width, z],
                    [x + cell_width, y - cell_width, z],
                    [x + cell_width, y - cell_width, z + cell_width],
                    [x, y - cell_width, z + cell_width]
                ])
                faces.extend([
                    [len(vertices) - 8, len(vertices) - 7, len(vertices) - 6],
                    [len(vertices) - 8, len(vertices) - 6, len(vertices) - 5],
                    [len(vertices) - 4, len(vertices) - 3, len(vertices) - 2],
                    [len(vertices) - 4, len(vertices) - 2, len(vertices) - 1],
                    [len(vertices) - 8, len(vertices) - 4, len(vertices) - 7],
                    [len(vertices) - 7, len(vertices) - 4, len(vertices) - 3],
                    [len(vertices) - 6, len(vertices) - 5, len(vertices) - 2],
                    [len(vertices) - 5, len(vertices) - 1, len(vertices) - 2]
                ])

    mesh = trimesh.Trimesh(vertices=np.array(vertices), faces=np.array(faces))
    mesh.remove_duplicate_faces()
    mesh.remove_degenerate_faces()
    mesh.remove_unreferenced_vertices()
    return mesh

matrix, start, finish = create_labyrinth(10, 10)
labyrinth = generate_labyrinth(100, 50, 100, matrix)

# Сохранение изосурфейса в OBJ файл
filename = os.path.join(os.path.expanduser("~"), "Desktop", "labyrinth.obj")
labyrinth.export(filename)
print(f"Model saved as {filename}")

# Визуализация
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.add_collection3d(labyrinth)
ax.set_xlim(0, 100)
ax.set_ylim(0, 50)
ax.set_zlim(0, 100)
plt.show()
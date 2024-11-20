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

def generate_room_with_holes(width, height, depth, num_holes, labyrinth_matrix):
    # Определите вершины комнаты
    vertices = [
        [0, 0, 0],
        [width, 0, 0],
        [width, 0, depth],
        [0, 0, depth],
        [0, height, 0],
        [width, height, 0],
        [width, height, depth],
        [0, height, depth]
    ]

    # Определите грани комнаты
    faces = [
        [0, 1, 2],
        [0, 2, 3],
        [4, 5, 6],
        [4, 6, 7],
        [0, 1, 5],
        [0, 5, 4],
        [1, 2, 6],
        [1, 6, 5],
        [2, 3, 7],
        [2, 7, 6],
        [3, 0, 4],
        [3, 4, 7]
    ]

    # Добавляем стены по лабиринту
    cell_width = 10
    for i in range(len(labyrinth_matrix)):
        for j in range(len(labyrinth_matrix[i])):
            if not labyrinth_matrix[i][j]:
                # Если это стена, то добавляем ее в список вершин и граней
                x = i * cell_width
                y = j * cell_width
                z = 0
                vertices.extend([
                    [x, y, z],
                    [x + cell_width, y, z],
                    [x + cell_width, y + cell_width, z],
                    [x, y + cell_width, z],
                    [x, y, height],
                    [x + cell_width, y, height],
                    [x + cell_width, y + cell_width, height],
                    [x, y + cell_width, height]
                ])
                faces.extend([
                    [len(vertices) - 8, len(vertices) - 7, len(vertices) - 6],
                    [len(vertices) - 8, len(vertices) - 6, len(vertices) - 5],
                    [len(vertices) - 4, len(vertices) - 3, len(vertices) - 2],
                    [len(vertices) - 4, len(vertices) - 2, len(vertices) - 1],
                    [len(vertices) - 8, len(vertices) - 4, len(vertices) - 7],
                    [len(vertices) - 7, len(vertices) - 4, len(vertices) - 3],
                    [len(vertices) - 6, len(vertices) - 5, len(vertices) - 2],
                    [len(vertices) - 5, len(vertices) - 1, len(vertices) - 2],
                    [len(vertices) - 8, len(vertices) - 6, len(vertices) - 4],
                    [len(vertices) - 6, len(vertices) - 10, len(vertices) - 4],
                    [len(vertices) - 7, len(vertices) - 3, len(vertices) - 5],
                    [len(vertices) - 5, len(vertices) - 9, len(vertices) - 3]
                ])

    mesh = trimesh.Trimesh(vertices=np.array(vertices), faces=np.array(faces))
    return mesh

matrix, start, finish = create_labyrinth(10, 10)
room = generate_room_with_holes(100, 10, 100, 100, matrix)

# Сохранение изосурфейса в OBJ файл
filename = os.path.join(os.path.expanduser("~"), "Desktop", "room.obj")
room.export(filename)
print(f"Model saved as {filename}")

# Визуализация
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.add_collection3d(room)
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.set_zlim(0, 10)
plt.show()
from random import randint
import heapq
from tkinter import *


water_value = "🌊"
ground_value = "🟩"
water_cost = 2
ground_cost = 1
water_size = 100

dist_matrix = []

class NeighbourCounting:
    global water_size

    @staticmethod
    def count_neighbours(pos, matrix, value):
        sum_neighbours = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                if (not i == j == 0 and 0 <= pos[0] + i < water_size and 0 <= pos[1] + j <
                        water_size and matrix[pos[0] + i][pos[1] + j] == value):
                    sum_neighbours += 1
        return sum_neighbours

    @staticmethod
    def get_neighbours(pos):
        neighbours = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                if (not (i == 0 and j == 0) and 0 <= pos[0] + i < water_size and 0 <= pos[1] + j <
                        water_size):
                    neighbours.append([pos[0] + i, pos[1] + j])
        return neighbours


class Pathfind:
    global water_size

    @staticmethod
    def dijkstra(matrix, h, dist_m, checked_m):
        while len(h) > 0:
            tile = heapq.heappop(h)
            neighbours = NeighbourCounting.get_neighbours(pos=tile)
            checked_m[tile[0]][tile[1]] = True
            for i in neighbours:
                if checked_m[i[0]][i[1]]:
                    continue
                cost = water_cost
                if matrix[i[0]][i[1]] == ground_value:
                    cost = ground_cost
                if dist_m[i[0]][i[1]] == '?' or dist_m[i[0]][i[1]] > dist_m[tile[0]][tile[1]] + cost + 1:
                    dist_m[i[0]][i[1]] = dist_m[tile[0]][tile[1]] + cost + 1
                    heapq.heappush(h, i)
        return dist_m

    @staticmethod
    def get_path(start, end, dist_m, matrix):
        pos = end
        length = 1
        while pos != start:
            neighbours = NeighbourCounting.get_neighbours(pos)
            pos = min(neighbours, key=lambda x: dist_m[x[0]][x[1]])
            cost = water_cost
            if matrix[pos[0]][pos[1]] == ground_value:
                cost = ground_cost
            length += cost + 1
            if pos != start:
                if matrix[pos[0]][pos[1]] == ground_value:
                    matrix[pos[0]][pos[1]] = '⭐'
                else:
                    matrix[pos[0]][pos[1]] = '💠'
        return length

    @staticmethod
    def pathfind(matrix, start, end):
        global dist_matrix, water_cost, ground_cost
        water_cost = water_cost  # wtr_cost_V.get()
        ground_cost = ground_cost  # gnd_cost_V.get()
        dist_matrix = [['?' for i in range(water_size)] for j in range(water_size)]
        checked_matrix = [[False for i in range(water_size)] for j in range(water_size)]
        dist_matrix[start[0]][start[1]] = 0
        checked_matrix[start[0]][start[1]] = True
        h = [start]
        heapq.heapify(h)
        dist_matrix = Pathfind.dijkstra(matrix, h, dist_matrix, checked_matrix)
        return Pathfind.get_path(start, end, dist_matrix, matrix)


class PrintEverywhere:
    def __init__(self):
        self.full_result = ""

    def print_and_record(self, var):
        print(var, end='')
        self.full_result += str(var)

    def tk_print(self):
        label_terminal.configure(text=self.full_result, font=("Arial", 5))


def main():
    try:
        max_P = max_P_V.get()
        density = density_V.get()
        execution_type = draw_V.get()
        if max_P < 3 or density < 1:
            return
    except:
        return
    try:
        global water_size
        result = PrintEverywhere()
        P = []

        for i in range(randint(1, 30)):
            P.append(randint(3, max_P))

        water_size = (len(P) + 2) * (density + 1) + 2

        successful_generation = False

        human_pos = []
        treasure_pos = []

        matrix = [[water_value for i in range(water_size + 10)] for j in range(water_size + 10)]

        while not successful_generation:
            successful_generation = True
            matrix = [[water_value for i in range(water_size + 10)] for j in range(water_size + 10)]
            restart_generation_counter = 0
            for perimeter in P:
                for row in range(len(matrix)):
                    for c in range(len(matrix[row])):
                        if matrix[row][c] == 2:
                            matrix[row][c] = water_value

                if restart_generation_counter >= 10:
                    successful_generation = False
                    break
                while True:
                    pos = [randint(1, water_size - 1), randint(1, water_size - 1)]
                    if NeighbourCounting.count_neighbours(pos, matrix, ground_value) == 0:
                        break
                exit_i_loop_counter = 0
                for i in range(perimeter):
                    exit_while_true_loop_counter = 0
                    while True:
                        matrix[pos[0]][pos[1]] = 2
                        new_pos = [[0, 1], [0, -1], [1, 0], [-1, 0]][randint(0, 3)]
                        if (NeighbourCounting.count_neighbours([pos[0] + new_pos[0], pos[1] + new_pos[1]],
                                                               matrix, ground_value) < 1 and
                                pos[0] + new_pos[0] != 0 and pos[0] + new_pos[0] != water_size - 1 and pos[1] +
                                new_pos[1] != 0 and
                                pos[1] + new_pos[1] != water_size - 1 and matrix[pos[0] + new_pos[0]][pos[1] +
                                                                                                      new_pos[1]] != 2):
                            pos = [pos[0] + new_pos[0], pos[1] + new_pos[1]]
                            break
                        else:
                            exit_while_true_loop_counter += 1
                            if exit_while_true_loop_counter >= 10:
                                exit_i_loop_counter += 1
                                break
                    if exit_i_loop_counter >= 10:
                        restart_generation_counter += 1
                        break

                for row in range(len(matrix)):
                    for c in range(len(matrix[row])):
                        interception = False
                        interceptions = 0
                        for s in range(c, len(matrix[row])):
                            if not interception and matrix[row][s] == 2:
                                interception = True
                                interceptions += 1
                                if interceptions > 1:
                                    break
                            elif not matrix[row][s] == 2:
                                interception = False
                        if interceptions == 1:
                            interception = False
                            interceptions = 0
                            for s in range(len(matrix[row]), c):
                                if not interception and matrix[row][s] == 2:
                                    interception = True
                                    interceptions += 1
                                    if interceptions > 1:
                                        break
                                elif not matrix[row][s]:
                                    interception = False
                            if interceptions == 1:
                                matrix[row][c] = 2

                for row in range(len(matrix)):
                    for c in range(len(matrix[row])):
                        if matrix[row][c] == 2:
                            matrix[row][c] = ground_value

            human_placed = False
            if execution_type == 1:
                while not human_placed:
                    for row in range(len(matrix)):
                        for c in range(len(matrix[row])):
                            if matrix[row][c] == ground_value:
                                if randint(1, 100) == 1 and not human_placed:
                                    human_pos = [row, c]
                                    human_placed = True
                            if matrix[row][c] == 2:
                                matrix[row][c] = ground_value

            if not successful_generation:
                continue

            if execution_type != 3:
                create_treasure_fails = 0
                while not create_treasure_fails >= 50:
                    while True:
                        pos = [randint(2, water_size - 1), randint(2, water_size - 1)]
                        if NeighbourCounting.count_neighbours(pos, matrix, ground_value) == 0:
                            break
                    exit_i_loop_counter = 0
                    for i in range(randint(9, 20)):
                        exit_while_true_loop_counter = 0
                        while True:
                            matrix[pos[0]][pos[1]] = 2
                            new_pos = [[0, 1], [0, -1], [1, 0], [-1, 0]][randint(0, 3)]
                            if (NeighbourCounting.count_neighbours([pos[0] + new_pos[0], pos[1] + new_pos[1]],
                                                                   matrix, ground_value) < 1 and
                                    pos[0] + new_pos[0] != 0 and pos[0] + new_pos[0] != water_size - 1 and pos[1] +
                                    new_pos[1] != 0 and
                                    pos[1] + new_pos[1] != water_size - 1 and matrix[pos[0] + new_pos[0]][pos[1] +
                                                                                                          new_pos[
                                                                                                              1]] != 2):
                                pos = [pos[0] + new_pos[0], pos[1] + new_pos[1]]
                                break
                            else:
                                exit_while_true_loop_counter += 1
                                if exit_while_true_loop_counter >= 10:
                                    exit_i_loop_counter += 1
                                    break
                        if exit_i_loop_counter >= 10:
                            create_treasure_fails += 1
                            break
                    for row in range(len(matrix)):
                        for c in range(len(matrix[row])):
                            interception = False
                            interceptions = 0
                            for s in range(c, len(matrix[row])):
                                if not interception and matrix[row][s] == 2:
                                    interception = True
                                    interceptions += 1
                                    if interceptions > 1:
                                        break
                                elif not matrix[row][s] == 2:
                                    interception = False
                            if interceptions == 1:
                                interception = False
                                interceptions = 0
                                for s in range(len(matrix[row]), c):
                                    if not interception and matrix[row][s] == 2:
                                        interception = True
                                        interceptions += 1
                                        if interceptions > 1:
                                            break
                                    elif not matrix[row][s]:
                                        interception = False
                                if interceptions == 1:
                                    matrix[row][c] = 2
                    successful_generation = False
                    treasure_placed = False
                    for row in range(len(matrix)):
                        if treasure_placed:
                            break
                        for c in range(len(matrix[row])):
                            if (matrix[row][c] == 2 and
                                    NeighbourCounting.count_neighbours([row, c], matrix, 2) == 8):
                                treasure_placed = True
                                successful_generation = True
                                treasure_pos = [row, c]
                                break
                    if successful_generation:
                        break
                    else:
                        create_treasure_fails += 1

            for row in range(len(matrix)):
                for c in range(len(matrix[row])):
                    if matrix[row][c] == 2:
                        matrix[row][c] = ground_value

            fixes = 1
            while fixes != 0:
                fixes = 0
                for row in range(len(matrix)):
                    for c in range(len(matrix[row])):
                        if (matrix[row][c] != ground_value and
                                NeighbourCounting.count_neighbours([row, c], matrix, ground_value) >= 6):
                            matrix[row][c] = ground_value
                            fixes += 1

            if successful_generation:
                break

        if execution_type == 1:
            length = Pathfind.pathfind(matrix=matrix, start=human_pos, end=treasure_pos)
            result.print_and_record(("Длина пути: " + str(length) + " \n"))
            matrix[human_pos[0]][human_pos[1]] = '🧍'
        if execution_type != 3:
            matrix[treasure_pos[0]][treasure_pos[1]] = '🪙'

        for row in matrix:
            for _ in row:
                result.print_and_record((_ + ' \t'))
            result.print_and_record("\n")

        result.tk_print()
        print("\n" * 10)
    except Exception as e:
        print(e)
        main()


root = Tk()
root.title("Человек, острова и сокровище")
root.geometry("1366x768")
root.resizable(False, False)


bg_label_main = Label(root, bg="lightblue", width=1633, height=768)
bg_label_main.pack()
bg_label_main.place(x=0, y=0)


bg_label = Label(root, bg="gray", width=1633, height=5)
bg_label.pack()
bg_label.place(x=0, y=95)


label_title = Label(root, text=f"{'- ' * 10}Генератор островов{' -' * 10}", bg="cyan", width=57, height=2,
                    font=("Arial", 30, "bold"))
label_title.pack()
label_title.place(x=0, y=0)


max_P_V = IntVar()
max_P_V.set(3)

label_entry_max_P = Label(root, text="Максимальный периметр островов")
label_entry_max_P.pack()
label_entry_max_P.place(x=25, y=110)
entry_max_P = Entry(root, textvariable=max_P_V, width=32, borderwidth=5)
entry_max_P.pack()
entry_max_P.place(x=25, y=135)


density_V = IntVar()
density_V.set(1)

label_density = Label(root, text="     Расстояние между островами      ")
label_density.pack()
label_density.place(x=300, y=110)
entry_density = Entry(root, textvariable=density_V, width=32, borderwidth=5)
entry_density.pack()
entry_density.place(x=300, y=135)


draw_V = IntVar()
Radiobutton(root, text="Рисовать человека и кратчайший путь от него к сокровищу", variable=draw_V, value=1, width=50,
            anchor="w").place(x=575, y=103)
Radiobutton(root, text="Рисовать только сокровище", variable=draw_V, value=2, width=50, anchor="w").place(x=575, y=123)
Radiobutton(root, text="Не рисовать человека, кратчайший путь и сокровище", variable=draw_V, value=3, width=50,
            anchor="w").place(x=575, y=143)


#  В разработке
# gnd_cost_V = IntVar()
# wtr_cost_V = IntVar()
# gnd_cost_V.set(1)
# wtr_cost_V.set(2)
#
# label_gnd_cost = Label(root, text="Стоимость пути по земле и по воде в штрафных баллах")
# label_gnd_cost.pack()
# label_gnd_cost.place(x=1025, y=110)
#
# entry_gnd_cost = Entry(root, textvariable=gnd_cost_V, width=5, borderwidth=5, bg="brown")
# entry_gnd_cost.pack()
# entry_gnd_cost.place(x=1053, y=135)
#
# entry_wtr_cost = Entry(root, textvariable=wtr_cost_V, width=5, borderwidth=5, bg="cyan")
# entry_wtr_cost.pack()
# entry_wtr_cost.place(x=1273, y=135)


label_terminal = Label(root, bg="white", width=290, height=75, font=("Arial", 5), anchor="center")
label_terminal.pack()
label_terminal.place(x=100, y=210)


button = Button(root, text='Генерировать', width=50, command=main, bg="green")
button.pack()
button.place(x=500, y=180)


root.mainloop()

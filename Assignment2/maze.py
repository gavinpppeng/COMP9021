# Written by Wenxun Peng for COMP9021 Assignment2 Maze in 17/10/2018


import sys
import re
import copy


class MazeError(Exception):
    def __init__(self, msg):
        self.msg = msg


# ############################################## Defining class Maze ###################################################
class Maze:
    def __init__(self, filename='maze_1.txt'):
        # Getting maze from txt
        self.filename = filename
        file = open(filename)
        file_data = file.read()
        file.close()
        # print(file_data)
        initial_maze = []
        sec_maze = []
        self.maze = []
        try:
            file_lines = file_data.splitlines()
            for line in file_lines:
                line = line.strip("\n").strip(" ")  # delete \n and " ", and the length will become 0
                if len(line) != 0:
                    initial_maze.append(re.split(r' +', line))
        # print(len(num_list[0]))
        except MazeError('Incorrect input.'):
            sys.exit()

        # print(initial_maze)
        # print(len(initial_maze))
        for maze_str in initial_maze:
            # print(len(str(maze_str)))
            for maze_str2 in str(maze_str):
                if maze_str2.isdigit():
                    sec_maze.append(int(maze_str2))
                else:
                    if maze_str2 == ']':
                        self.maze.append(sec_maze)
                        sec_maze = []
        # print(self.maze)
        self.nb_of_rows = len(self.maze)
        self.nb_of_columns = len(self.maze[0])

        if self.nb_of_rows < 2 or self.nb_of_columns < 2 or self.nb_of_rows > 41 or self.nb_of_columns > 31:
            raise MazeError('Incorrect input.')

        for i in range(self.nb_of_rows):
            if len(self.maze[i]) != self.nb_of_columns:
                raise MazeError('Incorrect input.')

            for j in range(self.nb_of_columns):
                if self.maze[i][j] == 0 or self.maze[i][j] == 1 or self.maze[i][j] == 2 or self.maze[i][j] == 3:
                    continue
                else:
                    raise MazeError('Incorrect input.')

        for j in range(self.nb_of_columns):
            if self.maze[self.nb_of_rows-1][j] == 2 or self.maze[self.nb_of_rows-1][j] == 3:
                raise MazeError('Input does not represent a maze.')

        for i in range(self.nb_of_rows):
            if self.maze[i][self.nb_of_columns-1] == 1 or self.maze[i][self.nb_of_columns-1] == 3:
                raise MazeError('Input does not represent a maze.')

        self.walls_traverse = [[False for _ in range(self.nb_of_columns)] for _ in range(self.nb_of_rows)]
        self.explore_confirm = [[False for _ in range(self.nb_of_columns)] for _ in range(self.nb_of_rows)]
        self.initial_cul_de_sacs = [[0 for _ in range(self.nb_of_columns)] for _ in range(self.nb_of_rows)]
        self.cul_de_sacs = [[0 for _ in range(self.nb_of_columns)] for _ in range(self.nb_of_rows)]
        self.cul_de_sacs_confirm = [[False for _ in range(self.nb_of_columns)] for _ in range(self.nb_of_rows)]
        self.gates_traverse = []
        self.yellow_line = []
        self.gates_path = []
        self.judging_if_support = False
        self.nb_of_gates = 0
        self.wall_count = 0
        self.count_unacc_area = 0
        self.count_acc_area = 0
        self.count_cul_de_sacs = 0
        self.count_total_entry_exit = 0

    def find_whole_wall(self, i=0, j=0):
        find_wall = copy.deepcopy(self.maze)
        if find_wall[i][j] == 0:
            self.walls_traverse[i][j] = True
            return 0

        elif find_wall[i][j] == 1:
            self.walls_traverse[i][j] = True
            if i-1 >= 0:        # North
                if self.walls_traverse[i-1][j] is False and (find_wall[i-1][j] == 2 or find_wall[i-1][j] == 3):
                    self.find_whole_wall(i-1, j)
            if i-1 >= 0 and j+1 <= self.nb_of_columns-1:   # Northeast
                if self.walls_traverse[i-1][j+1] is False and (find_wall[i-1][j+1] == 2 or find_wall[i-1][j+1] == 3):
                    self.find_whole_wall(i-1, j+1)
            if j+1 <= self.nb_of_columns-1:      # East
                if self.walls_traverse[i][j+1] is False and find_wall[i][j+1] != 0:  # (1, 2, 3)
                    self.find_whole_wall(i, j+1)
            if j-1 >= 0:      # West
                if self.walls_traverse[i][j-1] is False and (find_wall[i][j-1] == 1 or find_wall[i][j-1] == 3):
                    self.find_whole_wall(i, j-1)

        elif find_wall[i][j] == 2:
            self.walls_traverse[i][j] = True
            if i-1 >= 0:        # North
                if self.walls_traverse[i-1][j] is False and (find_wall[i-1][j] == 2 or find_wall[i-1][j] == 3):
                    self.find_whole_wall(i-1, j)
            if j-1 >= 0:      # West
                if self.walls_traverse[i][j-1] is False and (find_wall[i][j-1] == 1 or find_wall[i][j-1] == 3):
                    self.find_whole_wall(i, j-1)
            if j-1 >= 0 and i+1 <= self.nb_of_rows-1:   # Southwest
                if self.walls_traverse[i+1][j-1] is False and (find_wall[i+1][j-1] == 1 or find_wall[i+1][j-1] == 3):
                    self.find_whole_wall(i+1, j-1)
            if i+1 <= self.nb_of_rows-1:    # South
                if self.walls_traverse[i+1][j] is False and find_wall[i+1][j] != 0:   # (1, 2, 3)
                    self.find_whole_wall(i+1, j)

        elif find_wall[i][j] == 3:
            self.walls_traverse[i][j] = True
            if i-1 >= 0:        # North
                if self.walls_traverse[i-1][j] is False and (find_wall[i-1][j] == 2 or find_wall[i-1][j] == 3):
                    self.find_whole_wall(i-1, j)
            if i+1 <= self.nb_of_rows-1:    # South
                if self.walls_traverse[i+1][j] is False and find_wall[i+1][j] != 0:   # (1, 2, 3)
                    self.find_whole_wall(i+1, j)
            if j-1 >= 0:      # West
                if self.walls_traverse[i][j-1] is False and (find_wall[i][j-1] == 1 or find_wall[i][j-1] == 3):
                    self.find_whole_wall(i, j-1)
            if j+1 <= self.nb_of_columns-1:      # East
                if self.walls_traverse[i][j+1] is False and find_wall[i][j+1] != 0:  # (1, 2, 3)
                    self.find_whole_wall(i, j+1)
            if j-1 >= 0 and i+1 <= self.nb_of_rows-1:   # Southwest
                if self.walls_traverse[i+1][j-1] is False and (find_wall[i+1][j-1] == 1 or find_wall[i+1][j-1] == 3):
                    self.find_whole_wall(i+1, j-1)
            if i-1 >= 0 and j+1 <= self.nb_of_columns - 1:  # Northeast
                if self.walls_traverse[i-1][j+1] is False and (find_wall[i-1][j+1] == 2 or find_wall[i-1][j+1] == 3):
                    self.find_whole_wall(i-1, j+1)

        return 1

    def explore_accessible_area(self, i=0, j=0):
        explore_area = copy.deepcopy(self.maze)
        # border
        if i == self.nb_of_rows-1:     # North
            self.explore_confirm[i][j] = True
            if self.explore_confirm[i-1][j] is False:   # (0, 1, 2, 3)
                self.explore_accessible_area(i-1, j)

        elif j == self.nb_of_columns-1:     # West
            self.explore_confirm[i][j] = True
            if self.explore_confirm[i][j - 1] is False:  # (0, 1, 2, 3)
                self.explore_accessible_area(i, j-1)

        # normal
        elif explore_area[i][j] == 0:   # can go anywhere
            self.explore_confirm[i][j] = True
            if i-1 >= 0:   # North
                if self.explore_confirm[i-1][j] is False:   # (0, 1, 2, 3)
                    self.explore_accessible_area(i-1, j)
            if i+1 <= self.nb_of_rows-1:   # South
                if self.explore_confirm[i+1][j] is False and (explore_area[i+1][j] == 0 or explore_area[i+1][j] == 2):
                    self.explore_accessible_area(i+1, j)
            if j-1 >= 0:   # West
                if self.explore_confirm[i][j-1] is False:  # (0, 1, 2, 3)
                    self.explore_accessible_area(i, j-1)
            if j+1 <= self.nb_of_columns-1:   # East
                if self.explore_confirm[i][j+1] is False and (explore_area[i][j+1] == 0 or explore_area[i][j+1] == 1):
                    self.explore_accessible_area(i, j+1)

        elif explore_area[i][j] == 1:
            self.explore_confirm[i][j] = True
            if i+1 <= self.nb_of_rows-1:   # South
                if self.explore_confirm[i+1][j] is False and (explore_area[i+1][j] == 0 or explore_area[i+1][j] == 2):
                    self.explore_accessible_area(i+1, j)
            if j-1 >= 0:   # West
                if self.explore_confirm[i][j-1] is False:  # (0, 1, 2, 3)
                    self.explore_accessible_area(i, j-1)
            if j+1 <= self.nb_of_columns-1:   # East
                if self.explore_confirm[i][j+1] is False and (explore_area[i][j+1] == 0 or explore_area[i][j+1] == 1):
                    self.explore_accessible_area(i, j+1)

        elif explore_area[i][j] == 2:
            self.explore_confirm[i][j] = True
            if i-1 >= 0:   # North
                if self.explore_confirm[i-1][j] is False:   # (0, 1, 2, 3)
                    self.explore_accessible_area(i-1, j)
            if i+1 <= self.nb_of_rows-1:   # South
                if self.explore_confirm[i+1][j] is False and (explore_area[i+1][j] == 0 or explore_area[i+1][j] == 2):
                    self.explore_accessible_area(i+1, j)
            if j+1 <= self.nb_of_columns-1:   # East
                if self.explore_confirm[i][j+1] is False and (explore_area[i][j+1] == 0 or explore_area[i][j+1] == 1):
                    self.explore_accessible_area(i, j+1)

        else:
            self.explore_confirm[i][j] = True
            if i+1 <= self.nb_of_rows-1:  # South
                if self.explore_confirm[i+1][j] is False and (explore_area[i+1][j] == 0 or explore_area[i+1][j] == 2):
                    self.explore_accessible_area(i+1, j)
            if j+1 <= self.nb_of_columns-1:   # East
                if self.explore_confirm[i][j+1] is False and (explore_area[i][j+1] == 0 or explore_area[i][j+1] == 1):
                    self.explore_accessible_area(i, j+1)
        return

    def explore_cul_de_sacs(self, i=0, j=0, cul_de_sacs_maze=[]):
        if self.initial_cul_de_sacs[i][j] == 1 and self.cul_de_sacs_confirm[i][j] is False:
            self.cul_de_sacs_confirm[i][j] = True
            if cul_de_sacs_maze[i][j] == 0:     # ############  0
                if i-1 >= 0:   # North
                    if self.cul_de_sacs_confirm[i-1][j] is False and self.initial_cul_de_sacs[i-1][j] > 1:
                        self.initial_cul_de_sacs[i-1][j] -= 1
                        self.explore_cul_de_sacs(i-1, j, cul_de_sacs_maze)

                if i+1 <= self.nb_of_rows-1:   # South
                    if self.cul_de_sacs_confirm[i+1][j] is False and \
                            (cul_de_sacs_maze[i+1][j] == 0 or cul_de_sacs_maze[i+1][j] == 2) \
                            and self.initial_cul_de_sacs[i+1][j] > 1:
                        self.initial_cul_de_sacs[i+1][j] -= 1
                        self.explore_cul_de_sacs(i+1, j, cul_de_sacs_maze)

                if j-1 >= 0:        # West
                    if self.cul_de_sacs_confirm[i][j-1] is False and self.initial_cul_de_sacs[i][j-1] > 1:
                        self.initial_cul_de_sacs[i][j-1] -= 1
                        self.explore_cul_de_sacs(i, j-1, cul_de_sacs_maze)

                if j+1 <= self.nb_of_columns-1:  # East
                    if self.cul_de_sacs_confirm[i][j+1] is False and \
                            (cul_de_sacs_maze[i][j+1] == 0 or cul_de_sacs_maze[i][j+1] == 1) and \
                            self.initial_cul_de_sacs[i][j+1] > 1:
                        self.initial_cul_de_sacs[i][j+1] -= 1
                        self.explore_cul_de_sacs(i, j+1, cul_de_sacs_maze)

            elif cul_de_sacs_maze[i][j] == 1:   # ############  1
                if i + 1 <= self.nb_of_rows - 1:  # South
                    if self.cul_de_sacs_confirm[i + 1][j] is False and \
                            (cul_de_sacs_maze[i + 1][j] == 0 or cul_de_sacs_maze[i + 1][j] == 2) and \
                            self.initial_cul_de_sacs[i + 1][j] > 1:
                        self.initial_cul_de_sacs[i + 1][j] -= 1
                        self.explore_cul_de_sacs(i + 1, j, cul_de_sacs_maze)

                if j - 1 >= 0:  # West
                    if self.cul_de_sacs_confirm[i][j - 1] is False and self.initial_cul_de_sacs[i][j - 1] > 1:
                        self.initial_cul_de_sacs[i][j - 1] -= 1
                        self.explore_cul_de_sacs(i, j - 1, cul_de_sacs_maze)

                if j + 1 <= self.nb_of_columns - 1:  # East
                    if self.cul_de_sacs_confirm[i][j + 1] is False and \
                            (cul_de_sacs_maze[i][j + 1] == 0 or cul_de_sacs_maze[i][j + 1] == 1) and \
                            self.initial_cul_de_sacs[i][j + 1] > 1:
                        self.initial_cul_de_sacs[i][j + 1] -= 1
                        self.explore_cul_de_sacs(i, j + 1, cul_de_sacs_maze)

            elif cul_de_sacs_maze[i][j] == 2:        # ############  2
                if i - 1 >= 0:  # North
                    if self.cul_de_sacs_confirm[i - 1][j] is False and self.initial_cul_de_sacs[i - 1][j] > 1:
                        self.initial_cul_de_sacs[i - 1][j] -= 1
                        self.explore_cul_de_sacs(i - 1, j, cul_de_sacs_maze)

                if i + 1 <= self.nb_of_rows - 1:  # South
                    if self.cul_de_sacs_confirm[i + 1][j] is False and \
                            (cul_de_sacs_maze[i + 1][j] == 0 or cul_de_sacs_maze[i + 1][j] == 2) and \
                            self.initial_cul_de_sacs[i + 1][j] > 1:
                        self.initial_cul_de_sacs[i + 1][j] -= 1
                        self.explore_cul_de_sacs(i + 1, j, cul_de_sacs_maze)

                if j + 1 <= self.nb_of_columns - 1:  # East
                    if self.cul_de_sacs_confirm[i][j + 1] is False and \
                            (cul_de_sacs_maze[i][j + 1] == 0 or cul_de_sacs_maze[i][j + 1] == 1) and \
                            self.initial_cul_de_sacs[i][j + 1] > 1:
                        self.initial_cul_de_sacs[i][j + 1] -= 1
                        self.explore_cul_de_sacs(i, j + 1, cul_de_sacs_maze)

            elif cul_de_sacs_maze[i][j] == 3:         # ############  3
                if i + 1 <= self.nb_of_rows - 1:  # South
                    if self.cul_de_sacs_confirm[i + 1][j] is False and \
                            (cul_de_sacs_maze[i + 1][j] == 0 or cul_de_sacs_maze[i + 1][j] == 2) and \
                            self.initial_cul_de_sacs[i + 1][j] > 1:
                        self.initial_cul_de_sacs[i + 1][j] -= 1
                        self.explore_cul_de_sacs(i + 1, j, cul_de_sacs_maze)

                if j + 1 <= self.nb_of_columns - 1:  # East
                    if self.cul_de_sacs_confirm[i][j + 1] is False and \
                            (cul_de_sacs_maze[i][j + 1] == 0 or cul_de_sacs_maze[i][j + 1] == 1) and \
                            self.initial_cul_de_sacs[i][j + 1] > 1:
                        self.initial_cul_de_sacs[i][j + 1] -= 1
                        # print(self.initial_cul_de_sacs[i][j+1])
                        self.explore_cul_de_sacs(i, j + 1, cul_de_sacs_maze)

        return

    def find_cul_de_sacs(self, i=0, j=0, cul_de_sacs_maze=[]):
        self.cul_de_sacs_confirm[i][j] = True
        if cul_de_sacs_maze[i][j] == 0:  # ############  0
            if i-1 >= 0:  # North
                if self.cul_de_sacs_confirm[i-1][j] is False and self.initial_cul_de_sacs[i-1][j] == 1:
                    self.find_cul_de_sacs(i-1, j, cul_de_sacs_maze)

            if i+1 <= self.nb_of_rows-1:  # South
                if self.cul_de_sacs_confirm[i+1][j] is False and \
                        (cul_de_sacs_maze[i+1][j] == 0 or cul_de_sacs_maze[i+1][j] == 2) \
                        and self.initial_cul_de_sacs[i+1][j] == 1:
                    self.find_cul_de_sacs(i+1, j, cul_de_sacs_maze)

            if j-1 >= 0:  # West
                if self.cul_de_sacs_confirm[i][j - 1] is False and self.initial_cul_de_sacs[i][j-1] == 1:
                    self.find_cul_de_sacs(i, j-1, cul_de_sacs_maze)

            if j + 1 <= self.nb_of_columns - 1:  # East
                if self.cul_de_sacs_confirm[i][j + 1] is False and \
                        (cul_de_sacs_maze[i][j + 1] == 0 or cul_de_sacs_maze[i][j + 1] == 1) and \
                        self.initial_cul_de_sacs[i][j + 1] == 1:
                    self.find_cul_de_sacs(i, j + 1, cul_de_sacs_maze)

        elif cul_de_sacs_maze[i][j] == 1:  # ############  1
            if i + 1 <= self.nb_of_rows - 1:  # South
                if self.cul_de_sacs_confirm[i + 1][j] is False and \
                        (cul_de_sacs_maze[i + 1][j] == 0 or cul_de_sacs_maze[i + 1][j] == 2) and \
                        self.initial_cul_de_sacs[i + 1][j] == 1:
                    self.find_cul_de_sacs(i + 1, j, cul_de_sacs_maze)

            if j - 1 >= 0:  # West
                if self.cul_de_sacs_confirm[i][j - 1] is False and self.initial_cul_de_sacs[i][j - 1] == 1:
                    self.find_cul_de_sacs(i, j - 1, cul_de_sacs_maze)

            if j + 1 <= self.nb_of_columns - 1:  # East
                if self.cul_de_sacs_confirm[i][j + 1] is False and \
                        (cul_de_sacs_maze[i][j + 1] == 0 or cul_de_sacs_maze[i][j + 1] == 1) and \
                        self.initial_cul_de_sacs[i][j + 1] == 1:
                    self.find_cul_de_sacs(i, j + 1, cul_de_sacs_maze)

        elif cul_de_sacs_maze[i][j] == 2:  # ############  2
            if i - 1 >= 0:  # North
                if self.cul_de_sacs_confirm[i - 1][j] is False and self.initial_cul_de_sacs[i - 1][j] == 1:
                    self.find_cul_de_sacs(i - 1, j, cul_de_sacs_maze)

            if i + 1 <= self.nb_of_rows - 1:  # South
                if self.cul_de_sacs_confirm[i + 1][j] is False and \
                        (cul_de_sacs_maze[i + 1][j] == 0 or cul_de_sacs_maze[i + 1][j] == 2) and \
                        self.initial_cul_de_sacs[i + 1][j] == 1:
                    self.find_cul_de_sacs(i + 1, j, cul_de_sacs_maze)

            if j + 1 <= self.nb_of_columns - 1:  # East
                if self.cul_de_sacs_confirm[i][j + 1] is False and \
                        (cul_de_sacs_maze[i][j + 1] == 0 or cul_de_sacs_maze[i][j + 1] == 1) and \
                        self.initial_cul_de_sacs[i][j + 1] == 1:
                    self.find_cul_de_sacs(i, j + 1, cul_de_sacs_maze)

        elif cul_de_sacs_maze[i][j] == 3:  # ############  3
            if i + 1 <= self.nb_of_rows - 1:  # South
                if self.cul_de_sacs_confirm[i + 1][j] is False and \
                        (cul_de_sacs_maze[i + 1][j] == 0 or cul_de_sacs_maze[i + 1][j] == 2) and \
                        self.initial_cul_de_sacs[i + 1][j] == 1:
                    self.find_cul_de_sacs(i + 1, j, cul_de_sacs_maze)

            if j + 1 <= self.nb_of_columns - 1:  # East
                if self.cul_de_sacs_confirm[i][j + 1] is False and \
                        (cul_de_sacs_maze[i][j + 1] == 0 or cul_de_sacs_maze[i][j + 1] == 1) and \
                        self.initial_cul_de_sacs[i][j + 1] == 1:
                    # print(self.initial_cul_de_sacs[i][j + 1])
                    self.find_cul_de_sacs(i, j + 1, cul_de_sacs_maze)
        return

    def entry_exit_only_way(self, i=0, j=0, cul_de_sacs_maze=[], different_gates=False):

        if self.cul_de_sacs[i][j] == 2 and self.cul_de_sacs_confirm[i][j] is False:
            self.cul_de_sacs_confirm[i][j] = True
            if (i, j) in self.gates_traverse:
                self.gates_traverse.remove((i, j))
                if (i, j) in self.gates_traverse:  # same coordinate but different gate that means the gate is still in
                    self.gates_path.append((i, j))
                    self.yellow_line.append(self.gates_path)
                    self.gates_path = []
                    return
                if different_gates is True:
                    self.gates_path.append((i, j))
                    self.yellow_line.append(self.gates_path)
                    self.gates_path = []
                    return

            if i == self.nb_of_rows-1:
                if cul_de_sacs_maze[i][j] == 0:
                    if i - 1 >= 0:  # North
                        if self.cul_de_sacs_confirm[i - 1][j] is False and self.cul_de_sacs[i - 1][j] == 2:
                            self.gates_path.append((i, j))
                            self.entry_exit_only_way(i - 1, j, cul_de_sacs_maze, True)
                            return
            else:
                if j == self.nb_of_columns-1:
                    if cul_de_sacs_maze[i][j] == 0:
                        if j - 1 >= 0:  # West
                            if self.cul_de_sacs_confirm[i][j - 1] is False and self.cul_de_sacs[i][j - 1] == 2:
                                self.gates_path.append((i, j))
                                self.entry_exit_only_way(i, j - 1, cul_de_sacs_maze, True)
                                return
                else:
                    if cul_de_sacs_maze[i][j] == 0:  # ############  0
                        if i - 1 >= 0:  # North
                            if self.cul_de_sacs_confirm[i - 1][j] is False and self.cul_de_sacs[i - 1][j] == 2:
                                self.gates_path.append((i, j))
                                self.entry_exit_only_way(i - 1, j, cul_de_sacs_maze, True)
                                return

                        if i + 1 <= self.nb_of_rows - 1:  # South
                            if self.cul_de_sacs_confirm[i + 1][j] is False and \
                                    (cul_de_sacs_maze[i + 1][j] == 0 or cul_de_sacs_maze[i + 1][j] == 2) \
                                    and self.cul_de_sacs[i + 1][j] == 2:
                                self.gates_path.append((i, j))
                                self.entry_exit_only_way(i + 1, j, cul_de_sacs_maze, True)
                                return

                        if j - 1 >= 0:  # West
                            if self.cul_de_sacs_confirm[i][j - 1] is False and self.cul_de_sacs[i][j - 1] == 2:
                                self.gates_path.append((i, j))
                                self.entry_exit_only_way(i, j - 1, cul_de_sacs_maze, True)
                                return

                        if j + 1 <= self.nb_of_columns - 1:  # East
                            if self.cul_de_sacs_confirm[i][j + 1] is False and \
                                    (cul_de_sacs_maze[i][j + 1] == 0 or cul_de_sacs_maze[i][j + 1] == 1) and \
                                    self.cul_de_sacs[i][j + 1] == 2:
                                self.gates_path.append((i, j))
                                self.entry_exit_only_way(i, j + 1, cul_de_sacs_maze, True)
                                return

                    elif cul_de_sacs_maze[i][j] == 1:  # ############  1
                        if i + 1 <= self.nb_of_rows - 1:  # South
                            if self.cul_de_sacs_confirm[i + 1][j] is False and \
                                    (cul_de_sacs_maze[i + 1][j] == 0 or cul_de_sacs_maze[i + 1][j] == 2) and \
                                    self.cul_de_sacs[i + 1][j] == 2:
                                self.gates_path.append((i, j))
                                self.entry_exit_only_way(i + 1, j, cul_de_sacs_maze, True)
                                return

                        if j - 1 >= 0:  # West
                            if self.cul_de_sacs_confirm[i][j - 1] is False and self.cul_de_sacs[i][j - 1] == 2:
                                self.gates_path.append((i, j))
                                self.entry_exit_only_way(i, j - 1, cul_de_sacs_maze, True)
                                return

                        if j + 1 <= self.nb_of_columns - 1:  # East
                            if self.cul_de_sacs_confirm[i][j + 1] is False and \
                                    (cul_de_sacs_maze[i][j + 1] == 0 or cul_de_sacs_maze[i][j + 1] == 1) and \
                                    self.cul_de_sacs[i][j + 1] == 2:
                                self.gates_path.append((i, j))
                                self.entry_exit_only_way(i, j + 1, cul_de_sacs_maze, True)
                                return

                    elif cul_de_sacs_maze[i][j] == 2:  # ############  2
                        if i - 1 >= 0:  # North
                            if self.cul_de_sacs_confirm[i - 1][j] is False and self.cul_de_sacs[i - 1][j] == 2:
                                self.gates_path.append((i, j))
                                self.entry_exit_only_way(i - 1, j, cul_de_sacs_maze, True)
                                return

                        if i + 1 <= self.nb_of_rows - 1:  # South
                            if self.cul_de_sacs_confirm[i + 1][j] is False and \
                                    (cul_de_sacs_maze[i + 1][j] == 0 or cul_de_sacs_maze[i + 1][j] == 2) and \
                                    self.cul_de_sacs[i + 1][j] == 2:
                                self.gates_path.append((i, j))
                                self.entry_exit_only_way(i + 1, j, cul_de_sacs_maze, True)
                                return

                        if j + 1 <= self.nb_of_columns - 1:  # East
                            if self.cul_de_sacs_confirm[i][j + 1] is False and \
                                    (cul_de_sacs_maze[i][j + 1] == 0 or cul_de_sacs_maze[i][j + 1] == 1) and \
                                    self.cul_de_sacs[i][j + 1] == 2:
                                self.gates_path.append((i, j))
                                self.entry_exit_only_way(i, j + 1, cul_de_sacs_maze, True)
                                return

                    elif cul_de_sacs_maze[i][j] == 3:  # ############  3
                        if i + 1 <= self.nb_of_rows - 1:  # South
                            if self.cul_de_sacs_confirm[i + 1][j] is False and \
                                    (cul_de_sacs_maze[i + 1][j] == 0 or cul_de_sacs_maze[i + 1][j] == 2) and \
                                    self.cul_de_sacs[i + 1][j] == 2:
                                self.gates_path.append((i, j))
                                self.entry_exit_only_way(i + 1, j, cul_de_sacs_maze, True)
                                return

                        if j + 1 <= self.nb_of_columns - 1:  # East
                            if self.cul_de_sacs_confirm[i][j + 1] is False and \
                                    (cul_de_sacs_maze[i][j + 1] == 0 or cul_de_sacs_maze[i][j + 1] == 1) and \
                                    self.cul_de_sacs[i][j + 1] == 2:
                                # print(self.cul_de_sacs[i][j + 1])
                                self.gates_path.append((i, j))
                                self.entry_exit_only_way(i, j + 1, cul_de_sacs_maze, True)
                                return

    def analyse_support(self):
        self.judging_if_support = True
        global gates_coordinate
        # ###################### Finding number of gates ############################
        nb_of_gates = 0
        gates_coordinate = []
        maze_gate = copy.deepcopy(self.maze)
        nb_of_rows = len(maze_gate)
        nb_of_columns = len(maze_gate[0])
        # situation 1(First row):
        for gates in range(nb_of_columns-1):
            if maze_gate[0][gates] == 0 or maze_gate[0][gates] == 2:
                gates_coordinate.append((0, gates))
                nb_of_gates += 1
        # situation 2(Last row):
        for gates in range(nb_of_columns-1):
            if maze_gate[nb_of_rows-1][gates] == 0 or maze_gate[nb_of_rows-1][gates] == 2:
                gates_coordinate.append((nb_of_rows-1, gates))
                nb_of_gates += 1
        # situation 3(First column):
        for gates in range(nb_of_rows-1):
            if maze_gate[gates][0] == 0 or maze_gate[gates][0] == 1:
                gates_coordinate.append((gates, 0))
                nb_of_gates += 1
        # situation 4(Last column):
        for gates in range(nb_of_rows-1):
            if maze_gate[gates][nb_of_columns-1] == 0 or maze_gate[gates][nb_of_columns-1] == 1:
                gates_coordinate.append((gates, nb_of_columns-1))
                nb_of_gates += 1

        self.nb_of_gates = nb_of_gates

        # ###################### Finding number of sets of walls ############################
        count = 0
        for i in range(nb_of_rows):
            for j in range(nb_of_columns):
                if self.walls_traverse[i][j] is True:
                    continue
                else:
                    count = count + self.find_whole_wall(i, j)

        self.wall_count = count

        # ###################### Finding inaccessible and accessible area ############################
        # print(gates_coordinate)
        count_acc_area = 0
        count_unacc_area = 0
        unacc_point = []
        for gate_in in gates_coordinate:
            x, y = gate_in
            if self.explore_confirm[x][y] is True:
                continue
            else:
                count_acc_area += 1
                self.explore_accessible_area(x, y)
        for i in range(nb_of_rows):
            for j in range(nb_of_columns):
                if self.explore_confirm[i][j] is False and i != nb_of_rows-1 and j != nb_of_columns-1:
                    count_unacc_area += 1
                    unacc_point.append((i, j))

        self.count_unacc_area = count_unacc_area
        self.count_acc_area = count_acc_area

        # ###################### Finding accessible area cul-de-sacs ############################
        cul_de_sacs_maze = copy.deepcopy(self.maze)
        for i in range(self.nb_of_rows):
            for j in range(self.nb_of_columns):
                if cul_de_sacs_maze[i][j] == 0:
                    count_0 = 2
                    if j+1 <= self.nb_of_columns-1:     # East
                        if cul_de_sacs_maze[i][j+1] == 0 or cul_de_sacs_maze[i][j+1] == 1:
                            count_0 += 1
                    if i+1 <= self.nb_of_rows-1:      # South
                        if cul_de_sacs_maze[i+1][j] == 0 or cul_de_sacs_maze[i+1][j] == 2:
                            count_0 += 1
                    self.initial_cul_de_sacs[i][j] = count_0
                elif cul_de_sacs_maze[i][j] == 1:
                    count_1 = 1
                    if j+1 <= self.nb_of_columns-1:     # East
                        if cul_de_sacs_maze[i][j+1] == 0 or cul_de_sacs_maze[i][j+1] == 1:
                            count_1 += 1
                    if i+1 <= self.nb_of_rows-1:      # South
                        if cul_de_sacs_maze[i+1][j] == 0 or cul_de_sacs_maze[i+1][j] == 2:
                            count_1 += 1
                    self.initial_cul_de_sacs[i][j] = count_1
                elif cul_de_sacs_maze[i][j] == 2:
                    count_2 = 1
                    if j+1 <= self.nb_of_columns-1:     # East
                        if cul_de_sacs_maze[i][j+1] == 0 or cul_de_sacs_maze[i][j+1] == 1:
                            count_2 += 1
                    if i+1 <= self.nb_of_rows-1:      # South
                        if cul_de_sacs_maze[i+1][j] == 0 or cul_de_sacs_maze[i+1][j] == 2:
                            count_2 += 1
                    self.initial_cul_de_sacs[i][j] = count_2
                else:
                    count_3 = 0
                    if j+1 <= self.nb_of_columns-1:     # East
                        if cul_de_sacs_maze[i][j+1] == 0 or cul_de_sacs_maze[i][j+1] == 1:
                            count_3 += 1
                    if i+1 <= self.nb_of_rows-1:      # South
                        if cul_de_sacs_maze[i+1][j] == 0 or cul_de_sacs_maze[i+1][j] == 2:
                            count_3 += 1
                    self.initial_cul_de_sacs[i][j] = count_3
        # eliminating inaccessible area
        for x, y in unacc_point:
            self.initial_cul_de_sacs[x][y] = 0

        for i in range(self.nb_of_rows):
            for j in range(self.nb_of_columns):
                if self.initial_cul_de_sacs[i][j] == 1 and self.cul_de_sacs_confirm[i][j] is False:
                    self.explore_cul_de_sacs(i, j, cul_de_sacs_maze)

        # resetting cul_de_sacs
        # count the number of cul_de_sacs
        self.cul_de_sacs_confirm = [[False for _ in range(self.nb_of_columns)] for _ in range(self.nb_of_rows)]
        count_cul_de_sacs = 0
        for i in range(self.nb_of_rows):
            for j in range(self.nb_of_columns):
                if self.initial_cul_de_sacs[i][j] == 1 and self.cul_de_sacs_confirm[i][j] is False:
                    self.find_cul_de_sacs(i, j, cul_de_sacs_maze)
                    count_cul_de_sacs += 1

        self.count_cul_de_sacs = count_cul_de_sacs

        # ###################### Finding entry-exit with no intersection ############################
        self.cul_de_sacs_confirm = [[False for _ in range(self.nb_of_columns)] for _ in range(self.nb_of_rows)]
        self.gates_traverse = copy.deepcopy(gates_coordinate)
        self.cul_de_sacs = copy.deepcopy(self.initial_cul_de_sacs)
        for j in range(nb_of_columns):
            self.cul_de_sacs[self.nb_of_rows-1][j] -= 1
        for i in range(nb_of_rows):
            self.cul_de_sacs[i][self.nb_of_columns-1] -= 1
        # print(f'cul_de_sacs is {self.cul_de_sacs}')

        for x, y in gates_coordinate:
            if (x, y) in self.gates_traverse:
                self.gates_path = []
                self.entry_exit_only_way(x, y, cul_de_sacs_maze, False)

        count_total_entry_exit = len(self.yellow_line)
        self.count_total_entry_exit = count_total_entry_exit

    def analyse(self):
        if self.judging_if_support is False:
            self.analyse_support()
        if self.nb_of_gates == 0:
            print('The maze has no gate.')
        elif self.nb_of_gates == 1:
            print('The maze has a single gate.')
        else:
            print(f'The maze has {self.nb_of_gates} gates.')

        if self.wall_count == 0:
            print('The maze has no wall.')
        elif self.wall_count == 1:
            print('The maze has walls that are all connected.')
        else:
            print(f'The maze has {self.wall_count} sets of walls that are all connected.')

        if self.count_unacc_area == 0:
            print('The maze has no inaccessible inner point.')
        elif self.count_unacc_area == 1:
            print('The maze has a unique inaccessible inner point.')
        else:
            print(f'The maze has {self.count_unacc_area} inaccessible inner points.')

        if self.count_acc_area == 0:
            print('The maze has no accessible area.')
        elif self.count_acc_area == 1:
            print('The maze has a unique accessible area.')
        else:
            print(f'The maze has {self.count_acc_area} accessible areas.')

        if self.count_cul_de_sacs == 0:
            print('The maze has no accessible cul-de-sac.')
        elif self.count_cul_de_sacs == 1:
            print('The maze has accessible cul-de-sacs that are all connected.')
        else:
            print(f'The maze has {self.count_cul_de_sacs} sets of accessible cul-de-sacs that are all connected.')

        if self.count_total_entry_exit == 0:
            print('The maze has no entry-exit path with no intersection not to cul-de-sacs.')
        elif self.count_total_entry_exit == 1:
            print('The maze has a unique entry-exit path with no intersection not to cul-de-sacs.')
        else:
            print(f'The maze has {self.count_total_entry_exit} entry-exit '
                  f'paths with no intersections not to cul-de-sacs.')






    def display(self):
        if self.judging_if_support is False:
            self.analyse_support()
        draw_rows = []
        draw_columns = []
        pdf_filename = self.filename[0:-4] + ".tex"
        pdf_generate = open(pdf_filename, "w")
        pdf_generate.writelines("\\documentclass[10pt]{article}\n")
        pdf_generate.writelines("\\usepackage{tikz}\n")
        pdf_generate.writelines("\\usetikzlibrary{shapes.misc}\n")
        pdf_generate.writelines("\\usepackage[margin=0cm]{geometry}\n")
        pdf_generate.writelines("\\pagestyle{empty}\n")
        pdf_generate.writelines("\\tikzstyle{every node}=[cross out, draw, red]\n")
        pdf_generate.writelines("\n")
        pdf_generate.writelines("\\begin{document}\n")
        pdf_generate.writelines("\n")
        pdf_generate.writelines("\\vspace*{\\fill}\n")
        pdf_generate.writelines("\\begin{center}\n")
        pdf_generate.writelines("\\begin{tikzpicture}[x=0.5cm, y=-0.5cm, ultra thick, blue]\n")

        pdf_generate.writelines("% Walls\n")

        # ######################### print horizontal ###################################################################
        for i in range(self.nb_of_rows):
            for j in range(self.nb_of_columns):
                if self.maze[i][j] == 1 or self.maze[i][j] == 3:
                    draw_rows.append((j, i))

        # print(draw_rows)
        draw_rows_count = [0 for _ in range(len(draw_rows))]
        # print(draw_rows_count)

        for i in range(len(draw_rows)):
            if i+1 < len(draw_rows):
                if draw_rows[i][0] + 1 == draw_rows[i+1][0] and draw_rows[i][1] == draw_rows[i+1][1]:
                    draw_rows_count[i] += 1

        # print(draw_rows_count)
        p = 0
        while p < len(draw_rows_count):
            p1 = p
            while draw_rows_count[p1] == 1 and p1 < len(draw_rows_count):
                draw_rows_count[p] += 1
                p1 += 1
            p += 1

        # print(draw_rows_count)
        q = 0
        while q < len(draw_rows_count):
            if draw_rows_count[q] == 0:
                pdf_generate.writelines(f'    \draw ({draw_rows[q][0]},{draw_rows[q][1]}) -- '
                                        f'({draw_rows[q][0]+1},{draw_rows[q][1]});\n')
                q += 1
            else:
                pdf_generate.writelines(f'    \draw ({draw_rows[q][0]},{draw_rows[q][1]}) -- '
                                        f'({draw_rows[q][0]+draw_rows_count[q]},{draw_rows[q][1]});\n')
                q = q + draw_rows_count[q]

        # ######################### print vertical #####################################################################
        for j in range(self.nb_of_columns):
            for i in range(self.nb_of_rows):
                if self.maze[i][j] == 2 or self.maze[i][j] == 3:
                    draw_columns.append((j, i))

        # print(draw_columns)
        draw_columns_count = [0 for _ in range(len(draw_columns))]
        # print(draw_columns_count)

        for i in range(len(draw_columns)):
            if i+1 < len(draw_columns):
                if draw_columns[i][1] + 1 == draw_columns[i+1][1] and draw_columns[i][0] == draw_columns[i+1][0]:
                    draw_columns_count[i] += 1

        # print(draw_columns_count)
        p = 0
        while p < len(draw_columns_count):
            p1 = p
            while draw_columns_count[p1] == 1 and p1 < len(draw_columns_count):
                draw_columns_count[p] += 1
                p1 += 1
            p += 1

        # print(draw_columns_count)
        q = 0
        while q < len(draw_columns_count):
            if draw_columns_count[q] == 0:
                pdf_generate.writelines(f'    \draw ({draw_columns[q][0]},{draw_columns[q][1]}) -- '
                                        f'({draw_columns[q][0]},{draw_columns[q][1]+1});\n')
                q += 1
            else:
                pdf_generate.writelines(f'    \draw ({draw_columns[q][0]},{draw_columns[q][1]}) -- '
                                        f'({draw_columns[q][0]},{draw_columns[q][1]+draw_columns_count[q]});\n')
                q = q + draw_columns_count[q]

        # ######################### print pillars ######################################################################
        pdf_generate.writelines("% Pillars\n")

        # ######################### find pillars #######################################################################
        pillars = []
        for i in range(self.nb_of_rows):
            for j in range(self.nb_of_columns):
                if self.maze[i][j] == 0:
                    if i-1 >= 0:
                        if self.maze[i-1][j] == 2 or self.maze[i-1][j] == 3:
                            continue
                    if j-1 >= 0:
                        if self.maze[i][j-1] == 1 or self.maze[i][j-1] == 3:
                            continue
                    pillars.append((i, j))
        # print(pillars)
        for i in range(len(pillars)):
            pdf_generate.writelines(f'    \\fill[green] ({pillars[i][1]},{pillars[i][0]}) circle(0.2);\n')

        # ######################### print accessible cul-de-sacs #######################################################
        pdf_generate.writelines("% Inner points in accessible cul-de-sacs\n")
        print_cul_de_sacs = []
        for i in range(self.nb_of_rows):
            for j in range(self.nb_of_columns):
                if self.initial_cul_de_sacs[i][j] == 1:
                    print_cul_de_sacs.append((i, j))
        # print(print_cul_de_sacs)

        for j in range(len(print_cul_de_sacs)):
            pdf_generate.write(f'    \\node at ({print_cul_de_sacs[j][1] + 0.5},{print_cul_de_sacs[j][0] + 0.5}) ')
            pdf_generate.write('{};\n')

        # ######################### print entry-exit paths #############################################################
        pdf_generate.write('% Entry-exit paths without intersections\n')
        # print(self.yellow_line)
        single_point = []
        gates_print = []
        for yl in self.yellow_line:
            if len(yl) == 1:
                single_point = single_point + yl
        # print(single_point)

        for gp in self.yellow_line:
            gates_print = gates_print + gp

        already_print = []
        real_row_print = []

        # ######################### print horizontal ###################################################################
        for i in range(self.nb_of_rows):
            for j in range(self.nb_of_columns):
                if (i, j) in already_print:
                    continue
                else:
                    if (i, j) in single_point:
                        pdf_generate.write(f'    \draw[dashed, yellow] ({-j-0.5},{i+0.5}) -- ({j+0.5},{i+0.5});\n')
                        continue

                    for yellow_line in self.yellow_line:
                        if (i, j) in yellow_line:
                            for seek in range(len(yellow_line)):
                                if seek+1 < len(yellow_line):
                                    if yellow_line[seek] == (i, j) and yellow_line[seek+1] == (i, j+1):
                                        real_row_print.append((i, j))
                                        already_print.append((i, j))
                                        seek2 = seek
                                        j2 = j
                                        while yellow_line[seek2+1] == (i, j2+1):
                                            already_print.append((i, j2+1))
                                            j2 += 1
                                            seek2 += 1
                                            if seek2+1 >= len(yellow_line):
                                                break
                                        real_row_print.append((i, j2))
                                        # print(real_row_print)
                                        if j == 0 and (i, j) in gates_coordinate:
                                            pdf_generate.write(
                                                f'    \draw[dashed, yellow] ({-0.5},{i+0.5}) -- ({j2+0.5},{i+0.5});\n')
                                        else:
                                            pdf_generate.write(
                                                f'    \draw[dashed, yellow] ({j+0.5},{i+0.5}) -- ({j2+0.5},{i+0.5});\n')
                                        break

                                if seek-1 >= 0:
                                    if yellow_line[seek] == (i, j) and yellow_line[seek - 1] == (i, j + 1):
                                        real_row_print.append((i, j))
                                        already_print.append((i, j))
                                        seek2 = seek
                                        j2 = j
                                        while yellow_line[seek2 - 1] == (i, j2 + 1):
                                            already_print.append((i, j2 + 1))
                                            j2 += 1
                                            seek2 -= 1
                                            if seek2 - 1 < 0:
                                                break
                                        real_row_print.append((i, j2))
                                        # print(real_row_print)
                                        if j == 0 and (i, j) in gates_coordinate:
                                            pdf_generate.write(
                                                f'    \draw[dashed, yellow] ({-0.5},{i+0.5}) -- ({j2+0.5},{i+0.5});\n')
                                        else:
                                            pdf_generate.write(
                                                f'    \draw[dashed, yellow] ({j+0.5},{i+0.5}) -- ({j2+0.5},{i+0.5});\n')
                                        break

                    judging_print = 0
                    if (i, j) in gates_print and j == 0 and (i, j) in gates_coordinate \
                            and (i, j) not in already_print:    # no link
                        for yellow_line in self.yellow_line:
                            if (i, j) in yellow_line:
                                for seek in range(len(yellow_line)):
                                    if seek + 1 < len(yellow_line):
                                        if yellow_line[seek] == (i, j) and yellow_line[seek + 1] == (i, j + 1):
                                            judging_print = 1
                                            break
                                    if seek - 1 >= 0:
                                        if yellow_line[seek] == (i, j) and yellow_line[seek - 1] == (i, j + 1):
                                            judging_print = 1
                                            break
                        if judging_print == 1 or i == self.nb_of_rows-1:
                            continue
                        else:
                            pdf_generate.write(f'    \draw[dashed, yellow] ({-0.5},{i+0.5}) -- ({0.5},{i+0.5});\n')

        # ######################### print vertical #####################################################################
        already_columns_print = []
        real_column_print = []
        for j in range(self.nb_of_columns):
            for i in range(self.nb_of_rows):
                if (i, j) in already_columns_print:
                    continue
                else:
                    if (i, j) in single_point:
                        pdf_generate.write(f'    \draw[dashed, yellow] ({j+0.5},{-i-0.5}) -- ({j+0.5},{i+0.5});\n')
                        continue

                    for yellow_line in self.yellow_line:
                        if (i, j) in yellow_line:
                            for seek in range(len(yellow_line)):
                                if seek+1 < len(yellow_line):
                                    if yellow_line[seek] == (i, j) and yellow_line[seek+1] == (i+1, j):
                                        real_column_print.append((i, j))
                                        already_columns_print.append((i, j))
                                        seek2 = seek
                                        i2 = i
                                        while yellow_line[seek2+1] == (i2+1, j):
                                            already_columns_print.append((i2+1, j))
                                            i2 += 1
                                            seek2 += 1
                                            if seek2+1 >= len(yellow_line):
                                                break
                                        real_column_print.append((i2, j))
                                        # print(real_column_print)
                                        if i == 0 and (i, j) in gates_coordinate:
                                            pdf_generate.write(
                                                f'    \draw[dashed, yellow] ({j+0.5},{-0.5}) -- ({j+0.5},{i2+0.5});\n')
                                        else:
                                            pdf_generate.write(
                                                f'    \draw[dashed, yellow] ({j+0.5},{i+0.5}) -- ({j+0.5},{i2+0.5});\n')
                                        break

                                if seek-1 >= 0:
                                    if yellow_line[seek] == (i, j) and yellow_line[seek - 1] == (i+1, j):
                                        real_column_print.append((i, j))
                                        already_columns_print.append((i, j))
                                        seek2 = seek
                                        i2 = i
                                        while yellow_line[seek2 - 1] == (i2+1, j):
                                            already_columns_print.append((i2+1, j))
                                            i2 += 1
                                            seek2 -= 1
                                            if seek2 - 1 < 0:
                                                break
                                        real_column_print.append((i2, j))
                                        # print(real_column_print)
                                        if i == 0 and (i, j) in gates_coordinate:
                                            pdf_generate.write(
                                                f'    \draw[dashed, yellow] ({j+0.5},{-0.5}) -- ({j+0.5},{i2+0.5});\n')
                                        else:
                                            pdf_generate.write(
                                                f'    \draw[dashed, yellow] ({j+0.5},{i+0.5}) -- ({j+0.5},{i2+0.5});\n')
                                        break

                    judging_columns_print = 0
                    if (i, j) in gates_print and i == 0 and (i, j) in gates_coordinate \
                            and (i, j) not in already_columns_print:    # no link
                        for yellow_line in self.yellow_line:
                            if (i, j) in yellow_line:
                                for seek in range(len(yellow_line)):
                                    if seek + 1 < len(yellow_line):
                                        if yellow_line[seek] == (i, j) and yellow_line[seek + 1] == (i + 1, j):
                                            judging_columns_print = 1
                                            break
                                    if seek - 1 >= 0:
                                        if yellow_line[seek] == (i, j) and yellow_line[seek - 1] == (i + 1, j):
                                            judging_columns_print = 1
                                            break
                        if judging_columns_print == 1 or j == self.nb_of_columns-1:
                            continue
                        else:
                            pdf_generate.write(f'    \draw[dashed, yellow] ({j+0.5},{-0.5}) -- ({j+0.5},{0.5});\n')
        # print(already_columns_print)

        # ######################### print end ##########################################################################
        pdf_generate.write('\end{tikzpicture}\n')
        pdf_generate.write('\end{center}\n')
        pdf_generate.write('\\vspace*{\\fill}\n')
        pdf_generate.write('\n')
        pdf_generate.write('\end{document}\n')

'''
maze = Maze()
#maze = Maze('labyrinth.txt')
maze.analyse()
maze.display()
'''



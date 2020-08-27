from random import choice, sample, seed
from copy import deepcopy
from search_algorithms import depth_first_search
from search_problems import FindConqueredProblem

seed(1)


class Board:
    YELLOW = 'Y'
    BLUE = 'B'
    GREEN = 'G'
    RED = 'R'
    COLORS = [YELLOW, BLUE, GREEN, RED]
    NORMAL = 'N'
    KNIGHT = 'K'
    KNIGHT_MODE_ON_MSG = 'Knight mode toggled on!'
    KNIGHT_MODE_OFF_MSG = 'Knight mode toggled off!'

    def __init__(self, size=(18, 18), starting_point=(0, 0), jokers=0, copy=False):
        self.height, self.width = size
        self.starting_point = tuple(starting_point)

        if starting_point[0] < 0 or starting_point[0] >= self.height or \
                starting_point[1] < 0 or starting_point[1] >= self.width:
            self.starting_point = (0, 0)

        if copy:  # If we are calling the constructor to copy the object, we will assign the board in the calling function
            self.board = None
        else:
            self.board = self.__init_random_board()

        self.jokers = int(jokers)
        if jokers > 0:
            self.joker_locations = self.__init_random_jokers()
        self.mode = Board.NORMAL

    def copy(self):
        new_board = Board((self.height, self.width), self.starting_point, self.jokers, copy=True)
        new_board.board = deepcopy(self.board)
        new_board.mode = self.mode
        if self.jokers > 0:
            new_board.joker_locations = deepcopy(self.joker_locations)
        return new_board

    def transpose_board(self):
        """Returns a copy of the transposed board"""
        rotated_board = [[self.board[j][i] for j in range(self.height)] for i in range(self.width)]
        new_board = self.copy()
        new_board.width = self.height
        new_board.height = self.width
        new_board.board = rotated_board
        return new_board

    def toggle_mode(self):
        """Toggles the game mode between normal and knight"""
        if self.mode == Board.NORMAL:
            print(Board.KNIGHT_MODE_ON_MSG)
            self.mode = Board.KNIGHT
        elif self.mode == Board.KNIGHT:
            print(Board.KNIGHT_MODE_OFF_MSG)
            self.mode = Board.NORMAL

    def __init_random_jokers(self):
        """
        Initializes the stored number of jokers and places them across the board
        """
        cells = [(row, col) for row in range(self.height) for col in range(self.width)]
        return sample(cells, self.jokers)

    def __init_random_board(self):
        """
        Initializes the board with the stored sizes. Each cell is colored uniformly over available colors
        and independently of all other squares.
        """
        board = []
        for row in range(self.height):
            new_row = []
            for col in range(self.width):
                new_row.append(choice(Board.COLORS))
            board.append(new_row)
        return board

    def __eq__(self, other):
        for row in range(self.height):
            for col in range(self.width):
                if self.board[row][col] != other.board[row][col]:
                    return False
        return True

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(str(self.board))

    def __lt__(self, other):
        return True

    def __repr__(self):
        return f"Board(size=({self.height}, {self.width}), starting_point={self.starting_point}, jokers={self.jokers})"

    def __str__(self):
        output = ""
        for row in range(self.height):
            for col in range(self.width):
                output += ' ' + self.board[row][col]
            output += '\n'
        return output

    def full_board(self):
        """
        :return: True iff the entire board is colored the same color
        """
        color = self.board[self.height - 1][self.width - 1]  # Arbitrarily choose a color to check
        for row in range(self.height):
            for col in range(self.width):
                if self.board[row][col] != color:
                    return False
        return True

    def apply_color_move(self, color):
        """
        Applies the given color to the board
        :param color: A color in the form of a single char
        """
        all_neighbors = self.find_extended_neighbors_search()
        # all_neighbors = self.find_extended_neighbors(self.starting_point[0], self.starting_point[1], {self.starting_point})
        self.color_neighbors(all_neighbors, color)

    def find_extended_neighbors(self, row, col, neighbors_list):
        """
        Locates all of the neighbors of the same color
        :param row: The row of the target square
        :param col: The col of the target square
        :param neighbors_list: A set containing all of the neighbors found thusfar
        :return: A set of the all of the neighbors starting from the starting point of the same color
        """
        for neigh_row, neigh_col in self.find_neighbors(row, col):

            # If the neighbor is the right color and has not yet been visited (i.e added to the neighbors list)
            if self.board[neigh_row][neigh_col] == self.board[self.starting_point[0]][self.starting_point[1]] and \
                    (neigh_row, neigh_col) not in neighbors_list:

                # If the cell we are looking at is a joker cell
                if self.jokers > 0 and (neigh_row, neigh_col) in self.joker_locations:
                    print(f'Joker found at cell ({neigh_row}, {neigh_col})!')

                    # Add all immediate neighbors to the list of cells to be colored
                    for neighbor in self.find_adjacent_neighbors(neigh_row, neigh_col):
                        neighbors_list.add(neighbor)
                    self.joker_locations.remove((neigh_row, neigh_col))  # disallow multiple discovery

                neighbors_list.add((neigh_row, neigh_col))
                self.find_extended_neighbors(neigh_row, neigh_col, neighbors_list)

        return neighbors_list

    def find_extended_neighbors_search(self):
        problem = FindConqueredProblem(self, self.mode == Board.KNIGHT)
        return depth_first_search(problem)

    def color_neighbors(self, neighbors, color):
        """
        Colors all of the given neighbors the given color
        :param neighbors: A set of all neighbors in the form (x, y)
        :param color: The color
        """
        for row, col in neighbors:
            self.color_one_square(row, col, color)

    def color_one_square(self, row, col, color):
        self.board[row][col] = color

    def find_neighbors(self, row, col):
        """
        Given the coordinates of a target square, finds the neighbors based on the stored mode.
        Possible modes are 'regular' and 'knight'
        """
        if self.mode == Board.KNIGHT:
            return self.find_knight_neighbors(row, col)
        else:
            return self.find_adjacent_neighbors(row, col)

    def find_knight_neighbors(self, row, col):
        """
        Given the coordinates of a square, finds a list of all of the knight neighbors on the board
        :param row: The X-coordinate of the target square
        :param col: The Y-coordinate of the target square
        :return: A list of (x, y) tuples representing all adjacent neighbors
        """
        neighbors = [
            (row - 1, col - 2), (row - 1, col + 2), (row - 2, col - 1), (row - 2, col + 1),
            (row + 1, col - 2), (row + 1, col + 2), (row + 2, col - 1), (row + 2, col + 1)
        ]
        output = []
        for row, col in neighbors:
            if 0 <= row < self.width and 0 <= col < self.height:
                output.append((row, col))
        return output

    def find_adjacent_neighbors(self, row, col):
        """
        Given the coordinates of a square, finds a list of all of the adjacent neighbors on the board
        :param row: The Row-coordinate of the target square
        :param col: The Column-coordinate of the target square
        :return: A list of (row, col) tuples representing all adjacent neighbors
        """
        neighbors = []
        if row > 0:
            neighbors.append((row - 1, col))
        if row < self.width - 1:
            neighbors.append((row + 1, col))
        if col > 0:
            neighbors.append((row, col - 1))
        if col < self.height - 1:
            neighbors.append((row, col + 1))
        return neighbors

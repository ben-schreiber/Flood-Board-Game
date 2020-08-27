from abc import ABC, abstractmethod


class SearchProblem(ABC):

    def __init__(self, board):
        self.board = board

    @abstractmethod
    def get_start_state(self):
        """Returns the start state of the board"""
        pass

    @abstractmethod
    def get_successors(self, state):
        """
        Returns the successors to the given state
        :param state: A Board object representing the current state of the game
        :return: A list of all possible successor Board states
        """
        pass

    @abstractmethod
    def is_goal_state(self, state):
        """Returns True iff the given Board object is completely colored in one color"""
        pass


class FillProblem(SearchProblem):

    def __init__(self, board):
        super().__init__(board)
        self.expanded = 0

    def get_start_state(self):
        return self.board

    def get_successors(self, state):
        moves = state.COLORS
        self.expanded += 1
        successors = []
        for move in moves:
            successor = state.copy()
            successor.apply_color_move(move)
            successors.append((successor, move, 1))
        return successors

    def is_goal_state(self, state):
        return state.full_board()


class FindConqueredProblem(SearchProblem):
    """
    Models a Board as a graph search problem.
    Each 'state' is a (row, col) tuple.
    Each successor is a neighboring tuple with the same color
    """

    def __init__(self, board, knight_mode=False):
        super().__init__(board)
        self.board = board
        self.knight_mode = knight_mode

    def get_start_state(self):
        """Returns the first node from which to start looking"""
        return self.board.starting_point

    def get_successors(self, state):
        """Returns a list of all neighbors of the given (row, col) tuple with the same color"""
        row, col = state
        if self.knight_mode:
            neighbors = self.board.find_knight_neighbors(row, col)
        else:
            neighbors = self.board.find_adjacent_neighbors(row, col)
        target_color = self.board.board[self.board.starting_point[0]][self.board.starting_point[1]]
        return [((row, col), None, None) for row, col in neighbors if self.board.board[row][col] == target_color]

    def is_goal_state(self, state):
        """Always returns False in order to allow the search algorithm to find all nodes"""
        return False

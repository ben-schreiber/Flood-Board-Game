class FillProblem:

    def __init__(self, board):
        self.board = board
        self.expanded = 0

    def get_start_state(self):
        """Returns the start state of the board"""
        return self.board

    def get_successors(self, state):
        """
        Returns the successors to the given state
        :param state: A Board object representing the current state of the game
        :return: A list of all possible successor Board states
        """
        moves = state.COLORS
        self.expanded += 1
        successors = []
        for move in moves:
            successor = state.copy()
            successor.apply_color_move(move)
            successors.append((successor, move, 1))
        return successors

    def is_goal_state(self, state):
        """Returns True iff the given Board object is completely colored in one color"""
        return state.full_board()

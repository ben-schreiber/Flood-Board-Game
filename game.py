from board import Board


class Game:

    GAME_OVER_LOSS_MSG = 'Game Over! You Lost!'
    GAME_OVER_WIN_MSG = 'Game Over! You Won!'
    INVALID_INPUT_MSG = 'Invalid input. Please enter one of the following colors: '
    KNIGHT_HOTKEY = Board.KNIGHT
    HINT_HOTKEY = 'H'
    HOTKEYS = [KNIGHT_HOTKEY, HINT_HOTKEY]

    def __init__(self, size=(18, 18), starting_point=(0, 0), move_allowance=21, num_jokers=0):
        self.board = Board(size, starting_point, num_jokers)
        self.move_num = 0
        self.move_allowance = int(move_allowance)

    def one_turn(self):
        """
        Manages one turn of the game:
            (1) Gets input from the user
            (3) Applies move
            (4) Prints resulting board
        """
        user_input = self.get_input()
        if user_input.upper() in Board.COLORS:  # If the user wants to color the board
            self.board.apply_color_move(user_input.upper())
            self.move_num += 1
        elif user_input in Game.HOTKEYS:  # If we have a special input
            if user_input == Game.KNIGHT_HOTKEY:
                self.board.toggle_mode()
            # elif user_input == Game.HINT_HOTKEY:

        print(self.board)

    @staticmethod
    def __invalid_input_msg():
        """
        Prints an error and usage message
        """
        print(Game.INVALID_INPUT_MSG)
        print(Board.COLORS)

    @staticmethod
    def __valid_input(input_letter):
        """Returns True iff the input is one of the colors available or a special hotkey"""
        return input_letter in Board.COLORS or input_letter in Game.HOTKEYS

    def run_user_game(self):
        """Manages the entire game logic"""
        print(self.board)  # Print the initial board
        while not self.game_over():
            self.one_turn()
        if self.move_num == self.move_allowance and not self.board.full_board():  # If the user used all moves
            print(Game.GAME_OVER_LOSS_MSG)
        else:
            print(Game.GAME_OVER_WIN_MSG)

    def get_input(self):
        """
        Gets an input from the user. If valid, returns that input; otherwise, ask for a new input
        :return: A valid input
        """
        while True:
            user_input = input(f"{self.move_num}/{self.move_allowance} Moves. Insert Color:\n")
            user_input = user_input.upper()
            if self.__valid_input(user_input):
                return user_input
            self.__invalid_input_msg()

    def game_over(self):
        """Returns True iff the board is colored entirely in the same color or all moves have been used"""
        return self.move_num == self.move_allowance or self.board.full_board()

    def run_search_agent_game(self, agent_name, heuristic_name):
        """
        Runs an AI search agent to obtain a sequence of actions and then applies them to the board
        :param agent_name: A string with the name of the search algorithm
        :param heuristic_name: A string with the name of the heuristic to use
        """
        from search_problems import FillProblem
        from search_algorithms import run_search_algorithm
        from time import time
        start = time()
        problem = FillProblem(self.board)
        moves = run_search_algorithm(agent_name, problem, heuristic_name == 'null')
        for move in moves:
            self.board.apply_color_move(move)
            self.move_num += 1
        print(f'Moves taken: {moves}')
        print(f'Number of nodes expanded: {problem.expanded}')
        print(f'Number of moves required: {len(moves)}')
        print(f'Solution found in {time() - start} seconds')


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser('Get the board size, starting point, move allowance, and number of jokers')
    parser.add_argument('-s', '--size', nargs=2, dest='size', type=int, default=(18, 18))
    parser.add_argument('-p', '--starting_point', nargs=2, dest='start_point', type=int, default=(0, 0))
    parser.add_argument('-m', '--move_allowance', dest='move_allow', type=int, default=21)
    parser.add_argument('-j', '--num_jokers', dest='jokers', type=int, default=0)
    parser.add_argument('--search_method', dest='search', type=str, default=None)
    parser.add_argument('--heuristic', dest='heuristic', type=str, default='true')
    args = parser.parse_args()

    game = Game(args.size, args.start_point, args.move_allow, args.jokers)

    if args.search:  # If we want to run this game with an AI agent and not allow a user input
        game.run_search_agent_game(args.search, args.heuristic)
    else:  # Regular game using user input
        game.run_user_game()

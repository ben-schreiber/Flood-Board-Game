from board import Board
from random import shuffle
from search_problems import FillProblem
from search_algorithms import run_search_algorithm
import pygame as pg


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
            print(self.board)
        elif user_input in Game.HOTKEYS:  # If we have a special input
            if user_input == Game.KNIGHT_HOTKEY:
                self.board.toggle_mode()
            elif user_input == Game.HINT_HOTKEY:
                print('Calculating your hint...')
                hint_letter = self.get_hint()
                print(f'The AI agent suggests you play: {hint_letter.upper()}')

    def get_hint(self):
        """Returns a single move as a hint to play"""
        shuffle(self.board.COLORS)
        problem = FillProblem(self.board)
        moves = run_search_algorithm('dfs', problem)
        return moves[0]

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


class GUI:

    INVALID_INPUT = None
    TITLE_MESSAGE = 'Color Fill Game'

    # Color fill numbers for RGB fill
    RED_FILL = (255, 0, 0)
    BLUE_FILL = (0, 0, 255)
    GREEN_FILL = (0, 255, 0)
    YELLOW_FILL = (255, 255, 0)

    def __init__(self, game: Game):
        self.game = game
        self.width = self.game.board.width
        self.height = self.game.board.height
        self.square_size = 30
        self.padding = 150
        self.playing = True

        pg.init()
        self.window = pg.display.set_mode((self.square_size * self.width + self.padding, self.square_size * self.height))
        self.clock = pg.time.Clock()
        pg.display.set_caption(GUI.TITLE_MESSAGE)

    def get_color(self, row, col):
        """Given the (row, col) pair, will return the RGB color fills according to the state of the board"""
        square = self.game.board.board[row][col]
        if square == self.game.board.BLUE:
            return GUI.BLUE_FILL
        elif square == self.game.board.GREEN:
            return GUI.GREEN_FILL
        elif square == self.game.board.RED:
            return GUI.RED_FILL
        elif square == self.game.board.YELLOW:
            return GUI.YELLOW_FILL

    def draw(self, game_over=False, won=False):
        """Draws the board on the window"""
        self.window.fill((255, 255, 255))

        for row in range(self.height):
            for col in range(self.width):
                color = self.get_color(row, col)
                pg.draw.rect(self.window, color, (col * self.square_size, row * self.square_size, self.square_size, self.square_size))

        font = pg.font.SysFont('comicsans', 28)

        moves_made_header = font.render('Moves Made:', 1, (0, 0, 0))
        self.window.blit(moves_made_header, (self.width * self.square_size + 5, 10))
        moves_made_text = font.render(f'{self.game.move_num} / {self.game.move_allowance}', 1, (0, 0, 0))
        self.window.blit(moves_made_text, (self.width * self.square_size + 5, 30))

        moves_remaining_header = font.render('Moves Left:', 1, (0, 0, 0))
        self.window.blit(moves_remaining_header, (self.width * self.square_size + 5, 70))
        moves_remaining_text = font.render(f'{self.game.move_allowance - self.game.move_num}', 1, (0, 0, 0))
        self.window.blit(moves_remaining_text, (self.width * self.square_size + 5, 90))

        if game_over:
            font = pg.font.SysFont('comicsans', 150, True)
            if won:
                text = font.render('You Won!', 1, (0, 0, 0))
            else:
                text = font.render('You Lost!', 1, (0, 0, 0))
            self.window.blit(text, (75, 100))

        pg.display.update()

    def get_user_input(self, event):
        """Receives a KEYDOWN event. If the input is valid, return the relevant character; else, return GUI.INVALID_INPUT"""
        if event.key == pg.K_b:
            return self.game.board.BLUE
        elif event.key == pg.K_y:
            return self.game.board.YELLOW
        elif event.key == pg.K_r:
            return self.game.board.RED
        elif event.key == pg.K_g:
            return self.game.board.GREEN
        elif event.key == pg.K_k:
            return self.game.board.KNIGHT
        else:
            return GUI.INVALID_INPUT

    def run_game_loop(self):
        """Manages the logic for one game"""
        pg.event.clear()
        self.draw()
        while self.playing:
            event = pg.event.wait()
            if event.type == pg.QUIT:  # Check to see if the user hit the 'Exit' button
                self.playing = False

            elif event.type == pg.KEYDOWN:
                user_input = self.get_user_input(event)
                if user_input is not GUI.INVALID_INPUT:  # If the user inputted a valid input
                    if user_input == self.game.KNIGHT_HOTKEY:
                        self.game.board.toggle_mode(print_message=False)
                    else:
                        self.game.board.apply_color_move(user_input)
                        self.game.move_num += 1

            if self.game.game_over():
                self.playing = False
                self.draw(game_over=True, won=self.game.board.full_board())
                pg.time.delay(2000)
            else:
                self.draw()

        pg.quit()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser('Get the board size, starting point, move allowance, and number of jokers')
    parser.add_argument('-s', '--size', nargs=2, dest='size', type=int, default=(18, 18))
    parser.add_argument('-p', '--starting_point', nargs=2, dest='start_point', type=int, default=(0, 0))
    parser.add_argument('-m', '--move_allowance', dest='move_allow', type=int, default=21)
    parser.add_argument('-j', '--num_jokers', dest='jokers', type=int, default=0)
    parser.add_argument('-g', '--gui', dest='gui', type=bool, default=True)
    parser.add_argument('--search_method', dest='search', type=str, default=None)
    parser.add_argument('--heuristic', dest='heuristic', type=str, default='true')
    args = parser.parse_args()

    game = Game(args.size, args.start_point, args.move_allow, args.jokers)

    if args.gui:
        gui = GUI(game)
        gui.run_game_loop()
    elif args.search:  # If we want to run this game with an AI agent and not allow a user input
        game.run_search_agent_game(args.search, args.heuristic)
    else:  # Regular game using user input
        game.run_user_game()

import time

from interface import Interface
from strategy import Strategy
from wordle import Wordle


def wait_ms(ms: int) -> None:
    '''waits for the specified number of milliseconds'''
    time.sleep(ms / 1000)


class Solver:

    def __init__(
        self,
        wordle: Wordle,
        interface: Interface,
        strategy: Strategy
    ) -> None:
        self.wordle = wordle
        self.interface = interface
        self.strategy = strategy

    def solve(self, guess_delay_ms: int = 0) -> int:
        '''solves the wordle'''
        # setup a new game
        self.wordle.new_game()
        self.interface.new_game(
            valid_words=self.wordle.get_valid_words(),
            max_guesses=self.wordle.get_max_guesses()
        )
        # start making guesses
        while not self.wordle.is_game_over():
            guess = self.strategy.best_guess(
                valid_words=self.wordle.get_valid_words(),
                remaining_words=self.wordle.get_remaining_words(),
                word_length=self.wordle.get_word_length(),
                remaining_guesses=self.wordle.get_remaining_guesses()
            )
            guess_result = self.interface.make_guess(guess)
            self.wordle.add_guess(guess, guess_result)
            wait_ms(guess_delay_ms)
        # return the game result
        actual_word = self.interface.get_actual_word()
        self.wordle.set_actual_word(actual_word)
        game_result = self.wordle.get_result()
        self.interface.wrap_up(game_result)
        return game_result

    def run(self, guess_delay_ms: int = 0, game_delay_ms: int = 0, max_solves: int = 100) -> None:
        '''continuously solves wordles while tracking the results'''
        solve_count = 0
        while solve_count < max_solves:
            self.solve(guess_delay_ms=guess_delay_ms)
            solve_count += 1
            wait_ms(game_delay_ms)

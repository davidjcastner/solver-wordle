import time

from game_result import GameResult
from interface import Interface
from restriction import Restriction
from strategy import Strategy
from tracker import Tracker


def wait_ms(ms: int) -> None:
    '''waits for the specified number of milliseconds'''
    time.sleep(ms / 1000)


class Solver:

    def __init__(
        self,
        valid_words: list[str],
        word_length: int,
        interface: Interface,
        strategy: Strategy,
        tracker: Tracker
    ) -> None:
        self.valid_words = valid_words
        self.word_length = word_length
        self.interface = interface
        self.strategy = strategy
        self.tracker = tracker

    def solve(self, guess_delay_ms: int = 0) -> GameResult:
        '''solves the wordle'''
        # setup a new game
        self.interface.new_game()
        restriction = Restriction(self.valid_words, self.word_length)
        # start making guesses
        while not self.interface.is_game_over():
            guess = self.strategy.best_guess(restriction, self.interface.previous_guesses())
            guess_result = self.interface.make_guess(guess)
            restriction.update(guess_result)
            wait_ms(guess_delay_ms)
        # return the result
        return self.interface.get_result()

    def run(self, guess_delay_ms: int = 0, game_delay_ms: int = 0, max_solves: int = 100) -> None:
        '''continuously solves wordles while tracking the results'''
        solve_count = 0
        while solve_count < max_solves:
            result = self.solve(guess_delay_ms=guess_delay_ms)
            self.tracker.add_result(result)
            solve_count += 1
            wait_ms(game_delay_ms)

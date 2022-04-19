from abc import ABC, abstractmethod

from game_result import GameResult
from guess_result import GuessResult


class Interface(ABC):
    '''abstract base class for interacting with a wordle game implementation'''

    @abstractmethod
    def new_game(self) -> None:
        '''performs any necessary setup for a new game'''

    @abstractmethod
    def is_game_over(self) -> bool:
        '''returns True if the game is over'''

    @abstractmethod
    def previous_guesses(self) -> list[str]:
        '''returns the previous guesses'''

    @abstractmethod
    def make_guess(self, guess: str) -> GuessResult:
        '''makes a guess and returns the result'''

    @abstractmethod
    def get_result(self) -> GameResult:
        '''returns the result of the game'''

from abc import ABC, abstractmethod
from src.logic.guess_result import GuessResult


class Interface(ABC):
    '''how the engine interacts withe the user'''

    @abstractmethod
    def get_max_guesses(self) -> int:
        '''returns the maximum number of guesses'''

    @abstractmethod
    def new_game(self, answer: str) -> None:
        '''starts a new game, if a answer is given it will be used'''

    @abstractmethod
    def make_guess(self, guess: str) -> GuessResult:
        '''makes a guess and returns the result'''

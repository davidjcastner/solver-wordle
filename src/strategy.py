from abc import ABC, abstractmethod

from restriction import Restriction


class Strategy(ABC):
    '''abstract class for a strategy for solving the wordle'''

    def get_strategy_name(self) -> str:
        '''returns the name of the strategy'''
        return self.__class__.__name__

    @abstractmethod
    def best_guess(self, restriction: Restriction, previous_guesses: list[str]) -> str:
        '''returns the best guess based on the strategy implementation'''

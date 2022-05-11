from abc import ABC, abstractmethod


class Strategy(ABC):
    '''determines the next guess for the wordle game'''

    @abstractmethod
    def is_deterministic(self) -> bool:
        '''
        returns True if the strategy is deterministic,
        a strategy that always returns the same answer
        based on the state of the wordle game is deterministic
        '''

    @abstractmethod
    def find_best_guess(self) -> str:
        '''finds the best guess for the wordle game'''

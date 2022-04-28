from abc import ABC, abstractmethod


class Strategy(ABC):
    '''a strategy for solving the wordle'''

    @abstractmethod
    def best_guess(
        self,
        valid_words: set[str],
        remaining_words: set[str],
        word_length: int,
        remaining_guesses: int
    ) -> str:
        '''returns the best guess based on the strategy implementation'''

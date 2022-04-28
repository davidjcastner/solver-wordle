from abc import ABC, abstractmethod

from restriction import Restriction


class Wordle(ABC):
    '''interface for wordle game data structures'''

    @abstractmethod
    def __init__(
        self,
        valid_words: set[str],
        max_guesses: int,
        restriction: Restriction
    ) -> None:
        '''initializes the wordle data structure'''

    @abstractmethod
    def get_valid_words(self) -> set[str]:
        '''returns the set of valid words'''

    @abstractmethod
    def get_max_guesses(self) -> int:
        '''returns the maximum number of guesses'''

    @abstractmethod
    def new_game(self) -> None:
        '''resets all data structures for a new game'''

    @abstractmethod
    def is_game_over(self) -> bool:
        '''returns True if the game is over'''

    @abstractmethod
    def get_remaining_words(self) -> set[str]:
        '''returns a set of remaining possible words'''

    @abstractmethod
    def get_word_length(self) -> int:
        '''returns the length of all words in the game'''

    @abstractmethod
    def get_remaining_guesses(self) -> int:
        '''returns the number of remaining guesses'''

    @abstractmethod
    def add_guess(self, guess: str, result: list[int]) -> None:
        '''adds a guess and its result to the game'''

    @abstractmethod
    def set_actual_word(self, actual_word: str) -> None:
        '''sets the word that the game is or was trying to guess'''

    @abstractmethod
    def get_result(self) -> int:
        '''returns the result of the game'''

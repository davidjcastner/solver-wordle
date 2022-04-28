from abc import ABC, abstractmethod


class Restriction(ABC):
    '''tracks all possible solutions'''

    @abstractmethod
    def __init__(self, valid_words: set[str]) -> None:
        '''initializes the restriction'''

    @abstractmethod
    def get_word_length(self) -> int:
        '''returns the length of all words in the restriction'''

    @abstractmethod
    def reset(self) -> None:
        '''resets any restrictions'''

    @abstractmethod
    def update(self, guess: str, guess_result: list[int]) -> None:
        '''updates possible solutions'''

    @abstractmethod
    def remove_possible_word(self, word: str) -> bool:
        '''removes a possible word, returns True if removed'''

    @abstractmethod
    def get_possible_words(self) -> set[str]:
        '''returns a list of possible words'''

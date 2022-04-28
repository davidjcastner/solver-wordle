from abc import ABC, abstractmethod


class Interface(ABC):
    '''interface for interacting with the user or application'''

    @abstractmethod
    def new_game(self, valid_words: set[set], max_guesses: int) -> None:
        '''performs any necessary setup for a new game'''

    @abstractmethod
    def make_guess(self, guess: str) -> list[int]:
        '''makes a guess and returns the result'''

    @abstractmethod
    def get_actual_word(self) -> str:
        '''returns the actual word that the game is or was trying to guess'''

    @abstractmethod
    def wrap_up(self, game_result: int) -> None:
        '''performs any necessary cleanup for the game'''

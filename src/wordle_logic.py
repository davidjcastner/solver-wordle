from game_result import GameResult
from guess_result import GuessResult
from restriction import Restriction
from wordle import Wordle


class WordleLogic(Wordle):
    '''interface for wordle game data structures'''

    def __init__(
        self,
        valid_words: set[str],
        max_guesses: int,
        restriction: Restriction
    ) -> None:
        '''initializes the wordle data structure'''
        self.valid_words = valid_words.copy()
        self.max_guesses = max_guesses
        self.restriction = restriction
        self.new_game()

    def get_valid_words(self) -> set[str]:
        '''returns the set of valid words'''
        return self.valid_words.copy()

    def get_max_guesses(self) -> int:
        '''returns the maximum number of guesses'''
        return self.max_guesses

    def new_game(self) -> None:
        '''resets all data structures for a new game'''
        self.guesses = []
        self.guess_results = []
        self.solved = False
        self.actual_word = None
        self.restriction.reset()

    def can_make_guess(self) -> bool:
        '''returns True if the game can make a guess'''
        return len(self.guesses) < self.max_guesses

    def is_game_over(self) -> bool:
        '''returns True if the game is over'''
        return self.solved or not self.can_make_guess()

    def get_remaining_words(self) -> set[str]:
        '''returns a set of remaining possible words'''
        return self.restriction.get_possible_words()

    def get_word_length(self) -> int:
        '''returns the length of all words in the game'''
        return self.restriction.get_word_length()

    def get_remaining_guesses(self) -> int:
        '''returns the number of remaining guesses'''
        return self.max_guesses - len(self.guesses)

    def add_guess(self, guess: str, result: list[int]) -> None:
        '''adds a guess and its result to the game'''
        self.guesses.append(guess)
        self.guess_results.append(result)
        self.restriction.update(guess, result)
        # check for solution
        if all(res == GuessResult.MATCH for res in result):
            self.actual_word = guess
            self.solved = True
        else:
            self.restriction.remove_possible_word(guess)

    def set_actual_word(self, actual_word: str) -> None:
        '''sets the word that the game is or was trying to guess'''
        self.actual_word = actual_word
        self.solved = actual_word in self.guesses

    def get_result(self) -> int:
        '''returns the result of the game'''
        return GameResult.WIN if self.solved else GameResult.LOSE

import random

from game_result import GameResult
from guess_result import GuessResult
from interface import Interface
from letter_result import LetterResult

RESULT_CHAR_LOOKUP = {
    LetterResult.INCORRECT: 'X',
    LetterResult.WRONG_POSITION: 'W',
    LetterResult.CORRECT: 'Y',
}


class CLIInterface(Interface):
    '''cli interface for wordle game'''

    def __init__(self, valid_words: list[str], max_guesses: int = 6) -> None:
        self.valid_words = valid_words.copy()
        self.max_guesses = max_guesses
        self.current_word = None
        self.guesses = []
        self.guess_results = []
        self.solved = False

    def line_guess(self, line: int) -> str:
        '''returns the guess for the given line'''
        return self.guesses[line] if line < len(self.guesses) else '_' * len(self.current_word)

    def line_result(self, line: int) -> str:
        '''returns the result of the given line'''
        if not line < len(self.guess_results):
            return ' ' * len(self.current_word)
        result = self.guess_results[line]
        result_chars = [RESULT_CHAR_LOOKUP[lr] for lr in result.letter_results]
        return ''.join(result_chars)

    def display_game(self) -> None:
        '''displays the current game state'''
        word_length = len(self.current_word)
        print('=' * (word_length * 4 + 6))
        for index in range(self.max_guesses):
            line_guess = self.line_guess(index)
            line_result = self.line_result(index)
            line = str(index) + ': ' + ' '.join(line_guess) + ' | ' + ' '.join(line_result)
            print(line)

    def new_game(self) -> None:
        '''performs any necessary setup for a new game'''
        self.current_word = random.choice(self.valid_words)
        self.guesses = []
        self.guess_results = []
        self.solved = False
        print(f'New game started with word {self.current_word}')
        self.display_game()

    def can_make_guess(self) -> bool:
        '''returns True if the game can make a guess'''
        return len(self.guesses) < self.max_guesses

    def is_game_over(self) -> bool:
        '''returns True if the game is over'''
        return self.solved or not self.can_make_guess()

    def previous_guesses(self) -> list[str]:
        '''returns the previous guesses'''
        return self.guesses.copy()

    def check_guess(self, guess: str) -> GuessResult:
        '''checks the guess and returns the result'''
        result = GuessResult(guess)
        # start with checking for correct letters
        unsolved_indexes = []
        for index, letter in enumerate(guess):
            if letter == self.current_word[index]:
                result.update(index, LetterResult.CORRECT)
            else:
                unsolved_indexes.append(index)
        # get the letter frequency skipping over correct letters
        letter_count = {}
        for index, letter in enumerate(self.current_word):
            if index not in unsolved_indexes:
                continue
            letter_count[letter] = letter_count.get(letter, 0) + 1
        # loop through remaining letters and check for matches
        for index, letter in enumerate(guess):
            if index not in unsolved_indexes:
                continue
            if letter in letter_count and letter_count[letter] > 0:
                result.update(index, LetterResult.WRONG_POSITION)
                letter_count[letter] -= 1
        # return the result
        return result

    def make_guess(self, guess: str) -> GuessResult:
        '''makes a guess and returns the result'''
        assert self.can_make_guess(), 'Cannot make guess'
        self.guesses.append(guess)
        result = self.check_guess(guess)
        self.guess_results.append(result)
        if guess == self.current_word:
            self.solved = True
        self.display_game()
        return result

    def get_result(self) -> GameResult:
        '''returns the result of the game'''
        return GameResult(self.current_word, self.guesses)

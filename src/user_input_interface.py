from game_result import GameResult
from guess_result import GuessResult
from interface import Interface
from letter_result import LetterResult

RESULT_CHAR_LOOKUP = {
    LetterResult.INCORRECT: 'X',
    LetterResult.WRONG_POSITION: 'W',
    LetterResult.CORRECT: 'Y',
}
CHAR_RESULT_LOOKUP = {
    'X': LetterResult.INCORRECT,
    'W': LetterResult.WRONG_POSITION,
    'Y': LetterResult.CORRECT,
}


class UserInputInterface(Interface):
    '''user input interface for wordle game'''

    def __init__(self, valid_words: list[str], max_guesses: int = 6) -> None:
        self.valid_words = valid_words.copy()
        self.max_guesses = max_guesses
        # self.current_word = None
        self.guesses = []
        self.guess_results = []
        self.solved = False

    def line_guess(self, line: int) -> str:
        '''returns the guess for the given line'''
        return self.guesses[line] if line < len(self.guesses) else '_' * 5

    def line_result(self, line: int) -> str:
        '''returns the result of the given line'''
        if not line < len(self.guess_results):
            return ' ' * 5
        result = self.guess_results[line]
        result_chars = [RESULT_CHAR_LOOKUP[lr] for lr in result.letter_results]
        return ''.join(result_chars)

    def display_game(self) -> None:
        '''displays the current game state'''
        word_length = 5
        print('=' * (word_length * 4 + 6))
        for index in range(self.max_guesses):
            line_guess = self.line_guess(index)
            line_result = self.line_result(index)
            line = str(index) + ': ' + ' '.join(line_guess) + ' | ' + ' '.join(line_result)
            print(line)

    def new_game(self) -> None:
        '''performs any necessary setup for a new game'''
        self.guesses = []
        self.guess_results = []
        self.solved = False
        print('Starting new game...')
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
        while True:
            try:
                user_input = input('Enter results for guess: ')
                assert len(user_input) == 5
                assert all(c in 'XWY' for c in user_input)
                break
            except AssertionError:
                print('Invalid input')
        result = GuessResult(guess)
        for index, c in enumerate(user_input):
            result.update(index, CHAR_RESULT_LOOKUP[c])
        return result

    def make_guess(self, guess: str) -> GuessResult:
        '''makes a guess and returns the result'''
        assert self.can_make_guess(), 'Cannot make guess'
        self.guesses.append(guess)
        print(f'Make the guess "{guess}"')
        result = self.check_guess(guess)
        self.guess_results.append(result)
        if result.is_solved():
            self.solved = True
        self.display_game()
        return result

    def get_result(self) -> GameResult:
        '''returns the result of the game'''
        actual_word = self.guesses[-1] if self.solved else input('Enter actual word: ')
        return GameResult(actual_word, self.guesses)

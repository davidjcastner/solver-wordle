import random

from game_result import GameResult
from guess_result import GuessResult
from interface import Interface
from utility import calculate_result

RESULT_CHAR_LOOKUP = {
    LetterResult.INCORRECT: 'X',
    GuessResult.MATCH: 'Y',
}


class CLIInterface(Interface):
    '''cli interface for wordle game'''

    def display_new_game(self) -> None:
        '''displays the new game message'''
        print('Starting a new game of Wordle...')

    def check_for_hide_word(self) -> bool:
        '''asks the user if the word should be hidden'''
        while True:
            answer = input('Should the word be hidden? (y/n) ')
            if answer.lower() == 'y':
                return True
            elif answer.lower() == 'n':
                return False
            else:
                print('Invalid answer. Try again.')

    def line_guess(self, line: int) -> str:
        '''returns the guess for the given line'''
        return self.guesses[line] if line < len(self.guesses) else '_' * len(self.actual_word)

    def line_result(self, line: int) -> str:
        '''returns the result of the given line'''
        if not line < len(self.guess_results):
            return ' ' * len(self.actual_word)
        result = self.guess_results[line]
        result_chars = [RESULT_CHAR_LOOKUP[res] for res in result]
        return ''.join(result_chars)

    def display_game_state(self) -> None:
        '''displays the current game state'''
        display = ''
        word_length = len(self.actual_word)
        display += '=' * (word_length * 4 + 6) + '\n'
        if not self.hide_word:
            display += 'Word: ' + self.actual_word + '\n'
            display += '=' * (word_length * 4 + 6) + '\n'
        for index in range(self.max_guesses):
            line_guess = self.line_guess(index)
            line_result = self.line_result(index)
            line = str(index + 1) + ': ' + ' '.join(line_guess) + ' | ' + ' '.join(line_result)
            display += line + '\n'
        print(display[:-1])

    def new_game(self, valid_words: set[set], max_guesses: int) -> None:
        '''performs any necessary setup for a new game'''
        self.actual_word = random.choice(list(valid_words))
        self.max_guesses = max_guesses
        self.guesses = []
        self.guess_results = []
        self.display_new_game()
        self.hide_word = self.check_for_hide_word()
        self.display_game_state()

    def make_guess(self, guess: str) -> list[int]:
        '''makes a guess and returns the result'''
        result = calculate_result(guess, self.actual_word)
        self.guesses.append(guess)
        self.guess_results.append(result)
        self.display_game_state()
        return result

    def get_actual_word(self) -> str:
        '''returns the actual word that the game is or was trying to guess'''
        return self.actual_word

    def wrap_up(self, game_result: int) -> None:
        '''performs any necessary cleanup for the game'''
        if game_result == GameResult.WIN:
            if len(self.guesses) <= 1:
                print('Lucky guess, you won on the first try!')
            else:
                print(f'Congrats, you won in {len(self.guesses)} guesses!')
        elif game_result == GameResult.LOSE:
            print('Oh no, you lost. Better luck next time!')

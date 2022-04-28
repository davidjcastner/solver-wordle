from strategy import Strategy

ALL_LETTERS = set('ABCDEFGHIJKLMNOPQRSTUVWXYZ')


class UserInputStrategy(Strategy):
    '''prompts the user for a guess as the strategy'''

    def is_valid_guess(
        self,
        guess: str,
        word_length: int,
        valid_words: set[str]
    ) -> bool:
        '''returns True if the guess is valid'''
        if len(guess) != word_length:
            return False
        if guess not in valid_words:
            return False
        if not all(letter in ALL_LETTERS for letter in guess):
            return False
        return True

    def best_guess(
        self,
        valid_words: set[str],
        remaining_words: set[str],
        word_length: int,
        remaining_guesses: int
    ) -> str:
        '''asks the user for a valid guess'''
        if remaining_guesses < 6:
            # display remaining words
            print('Remaining valid words:')
            remaining_word_list = list(remaining_words)
            remaining_word_list.sort()
            words_per_line = 120 // (word_length + 1)
            # split the remaining words into lines
            lines = []
            for line_start in range(0, len(remaining_word_list), words_per_line):
                line_end = min(line_start + words_per_line, len(remaining_word_list))
                lines.append(remaining_word_list[line_start:line_end])
            # print the lines
            for line in lines:
                print('  '.join(line))
        while True:
            guess = input('Guess a word: ').upper()
            if self.is_valid_guess(guess, word_length, valid_words):
                return guess
            print('Invalid guess')

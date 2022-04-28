import random

from strategy import Strategy


class RandomGuessStrategy(Strategy):
    '''randomly guesses a word'''

    def best_guess(
        self,
        valid_words: set[str],
        remaining_words: set[str],
        word_length: int,
        remaining_guesses: int
    ) -> str:
        '''returns a random guess'''
        guess = random.choice(list(remaining_words))
        # if len(remaining_words) <= 80:
        #     # display remaining words
        #     print('Remaining valid words:')
        #     remaining_word_list = list(remaining_words)
        #     remaining_word_list.sort()
        #     words_per_line = 120 // (word_length + 1)
        #     # split the remaining words into lines
        #     lines = []
        #     for line_start in range(0, len(remaining_word_list), words_per_line):
        #         line_end = min(line_start + words_per_line, len(remaining_word_list))
        #         lines.append(remaining_word_list[line_start:line_end])
        #     # print the lines
        #     for line in lines:
        #         print('  '.join(line))
        # print('Guess:', guess)
        return guess

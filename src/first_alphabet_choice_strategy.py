from strategy import Strategy


class FirstAlphabetChoiceStrategy(Strategy):
    '''chooses the first word when remaining words are sorted alphabetically'''

    def best_guess(
        self,
        valid_words: set[str],
        remaining_words: set[str],
        word_length: int,
        remaining_guesses: int
    ) -> str:
        '''returns the best guess based on the strategy implementation'''
        remaining_word_list = list(remaining_words)
        remaining_word_list.sort()
        return remaining_word_list[0]

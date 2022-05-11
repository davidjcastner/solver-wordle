from strategy import Strategy

LetterFrequency = dict[str, int]


class LetterFrequencyStrategy(Strategy):
    '''makes guesses based on the letter frequency of remaining words'''

    def get_letter_frequencies(self, words: set[str], word_length: int) -> list[LetterFrequency]:
        '''returns the letter frequencies of the remaining words'''
        frequencies = [{} for _ in range(word_length)]
        for word in words:
            for index, letter in enumerate(word):
                frequencies[index][letter] = frequencies[index].get(letter, 0) + 1
        return frequencies

    def get_word_score(self, word: str, letter_frequencies: list[LetterFrequency]) -> int:
        '''returns the score of the word based on the letter frequencies'''
        return sum(letter_frequencies[index].get(letter, 0) for index, letter in enumerate(word))

    def best_guess(
        self,
        valid_words: set[str],
        remaining_words: set[str],
        word_length: int,
        remaining_guesses: int
    ) -> str:
        '''returns the best guess based on the strategy implementation'''
        # get the letter frequency of the remaining words
        letter_frequencies = self.get_letter_frequencies(remaining_words, word_length)
        max_score = -1
        max_guess = None
        for word in remaining_words:
            score = self.get_word_score(word, letter_frequencies)
            if score > max_score:
                max_score = score
                max_guess = word
        return max_guess

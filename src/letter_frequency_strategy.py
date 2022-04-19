from restriction import Restriction
from strategy import Strategy

LetterFrequency = dict[str, int]


class LetterFrequencyStrategy(Strategy):
    '''makes guesses based on the letter frequency of remaining words'''

    def get_letter_frequencies(self, restriction: Restriction) -> list[LetterFrequency]:
        '''returns the letter frequencies of the remaining words'''
        frequencies = [{} for _ in range(restriction.word_length)]
        for word in restriction.possible_words:
            for index, letter in enumerate(word):
                frequencies[index][letter] = frequencies[index].get(letter, 0) + 1
        return frequencies

    def get_word_score(self, word: str, letter_frequencies: list[LetterFrequency]) -> int:
        '''returns the score of the word based on the letter frequencies'''
        return sum(letter_frequencies[index].get(letter, 0) for index, letter in enumerate(word))

    def best_guess(self, restriction: Restriction, previous_guesses: list[str]) -> str:
        '''returns the best guess based on the strategy implementation'''
        # get the letter frequency of the remaining words
        letter_frequencies = self.get_letter_frequencies(restriction)
        max_score = -1
        max_guess = None
        for word in restriction.possible_words:
            if word in previous_guesses:
                continue
            score = self.get_word_score(word, letter_frequencies)
            if score > max_score:
                max_score = score
                max_guess = word
        return max_guess

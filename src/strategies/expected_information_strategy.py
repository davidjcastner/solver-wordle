import math
import random

from strategy import Strategy
from utility import calculate_result


class ExpectedInformationStrategy(Strategy):
    '''calculates the expected information of each guess to find the best one'''

    def __init__(self) -> None:
        # a dictionary where the key is the guess and the value is another
        # dictionary where the key is actual word and the value is the result
        # the result is a tuple of ints
        self.cached_results = {}
        self.max_guess_size = 512

    def get_calculated_result(self, guess: str, actual_word: str) -> tuple:
        '''returns the result of a guess and an actual word'''
        if guess in self.cached_results and actual_word in self.cached_results[guess]:
            return self.cached_results[guess][actual_word]
        result = tuple(calculate_result(guess, actual_word))
        if guess not in self.cached_results:
            self.cached_results[guess] = {}
        self.cached_results[guess][actual_word] = result
        return result

    def expected_information(self, guess: str, remaining_words: set[str]) -> float:
        '''calculates the expected information of a guess'''
        # group remaining words by the result they would give based on the guess
        words_by_result = {}
        for word in remaining_words:
            result = self.get_calculated_result(guess, word)
            if result not in words_by_result:
                words_by_result[result] = []
            words_by_result[result].append(word)
        expected_information = 0.0
        for grouping in words_by_result.values():
            probability = len(grouping) / len(remaining_words)
            information = -math.log2(probability)
            expected_information += probability * information
        return expected_information

    def best_guess(
        self,
        valid_words: set[str],
        remaining_words: set[str],
        word_length: int,
        remaining_guesses: int
    ) -> str:
        '''returns the best guess based on the strategy implementation'''
        if len(valid_words) == len(remaining_words):
            return 'TARES'
        if len(remaining_words) == 1:
            return list(remaining_words)[0]
        # if len(remaining_words) > self.max_guess_size:
        #     # choose a random guess set from remaining words
        #     guess_set = random.sample(remaining_words, self.max_guess_size)
        # else:
        #     guess_set = remaining_words
        information_values = []
        most_information = -1.0
        best_guess = ''
        in_most_information = -1.0
        in_best_guess = ''
        for guess in valid_words:
            information = self.expected_information(guess, remaining_words)
            information_values.append((guess, information))
            if information > most_information:
                most_information = information
                best_guess = guess
            if guess in remaining_words and information > in_most_information:
                in_most_information = information
                in_best_guess = guess
        # sort information values and print top ten
        information_values.sort(key=lambda x: x[1], reverse=True)
        top_guess_amount = min(10, len(information_values))
        print(f'Top {top_guess_amount} guesses:')
        for guess, information in information_values[:top_guess_amount]:
            print(f'{guess} - {information}')
        if abs(in_most_information - most_information) < 0.1:
            return in_best_guess
        return best_guess

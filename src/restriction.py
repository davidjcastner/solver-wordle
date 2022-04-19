from guess_result import GuessResult
from letter_result import LetterResult

ALL_LETTERS = set('ABCDEFGHIJKLMNOPQRSTUVWXYZ')


class Restriction:
    '''tracks all possible solutions'''

    def __init__(self, valid_words: list[str], word_length: int) -> None:
        self.possible_words = valid_words.copy()
        self.word_length = word_length
        # possible_letters is tracking the letters that are still possible for each character in the word
        self.possible_letters = []
        for _ in range(self.word_length):
            self.possible_letters.append(ALL_LETTERS.copy())
        # letter count tracks the minimum and maximum count of letters needed the word
        self.min_letter_count = {}
        self.max_letter_count = {}

    def __repr__(self) -> str:
        '''returns a string representation of the possible solutions'''
        display = 'Possible Letters{\n'
        for idx, pos in enumerate(self.possible_letters):
            display += f'\t{idx}: {pos}\n'
        display += '}'
        display += '\nMin Letter Count{\n'
        for letter, min_count in self.min_letter_count.items():
            display += f'\t{letter}: {min_count}\n'
        display += '}'
        display += '\nMax Letter Count{\n'
        for letter, max_count in self.max_letter_count.items():
            display += f'\t{letter}: {max_count}\n'
        display += '}'
        return display

    def meets_possible_letters(self, word: str) -> bool:
        '''returns True if the word meets the possible letters'''
        for i, letter in enumerate(word):
            if letter not in self.possible_letters[i]:
                return False
        return True

    def meets_letter_count(self, word: str) -> bool:
        '''returns True if the word meets the letter count'''
        letter_count = {}
        for letter in word:
            letter_count[letter] = letter_count.get(letter, 0) + 1
        for letter, min_count in self.min_letter_count.items():
            if letter_count.get(letter, 0) < min_count:
                return False
        for letter, max_count in self.max_letter_count.items():
            if letter_count.get(letter, 0) > max_count:
                return False
        return True

    def is_valid_word(self, word: str) -> bool:
        '''returns True if the word is valid'''
        return self.meets_possible_letters(word) and self.meets_letter_count(word)

    def filter_solutions(self) -> None:
        '''updates the possible solutions based on possible letters and letter count'''
        new_possible_words = []
        for word in self.possible_words:
            if self.is_valid_word(word):
                new_possible_words.append(word)
        self.possible_words = new_possible_words

    def update(self, guess_result: GuessResult) -> None:
        '''updates the possible letters and letter count based on the guess result'''
        letters_seen = set()
        for index, letter in enumerate(guess_result.word):
            letters_seen.add(letter)
            letter_result = guess_result.letter_results[index]
            if letter_result == LetterResult.CORRECT:
                self.possible_letters[index] = set(letter)
            else:
                if letter in self.possible_letters[index]:
                    self.possible_letters[index].remove(letter)
        for letter in letters_seen:
            counts = guess_result.get_counts(letter)
            # combined count of correct and wrong position
            combined_count = counts[LetterResult.CORRECT] + counts[LetterResult.WRONG_POSITION]
            # if there the count for incorrect letters is zero,
            # then set the minimum count to sum of correct and wrong position letters
            if counts[LetterResult.INCORRECT] == 0:
                self.min_letter_count[letter] = counts[LetterResult.CORRECT] + counts[LetterResult.WRONG_POSITION]
            # if the count for correct and wrong position letters is zero,
            # then the letter is not in the word
            # remove the letter from all possible letters
            elif combined_count == 0:
                for possible_letters in self.possible_letters:
                    if letter in possible_letters:
                        possible_letters.remove(letter)
            # otherwise set the minimum and maximum to the count for correct and wrong position letters
            else:
                self.min_letter_count[letter] = combined_count
                self.max_letter_count[letter] = combined_count
            # if the count for wrong position is zero, then remove the letter from possible letters
            # where it is not correct
            if counts[LetterResult.WRONG_POSITION] == 0:
                for index, possible_letters in enumerate(self.possible_letters):
                    if guess_result.letter_results[index] != LetterResult.CORRECT:
                        if letter in possible_letters:
                            possible_letters.remove(letter)
        self.filter_solutions()
        # print(self)

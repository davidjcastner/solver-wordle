from guess_result import GuessResult
from restriction import Restriction

ALL_LETTERS = set('ABCDEFGHIJKLMNOPQRSTUVWXYZ')


class RestrictionLogic(Restriction):
    '''tracks all possible solutions'''

    def __init__(self, valid_words: set[str]) -> None:
        '''initializes the restriction logic'''
        self.validate_word_set(valid_words)
        self.valid_words = valid_words.copy()
        self.reset()

    def validate_word_set(self, words: set[str]) -> None:
        '''ensures that the words are valid'''
        # check to make sure the valid word set is at least one word
        if len(words) == 0:
            raise ValueError('valid_words must contain at least one word')
        for index, word in enumerate(words):
            if index == 0:
                self.word_length = len(word)
            else:
                if len(word) != self.word_length:
                    raise ValueError('all words must be the same length')

    def get_word_length(self) -> int:
        '''returns the length of all words in the restriction'''
        return self.word_length

    def reset(self) -> None:
        '''resets any restrictions'''
        self.possible_words: set[str] = self.valid_words.copy()
        # possible_letters is tracking the letters that are still possible for each character in the word
        self.possible_letters = []
        for _ in range(self.word_length):
            self.possible_letters.append(ALL_LETTERS.copy())
        # letter count tracks the minimum and maximum count of letters needed the word
        self.min_letter_count = {}
        self.max_letter_count = {}

    def remove_possible_word(self, word: str) -> bool:
        '''removes a possible word, returns True if removed'''
        if word in self.possible_words:
            self.possible_words.remove(word)
            return True
        return False

    def get_possible_words(self) -> list[str]:
        '''returns the possible words'''
        return self.possible_words.copy()

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
        new_possible_words = set()
        for word in self.possible_words:
            if self.is_valid_word(word):
                new_possible_words.add(word)
        self.possible_words = new_possible_words

    def set_possible_letter(self, position: int, letter: str) -> None:
        '''sets the letter as the only possible letter of that position'''
        self.possible_letters[position] = {letter}

    def remove_possible_letter(self, position: int, letter: str) -> None:
        '''removes the letter from the possible letters of that positions'''
        if letter in self.possible_letters[position]:
            self.possible_letters[position].remove(letter)

    def remove_possible_letter_all(self, letter: str) -> None:
        '''removes the letter as a possible letter for all positions'''
        for possible_letters in self.possible_letters:
            if letter in possible_letters:
                possible_letters.remove(letter)

    def get_result_counts(self, letter: str, guess: str, guess_result: list[int]) -> dict[int, int]:
        '''returns the letter count for each result'''
        counts = {result: 0 for result in GuessResult}
        for index, result in enumerate(guess_result):
            if letter == guess[index]:
                counts[result] += 1
        return counts

    def update(self, guess: str, guess_result: list[int]) -> None:
        '''updates the possible letters and letter count based on the guess result'''
        # track each letter seen in the guess
        # if the letter is correct, set the possible letters to the letter
        # otherwise, remove the letter from the possible letters
        letters_seen = set()
        for index, letter in enumerate(guess):
            letters_seen.add(letter)
            if guess_result[index] == GuessResult.MATCH:
                self.set_possible_letter(index, letter)
            else:
                self.remove_possible_letter(index, letter)
        # go through each letter in the guess
        # get a count of each type of guess result for the letter
        # use the counts to update the min and max letter counts for the letter
        for letter in letters_seen:
            counts = self.get_result_counts(letter, guess, guess_result)
            # combined count of correct and wrong position
            combined_count = counts[GuessResult.MATCH] + counts[GuessResult.CLOSE]
            # if there the count for incorrect letters is zero,
            # then set the minimum count to sum of correct and wrong position letters
            if counts[GuessResult.WRONG] == 0:
                self.min_letter_count[letter] = counts[GuessResult.MATCH] + counts[GuessResult.CLOSE]
            # if the count for correct and wrong position letters is zero,
            # then the letter is not in the word
            # remove the letter from all possible letters
            elif combined_count == 0:
                self.remove_possible_letter_all(letter)
            # otherwise set the minimum and maximum to the count for correct and wrong position letters
            else:
                self.min_letter_count[letter] = combined_count
                self.max_letter_count[letter] = combined_count
            # if the count for wrong position is zero, then remove the letter from possible letters
            # where it is not correct
            # if counts[GuessResult.CLOSE] == 0:
            #     for index, possible_letters in enumerate(self.possible_letters):
            #         if guess_result[index] != GuessResult.MATCH:
            #             if letter in possible_letters:
            #                 possible_letters.remove(letter)
        self.filter_solutions()


if __name__ == '__main__':
    valid_words = {'PANIC'}
    restriction = RestrictionLogic(valid_words.copy())
    guess = 'SORES'
    guess_result = [GuessResult.WRONG, GuessResult.WRONG, GuessResult.WRONG, GuessResult.WRONG, GuessResult.WRONG]
    restriction.update(guess, guess_result)
    assert restriction.get_possible_words() == {'PANIC'}
    guess = 'PALAY'
    guess_result = [GuessResult.MATCH, GuessResult.MATCH, GuessResult.WRONG, GuessResult.WRONG, GuessResult.WRONG]
    restriction.update(guess, guess_result)
    assert restriction.get_possible_words() == {'PANIC'}
    guess = 'PINCH'
    guess_result = [GuessResult.MATCH, GuessResult.CLOSE, GuessResult.MATCH, GuessResult.CLOSE, GuessResult.WRONG]
    restriction.update(guess, guess_result)
    assert restriction.get_possible_words() == {'PANIC'}

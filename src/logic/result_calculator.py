from src.enums.letter_result import LetterResult
from src.logic.guess_result import GuessResult

DecodedKey = tuple[str, str]  # (guess, answer)
DecodedValue = GuessResult
EncodedKey = str
EncodedValue = int

VALUE_LOOKUP = {
    LetterResult.UNSET: 0,
    LetterResult.WRONG: 1,
    LetterResult.CLOSE: 2,
    LetterResult.MATCH: 3
}
RESULT_LOOKUP = {value: key for key, value in VALUE_LOOKUP.items()}


def _encode_key(key: DecodedKey) -> EncodedKey:
    '''encodes the key as a concatenation of the two words'''
    guess, answer = key
    return guess + answer


def _encode_value(value: DecodedValue) -> EncodedValue:
    '''encodes the value, each result is a bit flag'''
    encoded_value = 0
    for result in value:
        encoded_value = encoded_value << 2
        encoded_value += result.value
    return encoded_value


def _decode_key(key: EncodedKey) -> DecodedKey:
    '''decodes the key by splitting the string into two words'''
    word_length = len(key) // 2
    return (key[:word_length], key[word_length:])


def _decode_value(value: EncodedValue) -> DecodedValue:
    '''decodes the value by iterating over the bits'''
    decoded_value = GuessResult()
    temp_value = value
    remainder = temp_value % 4
    # stop at first 0
    while remainder != 0:
        decoded_value.insert(0, RESULT_LOOKUP[remainder])
        temp_value = temp_value >> 2
        remainder = temp_value % 4
    return decoded_value


class ResultCalculator:
    '''calculates the result of a wordle guess based on the answer,
    stores results in an efficient cache for quick lookup'''

    def __init__(self) -> None:
        self._cache: dict[EncodedKey, EncodedValue] = {}

    def _calc(self, guess: str, answer: str) -> GuessResult:
        '''actually performs the calculation'''
        # start with the default of all letters being wrong
        result = GuessResult(LetterResult.WRONG for _ in answer)
        # start with checking for correct letters
        # while tracking unsolved positions
        unsolved_indexes = []
        for index, (guess_letter, answer_letter) in enumerate(zip(guess, answer)):
            if guess_letter == answer_letter:
                result[index] = LetterResult.MATCH
            else:
                unsolved_indexes.append(index)
        # get the letter frequency of the answer skipping over correct letters
        # example: 'hello' -> {'h': 1, 'e': 1, 'l': 2, 'o': 1} (w/o any correct)
        letter_count = {}
        for index in unsolved_indexes:
            letter = answer[index]
            letter_count[letter] = letter_count.get(letter, 0) + 1
        # loop through remaining letters in the guess and check for close matches
        # decrement the letter count each time
        # this ensures only the correct amount of letters are set to wrong position
        # without going over, and the only the first ones will be checked
        for index in unsolved_indexes:
            letter = guess[index]
            if letter in letter_count and letter_count[letter] > 0:
                result[index] = LetterResult.CLOSE
                letter_count[letter] -= 1
        # return the result
        return result

    def calculate(self, guess: str, answer: str) -> GuessResult:
        '''calculates the result of a wordle guess while checking cache'''
        key = _encode_key((guess, answer))
        if key in self._cache:
            return _decode_value(self._cache[key])
        result = self._calc(guess, answer)
        self._cache[key] = _encode_value(result)
        return result

    def pre_compute(self, guesses: set[str], answers: set[str]) -> None:
        '''precomputes the results of all guesses and answers'''
        for guess in guesses:
            for answer in answers:
                result = self.calculate(guess, answer)
                key = _encode_key((guess, answer))
                self._cache[key] = _encode_value(result)


# if __name__ == '__main__':
#     # test the result calculator
#     calculator = ResultCalculator()
#     guesses = {'hello', 'world', 'trace', 'track', 'train'}
#     answers = {'hello', 'world', 'trace'}
#     calculator.pre_compute(guesses, answers)
#     # print(calculator._cache)
#     for key, value in calculator._cache.items():
#         print(key, _decode_value(value))

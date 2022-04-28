from enum import Enum


class GuessResult(Enum):
    '''enum for the result of a guessed letter'''
    WRONG = 0  # letter is not in the actual word
    CLOSE = 1  # letter appears in the word, but not at the correct position
    MATCH = 2  # letter appears in the word at the correct position

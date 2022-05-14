from enum import Enum


class LetterResult(Enum):
    '''enum for the result of a guessed letter'''
    UNSET = 0  # not information is known about the letter
    WRONG = 1  # letter is not in the answer
    CLOSE = 2  # letter appears in the answer, but not at the correct position
    MATCH = 3  # letter appears in the answer and is at the correct position

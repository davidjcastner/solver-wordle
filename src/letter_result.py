from enum import Enum


class LetterResult(Enum):
    '''feedback for an individual letter'''

    INCORRECT = 'incorrect'
    WRONG_POSITION = 'wrong position'
    CORRECT = 'correct'

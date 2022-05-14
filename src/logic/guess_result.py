from src.enums.letter_result import LetterResult


class GuessResult(list):
    '''represents the result of a guess'''

    def is_answer(self) -> bool:
        '''returns True if the guess is the answer'''
        return all(letter == LetterResult.MATCH for letter in self)

from letter_result import LetterResult


class GuessResult:
    '''tracks the result of a guess, default is incorrect'''

    def __init__(self, word: str) -> None:
        self.word = word
        self.letter_results = [LetterResult.INCORRECT for _ in range(len(word))]

    def update(self, index: int, letter_result: LetterResult) -> None:
        '''updates the letter result at the specified index'''
        assert index >= 0 and index < len(self.word), 'index out of range'
        self.letter_results[index] = letter_result

    def get_counts(self, letter: str) -> dict[LetterResult, int]:
        '''returns the count of each letter result for the specified letter'''
        counts = {LetterResult.INCORRECT: 0, LetterResult.CORRECT: 0, LetterResult.WRONG_POSITION: 0}
        for index, char in enumerate(self.word):
            if char == letter:
                letter_result = self.letter_results[index]
                counts[letter_result] += 1
        return counts

    def is_solved(self) -> bool:
        '''returns True if all letters are correct'''
        for letter_result in self.letter_results:
            if letter_result != LetterResult.CORRECT:
                return False
        return True

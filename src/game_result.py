class GameResult:
    '''represents the result of a game'''

    def __init__(self, actual_word: str, guesses: list[str]) -> None:
        self.actual_word = actual_word
        self.guesses = guesses

    def is_solved(self) -> bool:
        '''returns True if the game is solved'''
        return self.actual_word in self.guesses

    def total_guesses(self) -> int:
        '''returns the total number of guesses'''
        return len(self.guesses)

    def to_dict(self) -> dict:
        '''returns a dictionary representation of the result'''
        return {
            'word': self.actual_word,
            'guesses': self.guesses,
            'solved': self.is_solved(),
            'total_guesses': self.total_guesses()
        }

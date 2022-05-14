from src.abstracts.interface import Interface
from src.logic.guess_result import GuessResult


class CliInterface(Interface):
    '''how the engine interacts withe the user'''

    def get_max_guesses(self) -> int:
        '''returns the maximum number of guesses'''
        return 0

    def new_game(self, answer: str) -> None:
        '''starts a new game, if a answer is given it will be used'''

    def make_guess(self, guess: str) -> GuessResult:
        '''makes a guess and returns the result'''
        return GuessResult()

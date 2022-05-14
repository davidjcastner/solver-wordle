from src.abstracts.strategy import Strategy
from src.abstracts.interface import Interface


class Engine:
    '''runs a wordle game'''

    def __init__(self, interface: Interface, allowed_guesses: set[str], allowed_answers: set[str]) -> None:
        self._interface = interface
        self._allowed_guesses = allowed_guesses
        self._allowed_answers = allowed_answers
        self._reset()

    def get_allowed_answers(self) -> set[str]:
        '''returns the set of allowed answers'''
        return self._allowed_answers

    def _reset(self) -> None:
        '''resets any state the engine may have for a new game'''
        self._guess_count = 0
        self._is_win = False

    def _is_game_over(self) -> bool:
        '''returns True if the game is over'''
        return self._is_win or self._guess_count == self._interface.get_max_guesses()

    def _get_score(self) -> int:
        '''returns the score which is equal to the number of guesses,
        or zero if the answer was not guess'''
        return self._guess_count if self._is_win else 0

    def play_game(self, strategy: Strategy, answer: str = None) -> int:
        '''plays a game using the given strategy'''
        self._reset()
        self._interface.new_game(answer)
        while not self._is_game_over():
            guess = strategy.find_best_guess()
            result = self._interface.make_guess(guess)
            self._guess_count += 1
            self._is_win = result.is_answer()
        return self._get_score()

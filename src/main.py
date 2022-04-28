from interface import Interface
from restriction import Restriction
from solver import Solver
from strategy import Strategy
from word_set import WordSet
from wordle import Wordle

# implementations to use
from restriction_logic import RestrictionLogic as RestrictionImplementation
from wordle_logic import WordleLogic as WordleImplementation
from web_app_interface import WebAppInterface as InterfaceImplementation
from random_guess_strategy import RandomGuessStrategy as StrategyImplementation


WORD_FILE = './data/valid_words_web.txt'
WORD_LENGTH = 5
MAX_GUESSES = 6


def main() -> None:
    '''main function'''
    valid_words = WordSet(WORD_FILE, WORD_LENGTH).to_set()
    restriction: Restriction = RestrictionImplementation(valid_words)
    wordle: Wordle = WordleImplementation(valid_words, MAX_GUESSES, restriction)
    interface: Interface = InterfaceImplementation()
    strategy: Strategy = StrategyImplementation()
    solver = Solver(
        wordle=wordle,
        interface=interface,
        strategy=strategy
    )
    solver.run(guess_delay_ms=0, game_delay_ms=0, max_solves=20)


if __name__ == '__main__':
    main()

# from cli_interface import CLIInterface
from letter_frequency_strategy import LetterFrequencyStrategy
from solver import Solver
from tracker import Tracker
from user_input_interface import UserInputInterface
from word_list import WordList

WORD_FILE = './data/valid_words.txt'
WORD_LENGTH = 5
TRACKER_FILE = './data/tracker.json'


def main() -> None:
    '''main function'''
    valid_words = WordList(WORD_FILE, WORD_LENGTH).to_list()
    strategy = LetterFrequencyStrategy()
    interface = UserInputInterface(valid_words=valid_words)
    tracker = Tracker(
        results_file=TRACKER_FILE,
        strategy_name=strategy.get_strategy_name()
    )
    solver = Solver(
        valid_words=valid_words,
        word_length=WORD_LENGTH,
        interface=interface,
        strategy=strategy,
        tracker=tracker
    )
    solver.run(guess_delay_ms=1000, game_delay_ms=3000, max_solves=10)


if __name__ == '__main__':
    main()

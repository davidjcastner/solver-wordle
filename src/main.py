from src.abstracts.engine import Engine
from src.strategy_evaluator import strategy_evaluator


def engine_factory() -> Engine:
    '''engine factory'''
    return Engine()


def main() -> None:
    '''main function'''
    # create a list of strategies
    strategies = []
    # create the engine and evaluator
    engine = engine_factory()
    # rune the evaluator
    strategy_evaluator(engine, strategies, 'results.txt')


if __name__ == '__main__':
    main()

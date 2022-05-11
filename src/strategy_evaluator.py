from src.abstracts.engine import Engine
from src.abstracts.strategy import Strategy


def strategy_evaluator(
    engine: Engine,
    strategies: list[Strategy],
    result_file: str,
    trials: int = 16
) -> None:
    '''does an exhaustive evaluation of a strategy
    by figuring out the expected score for all possible answers'''
    print('Evaluating strategies:')
    for strategy in strategies:
        strategy_name = strategy.__class__.__name__
        is_deterministic = strategy.is_deterministic()
        print(f'{strategy_name} ({is_deterministic})')
        total = 0.0
        for answer in engine.get_allowed_answers():
            engine.new_game(answer)
            if is_deterministic:
                total += engine.play_game(strategy)
            else:
                sub_total = 0
                for _ in range(trials):
                    sub_total += engine.play_game(strategy)
                total += sub_total / trials
        average_score = total / len(engine.get_allowed_answers())
        print(f'Average score: {average_score}')

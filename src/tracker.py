import json
import os

from game_result import GameResult


class Tracker:
    '''tracks all results of a strategy'''

    def __init__(self, results_file: str, strategy_name: str) -> None:
        self.results_file = results_file
        self.strategy_name = strategy_name
        self.results = {}
        self.load_results()
        self.initialize_strategy()

    def initialize_strategy(self) -> None:
        '''initializes the strategy'''
        if self.strategy_name not in self.results:
            self.results[self.strategy_name] = {
                'wins': 0,
                'losses': 0,
                'total_games': 0,
                'average_guesses': 0,
                'trials': []
            }

    def load_results(self) -> None:
        '''loads the results from the file'''
        if os.path.isfile(self.results_file):
            with open(self.results_file, 'r') as f:
                for line in f:
                    line = line.strip()

    def save_results(self) -> None:
        '''saves the results to the file'''
        with open(self.results_file, 'w') as f:
            f.write(json.dumps(self.results, indent=4))

    def calculate_average_guesses(self) -> None:
        '''calculates the average guesses'''
        if self.results[self.strategy_name]['wins'] == 0:
            self.results[self.strategy_name]['average_guesses'] = 0
            return
        total_guesses = 0
        for result in self.results[self.strategy_name]['trials']:
            if result['solved']:
                total_guesses += result['total_guesses']
        average = total_guesses / self.results[self.strategy_name]['wins']
        self.results[self.strategy_name]['average_guesses'] = average

    def add_result(self, result: GameResult) -> None:
        '''adds a result to the tracker'''
        solved = result.is_solved()
        self.results[self.strategy_name]['total_games'] += 1
        if solved:
            self.results[self.strategy_name]['wins'] += 1
        else:
            self.results[self.strategy_name]['losses'] += 1
        self.results[self.strategy_name]['trials'].append(result.to_dict())
        if solved:
            self.calculate_average_guesses()
        self.save_results()

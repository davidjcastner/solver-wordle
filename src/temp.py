from utility import calculate_result


def main():
    allowed_guesses_file = './data/allowed_guesses.txt'
    possible_words_file = './data/possible_words.txt'

    with open(allowed_guesses_file, 'r') as f:
        allowed_guesses = f.read().splitlines()
    with open(possible_words_file, 'r') as f:
        possible_words = f.read().splitlines()

    # compute all possible results
    results = {}
    for guess in {'trace'}:
        results[guess] = {}
        for word in possible_words:
            result = calculate_result(guess, word)
            result = tuple(res.value for res in result)
            if result not in results[guess]:
                results[guess][result] = set()
            results[guess][result].add(word)

    # find the guess with the most results
    max_results = -1
    max_guess = None
    for guess, result_lkp in results.items():
        if len(result_lkp) > max_results:
            max_results = len(result_lkp)
            max_guess = guess

    # print the guess with the most results
    print(max_guess, max_results)
    # print(results[max_guess])


if __name__ == '__main__':
    main()

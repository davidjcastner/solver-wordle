from guess_result import GuessResult


def calculate_result(guess: str, actual_word: str) -> list[int]:
    '''calculates the result of a guess if the actual word is known'''
    # start with the default of all letters being wrong
    result = [GuessResult.WRONG for _ in range(len(actual_word))]
    # start with checking for correct letters
    # while tracking unsolved positions
    unsolved_indexes = []
    for index, letter in enumerate(guess):
        if letter == actual_word[index]:
            result[index] = GuessResult.MATCH
        else:
            unsolved_indexes.append(index)
    # get the letter frequency skipping over correct letters
    letter_count = {}
    for index, letter in enumerate(actual_word):
        if index not in unsolved_indexes:
            continue
        letter_count[letter] = letter_count.get(letter, 0) + 1
    # loop through remaining letters and check for matches
    # decrement the letter count each time
    # this ensures only the correct amount of letters are set to wrong position
    # without going over, and the only the first ones will be checked
    for index, letter in enumerate(guess):
        if index not in unsolved_indexes:
            continue
        if letter in letter_count and letter_count[letter] > 0:
            result[index] = GuessResult.CLOSE
            letter_count[letter] -= 1
    # return the result
    return result

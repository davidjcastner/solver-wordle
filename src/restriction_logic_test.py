import pytest

from guess_result import GuessResult
from restriction_logic import RestrictionLogic as Restriction


class TestRestrictionLogic:

    def test_initialization(self) -> None:
        valid_words = {'CAT', 'DOG', 'RAT'}
        restriction = Restriction(valid_words.copy())
        assert restriction.get_possible_words() == valid_words

    def test_initialization_with_no_valid_words(self) -> None:
        with pytest.raises(ValueError):
            Restriction([])

    def test_initialization_negative(self) -> None:
        valid_words = {'CAT', 'DOG', 'RAT'}
        restriction = Restriction(valid_words.copy())
        assert 'FOX' not in restriction.get_possible_words()

    def test_update_correct_letter(self) -> None:
        valid_words = {'CAT', 'DOG', 'RAT'}
        guess = 'XAX'
        guess_result = [GuessResult.WRONG, GuessResult.MATCH, GuessResult.WRONG]
        restriction = Restriction(valid_words.copy())
        restriction.update(guess, guess_result)
        assert restriction.get_possible_words() == {'CAT', 'RAT'}
        valid_words = {'CAT', 'DOG', 'RAT'}
        guess = 'XAT'
        guess_result = [GuessResult.WRONG, GuessResult.MATCH, GuessResult.MATCH]
        restriction = Restriction(valid_words.copy())
        restriction.update(guess, guess_result)
        assert restriction.get_possible_words() == {'CAT', 'RAT'}

    def test_update_wrong_position(self) -> None:
        valid_words = {'CAT', 'DOG', 'RAT'}
        guess = 'XXC'
        guess_result = [GuessResult.WRONG, GuessResult.WRONG, GuessResult.CLOSE]
        restriction = Restriction(valid_words.copy())
        restriction.update(guess, guess_result)
        assert restriction.get_possible_words() == {'CAT'}
        valid_words = {'CAT', 'DOG', 'RAT'}
        guess = 'XXA'
        guess_result = [GuessResult.WRONG, GuessResult.WRONG, GuessResult.CLOSE]
        restriction = Restriction(valid_words.copy())
        restriction.update(guess, guess_result)
        assert restriction.get_possible_words() == {'CAT', 'RAT'}

    def test_reset(self) -> None:
        valid_words = {'CAT', 'DOG', 'RAT'}
        guess = 'XAT'
        guess_result = [GuessResult.WRONG, GuessResult.MATCH, GuessResult.MATCH]
        restriction = Restriction(valid_words.copy())
        restriction.update(guess, guess_result)
        assert restriction.get_possible_words() == {'CAT', 'RAT'}
        restriction.reset()
        assert restriction.get_possible_words() == valid_words

    def test_remove_possible_word(self) -> None:
        valid_words = {'CAT', 'DOG', 'RAT'}
        restriction = Restriction(valid_words.copy())
        restriction.remove_possible_word('CAT')
        assert restriction.get_possible_words() == {'DOG', 'RAT'}
        restriction.remove_possible_word('RAT')
        assert restriction.get_possible_words() == {'DOG'}
        restriction.remove_possible_word('DOG')
        assert restriction.get_possible_words() == set()

    def test_remove_possible_word_not_in_set(self) -> None:
        valid_words = {'CAT', 'DOG', 'RAT'}
        restriction = Restriction(valid_words.copy())
        restriction.remove_possible_word('FOX')
        assert restriction.get_possible_words() == valid_words

    def test_remove_possible_word_return_value(self) -> None:
        valid_words = {'CAT', 'DOG', 'RAT'}
        restriction = Restriction(valid_words.copy())
        assert restriction.remove_possible_word('CAT') is True
        assert restriction.remove_possible_word('CAT') is False
        assert restriction.remove_possible_word('FOX') is False

    def test_bug_case_001(self) -> None:
        '''serks was removed incorrectly with the guesses of sawed or stole'''
        valid_words = {'SERKS'}
        restriction = Restriction(valid_words.copy())
        guess = 'SAWED'
        guess_result = [GuessResult.MATCH, GuessResult.WRONG, GuessResult.WRONG, GuessResult.CLOSE, GuessResult.WRONG]
        restriction.update(guess, guess_result)
        assert restriction.get_possible_words() == {'SERKS'}
        guess = 'STOLE'
        guess_result = [GuessResult.MATCH, GuessResult.WRONG, GuessResult.WRONG, GuessResult.WRONG, GuessResult.CLOSE]
        restriction.update(guess, guess_result)
        assert restriction.get_possible_words() == {'SERKS'}

    def test_bug_case_002(self) -> None:
        '''panic was removed incorrectly with the guesses of sores, palay, pinch'''
        valid_words = {'PANIC'}
        restriction = Restriction(valid_words.copy())
        guess = 'SORES'
        guess_result = [GuessResult.WRONG, GuessResult.WRONG, GuessResult.WRONG, GuessResult.WRONG, GuessResult.WRONG]
        restriction.update(guess, guess_result)
        assert restriction.get_possible_words() == {'PANIC'}
        guess = 'PALAY'
        guess_result = [GuessResult.MATCH, GuessResult.MATCH, GuessResult.WRONG, GuessResult.WRONG, GuessResult.WRONG]
        restriction.update(guess, guess_result)
        assert restriction.get_possible_words() == {'PANIC'}
        guess = 'PINCH'
        guess_result = [GuessResult.MATCH, GuessResult.CLOSE, GuessResult.MATCH, GuessResult.CLOSE, GuessResult.WRONG]
        restriction.update(guess, guess_result)
        assert restriction.get_possible_words() == {'PANIC'}

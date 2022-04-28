from selenium import webdriver
import time


from guess_result import GuessResult
from interface import Interface


CHROME_DRIVER_PATH = './bin/chromedriver.exe'
GAME_URL = 'https://wordlegame.org/'


def wait_to_poll() -> None:
    '''waits a little bit for next poll'''
    time.sleep(0.2)


class WebAppInterface(Interface):
    '''plays the wordle game on the site https://wordlegame.org/'''

    def __init__(self) -> None:
        self.driver = webdriver.Chrome(CHROME_DRIVER_PATH)
        self.driver.get(GAME_URL)
        self.wait_for_website_to_load()
        time.sleep(0.5)

    def wait_for_website_to_load(self) -> None:
        '''waits for the website to load'''
        while True:
            try:
                # get the element with id root
                root = self.driver.find_element_by_id('root')
                # get the element with class of alert
                # make sure the text of this element is blank
                alert = root.find_element_by_class_name('alert')
                if alert.text == '':
                    break
            except Exception as e:
                # print out first line of the exception
                print('waiting for website to load...')
                print(e)
            wait_to_poll()

    def new_game(self, valid_words: set[set], max_guesses: int) -> None:
        '''performs any necessary setup for a new game'''
        self.guesses = []
        self.actual_word = None

    def send_guess(self, guess: str) -> None:
        '''sends a guess to the game'''
        print(f'making the guess "{guess}"...')
        root = self.driver.find_element_by_id('root')
        buttons = root.find_elements_by_class_name('Game-keyboard-button')
        keyboard = {}
        for button in buttons:
            keyboard[button.text] = button
        for letter in guess:
            keyboard[letter].click()
            time.sleep(0.01)
        keyboard['Enter'].click()

    def wait_for_result(self, guess_count: int) -> None:
        '''waits for the result of the guess'''
        root = self.driver.find_element_by_id('root')
        game_rows = root.find_element_by_class_name('game_rows')
        row = game_rows.find_elements_by_class_name('Row')[guess_count]
        letters = row.find_elements_by_class_name('Row-letter')
        while True:
            if all(any(
                cls_name in letter.get_attribute('class') for cls_name in [
                    'letter-absent', 'letter-elsewhere', 'letter-correct'
                ]
            ) for letter in letters):
                break
            wait_to_poll()

    def get_result(self, guess_count: int) -> list[int]:
        '''gets the result of the guess'''
        self.wait_for_result(guess_count)
        root = self.driver.find_element_by_id('root')
        game_rows = root.find_element_by_class_name('game_rows')
        row = game_rows.find_elements_by_class_name('Row')[guess_count]
        letters = row.find_elements_by_class_name('Row-letter')
        result = []
        for letter in letters:
            if 'letter-correct' in letter.get_attribute('class'):
                result.append(GuessResult.MATCH)
            elif 'letter-elsewhere' in letter.get_attribute('class'):
                result.append(GuessResult.CLOSE)
            else:
                result.append(GuessResult.WRONG)
        return result

    def make_guess(self, guess: str) -> list[int]:
        '''makes a guess and returns the result'''
        self.send_guess(guess)
        # get the result
        result = self.get_result(len(self.guesses))
        self.guesses.append(guess)
        if all(res == GuessResult.MATCH for res in result):
            self.actual_word = guess
        return result

    def wait_for_modal_finish(self) -> None:
        '''wait for modal finish to appear'''
        root = self.driver.find_element_by_id('root')
        while True:
            try:
                # check if modal_finish has class active
                modals = root.find_elements_by_class_name('modal_finish')
                if any('active' in modal.get_attribute('class') for modal in modals):
                    break
            except Exception:
                # do nothing
                pass
            wait_to_poll()

    def get_actual_word(self) -> str:
        '''returns the actual word that the game is or was trying to guess'''
        if self.actual_word is not None:
            return self.actual_word
        self.wait_for_modal_finish()
        root = self.driver.find_element_by_id('root')
        modals = root.find_elements_by_class_name('modal_finish')
        actual_modal = None
        for modal in modals:
            if 'active' in modal.get_attribute('class'):
                actual_modal = modal
                break
        word = actual_modal.find_element_by_class_name('word')
        word = word.find_element_by_tag_name('span')
        self.actual_word = word.text
        print(f'actual word: {self.actual_word}')
        return self.actual_word

    def wrap_up(self, game_result: int) -> None:
        '''performs any necessary cleanup for the game'''
        self.wait_for_modal_finish()
        print(f'game result: {game_result}')
        root = self.driver.find_element_by_id('root')
        modals = root.find_elements_by_class_name('modal_finish')
        actual_modal = None
        for modal in modals:
            if 'active' in modal.get_attribute('class'):
                actual_modal = modal
                break
        restart_btn = actual_modal.find_element_by_class_name('restart_btn')
        restart_btn = restart_btn.find_element_by_tag_name('button')
        # click the button
        restart_btn.click()
        # wait a little bit
        time.sleep(0.5)

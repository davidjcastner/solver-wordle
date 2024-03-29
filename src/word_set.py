class WordSet:

    def __init__(self, file_name: str, word_length: int = 5) -> None:
        self.file_name = file_name
        self.word_length = word_length
        self.words: set[str] = set()
        self.load_words()
        self.validate()

    def load_words(self) -> None:
        '''loads the words from the file'''
        with open(self.file_name, 'r') as f:
            self.words = f.read().split()
        # ensure that the words are all uppercase
        self.words = {word.upper() for word in self.words}

    def validate(self) -> None:
        '''
        validates that all words meet the following criteria:
            the correct length,
            have no duplicates,
            and are all uppercase
        '''
        # check the length
        for word in self.words:
            if len(word) != self.word_length:
                raise ValueError(f'{word} is not of length {self.word_length}')
        # check for uppercase
        for word in self.words:
            if word != word.upper():
                raise ValueError(f'{word} is not uppercase')

    def to_set(self) -> set[str]:
        '''returns the set of words'''
        return self.words.copy()

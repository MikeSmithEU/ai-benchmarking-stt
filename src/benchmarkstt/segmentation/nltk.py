from nltk import tokenize, word_tokenize
from benchmarkstt.segmentation import Base
from benchmarkstt.factory import Factory


class Words(Base):
    """
    Split into words.
    """
    def __init__(self, txt, language=None):
        self._txt = txt
        self._language = language if language is not None else 'english'

    def __iter__(self):
        for w in word_tokenize(self._txt, self._language, True):
            yield w + ' '


class Sentences(Base):
    """
    Split into sentences.
    """
    def __init__(self, txt, language=None):
        self._txt = txt
        self._language = language if language is not None else 'english'

    def __iter__(self):
        for s in tokenize.sent_tokenize(self._txt, self._language):
            yield s + ' '


factory = Factory(Base, [Words.__module__])

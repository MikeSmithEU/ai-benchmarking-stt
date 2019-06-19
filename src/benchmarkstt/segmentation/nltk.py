from nltk import tokenize, word_tokenize
from benchmarkstt.segmentation import Base
from benchmarkstt.factory import Factory
from benchmarkstt.schema import Item


class Words(Base):
    """
    Split into words.
    """
    def __init__(self, text, language=None, normalizer=None):
        self._text = text
        self._language = language if language is not None else 'english'
        self._normalizer = normalizer
        if self._normalizer is not None:
            self._text = self._normalizer.normalize(text)

    def __iter__(self):
        for w in word_tokenize(self._text, self._language, True):
            yield Item({"item": w, "type": "word", "@raw": w + ' '})


class Sentences(Base):
    """
    Split into sentences.
    """
    def __init__(self, text, language=None, normalizer=None):
        self._text = text
        self._language = language if language is not None else 'english'
        self._normalizer = normalizer
        if self._normalizer is not None:
            self._text = self._normalizer.normalize(text)

    def __iter__(self):
        for s in tokenize.sent_tokenize(self._text, self._language):
            yield Item({"item": s, "type": "sentence", "@raw": s + '.'})


factory = Factory(Base, [Words.__module__])

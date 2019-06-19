from benchmarkstt.normalization import Base
from benchmarkstt.segmentation import nltk
from itertools import islice


class First(Base):
    """
    Shorten the text, only use the first amount of 'kind', eg. first 5 words or first 1 sentence.

    :param int amount: The amount to return
    :param str kind: The kind of segmented items to use, eg. 'words' or 'sentences'

    :example amount: 3
    :example kind: 'words'
    :example text: 'What once was is no longer were.'
    :example result: 'What once was '

    """
    def __init__(self, amount: int, kind=None):
        self._amount = int(amount)
        if self._amount < 0:
            raise ValueError("amount needs to be a positive integer number")

        if kind is None:
            kind = 'word'

        if kind not in nltk.factory:
            kind += 's'
        if kind not in nltk.factory:
            raise ValueError("unrecognized kind", kind)
        self._kind = kind

    def _normalize(self, text: str):
        if self._amount == 0:
            return text

        segmenter = iter(nltk.factory.create(self._kind, text))
        return ' '.join([next(segmenter)['@raw'] for _ in range(self._amount)])


class Last(First):
    """
    Shorten the text, only use the last amount of 'kind', eg. last 5 words or last 1 sentence.

    :param amount: The amount to return
    :param kind: The kind of segmented items to use, eg. 'words' or 'sentences'

    :example amount: 3
    :example kind: 'words'
    :example text: 'What once was is no longer were.'
    :example result: 'What once was '

    """

    def _normalize(self, text: str):
        if self._amount == 0:
            return text

        segmenter = nltk.factory.create(self._kind, text)
        return ''.join([item['@raw'] for item in list(segmenter)[-self._amount:]])

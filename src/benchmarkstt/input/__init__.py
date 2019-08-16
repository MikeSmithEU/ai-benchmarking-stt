"""
Subpackage responsible for dealing with input formats and converting them to benchmarkstt native schema
"""

from benchmarkstt.factory import Factory
from benchmarkstt.segmentation import Base as SegmenterBase


class Base:
    def segmented(self, segmenter: SegmenterBase):
        """
        Each input class should be accessible as iterator, each iteration should
        return a Item, so the input format is essentially usable and can be easily
        converted to a :py:class:`benchmarkstt.schema.Schema`
        """

        raise NotImplementedError()


factory = Factory(Base)

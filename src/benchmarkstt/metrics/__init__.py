from benchmarkstt.factory import Factory
from benchmarkstt.input import Base as InputBase


class Base:
    """
    Base class for metrics
    """
    def compare(self, ref: InputBase, hyp: InputBase):
        raise NotImplementedError()


factory = Factory(Base)

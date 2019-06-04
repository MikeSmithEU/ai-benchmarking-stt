from benchmarkstt.factory import Factory
from benchmarkstt.metrics import Base
from benchmarkstt.schema import Schema


class WeightedWER(Base):

    def compare(self, ref: Schema, hyp: Schema):
        pass


factory = Factory(Base, [WeightedWER.__module__])

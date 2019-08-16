"""
Subpackage responsible for dealing with output formats
"""

from benchmarkstt.factory import Factory


class Base:
    SECTIONS = ('title', 'result', 'section')

    def __init__(self):
        self._level = 0

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def title(self, text, level=None):
        raise NotImplementedError()

    def result(self, result):
        raise NotImplementedError()

    def section(self, **kwargs):
        if any(name not in self.SECTIONS for name in kwargs):
            raise ValueError("Unknown argument")

        self.start_section()
        for k in self.SECTIONS:
            try:
                v = kwargs[k]
            except KeyError:
                continue
            method = getattr(self, k)
            if type(v) is not tuple:
                v = (v,)
            method(*v)

        self.stop_section()

    def start_section(self):
        self._level += 1

    def stop_section(self):
        self._level -= 1

    # forward compatibility: write to streams
    @staticmethod
    def write(*args, **kwargs):
        print(*args, **kwargs, end='')


factory = Factory(Base)

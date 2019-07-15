from benchmarkstt import output
from benchmarkstt.schema import Schema


class ReStructuredText(output.Base):
    _levelChars = '=-~#+*_`:\'"^<>'

    def title(self, text, level=None):
        if level is None:
            level = self._level

        self.write(text)
        self.write('\n')
        self.write(self._levelChars[level] * len(text))
        self.write('\n\n')

    def result(self, result):
        if type(result) is float:
            self.write("%.6f" % (result,))
        else:
            self.write(result)
        self.write('\n\n')


class MarkDown(output.Base):
    def title(self, text, level=None):
        if level is None:
            level = self._level

        self.write(' '.join(['#' * (level+1), text]))
        self.write('\n\n')

    def result(self, result):
        if type(result) is float:
            self.write("%.6f" % (result,))
        else:
            self.write(result)
        self.write('\n\n')


class Json(output.Base):
    def __init__(self):
        super().__init__()
        self._line = None
        self._sectionlines = [None]
        self._titlebuffer = None

    def __enter__(self):
        if self._line is not None:
            raise ValueError("Already open")
        self.write('[')
        self._line = 0
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._line = None
        self.write('\n]\n')

    def title(self, text, level=None):
        if not self._level and self._titlebuffer is None:
            self._titlebuffer = text
            return
        if self._current_section_line != 0:
            self.write(',\n')
        self.write('\t')
        self.write(Schema.dumps(text))

    @property
    def _current_section_line(self):
        if self._level == 0:
            return self._line
        return self._sectionlines[self._level - 1] - self._line

    def increase_line(self):
        if self._level == 0:
            self._line += 1
        else:
            self._sectionlines[self._level - 1] += 1

    def result(self, result):
        line = self._current_section_line
        if line != 0:
            self.write(',')
        self.write('\n\t')
        if self._titlebuffer is None:
            self.write(Schema.dumps(result))
        else:
            self.write(Schema.dumps(dict(title=self._titlebuffer, result=result)))
            self._titlebuffer = None
        self.increase_line()

    def start_section(self):
        super().start_section()
        self._sectionlines.insert(self._line, self._level)

    def stop_section(self):
        if self._titlebuffer:
            title = self._titlebuffer
            self.title(title)
            self._titlebuffer = None
        if self._current_section_line > 0:
            self.write(',')
        super().stop_section()
        del self._sectionlines[self._level]

"""
Default input formats

"""

from benchmarkstt import input, settings
# from benchmarkstt.modules import LoadObjectProxy


class PlainText(input.Base):
    """
    plain text
    """
    def __init__(self, text, normalizer=None):
        self._text = text
        self._normalizer = normalizer

    def segmented(self, segmenter):
        return iter(segmenter(self._text, normalizer=self._normalizer))

    def __str__(self):
        return self._text


class File(input.Base):
    """
    Load from a given filename.
    """

    _extension_to_class = {
        "txt": PlainText,
    }

    @classmethod
    def available_types(cls):
        return {cls_config.name: ' '.join([cls.__doc__.strip(),
                                           'Treat file as',
                                           cls_config.cls.__doc__.strip()])
                for cls_config in input.factory
                if cls_config.name != 'file'}

    def __init__(self, file, input_type=None, normalizer=None):
        self._normalizer = normalizer
        if input_type is None or input_type == 'infer':
            if '.' not in file:
                raise ValueError('Cannot infer input file type of files without an extension')

            extension = file.rsplit('.', 1)[1].lower()
            if extension not in self._extension_to_class:
                raise ValueError('Cannot infer input file type for files of extension %s' % (extension,))

            input_type = self._extension_to_class[extension]

        encoding = settings.default_encoding
        with open(file, encoding=encoding):
            """Just checks that file is readable..."""

        self._file = file

        if type(input_type) is str:
            input_type = input.factory[input_type]

        self._input_class = input_type
        self._text = None

    @property
    def text(self):
        if self._text is None:
            encoding = settings.default_encoding
            with open(self._file, encoding=encoding) as f:
                self._text = f.read()

        return self._text

    def segmented(self, segmenter):
        return self._input_class(self.text, normalizer=self._normalizer).segmented(segmenter)

    def __str__(self):
        return self.text


# For future versions
# class ExternalInput(LoadObjectProxy, input.Base):
#     """
#     Automatically loads an external input class.
#
#     :param name: The name of the input to load (eg. mymodule.input.MyFileFormat)
#     """

from benchmarkstt.input.core import PlainText
import benchmarkstt.metrics as metrics

factory = metrics.factory


def callback(cls, ref: str, hyp: str, *args, **kwargs):
    """
    :example ref:

        .. code-block:: text

            Brave Sir Robin ran away. Bravely ran away away. When danger
            reared it’s ugly head, he bravely turned his tail and
            fled.
            Brave Sir Robin turned about and gallantly he chickened out...

    :example hyp:

        .. code-block:: text

            Brave Sir Robin ran away. Bravely ran away away. When danger
            reared it’s wicked head, he bravely turned his tail and
            fled. Brave Sir Chicken turned about and chickened out... Innit?

    :param ref: Reference text
    :param hyp: Hypothesis text

    """
    ref = PlainText(ref)
    hyp = PlainText(hyp)
    return cls(*args, **kwargs).compare(ref, hyp)

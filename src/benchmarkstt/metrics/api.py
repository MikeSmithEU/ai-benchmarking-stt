from benchmarkstt.input.core import PlainText
import benchmarkstt.metrics as metrics

factory = metrics.factory


def callback(cls, ref: str, hyp: str, *args, **kwargs):
    """
    :param ref: Reference text
    :param hyp: Hypothesis text

    :example ref: "Brave Sir Robin ran away. Bravely ran away away. When danger\\nreared it’s ugly head, he bravely turned his tail and\\nfled. Brave Sir Robin turned about and gallantly he chickened out..."
    :example hyp: "Brave Sir Robin ran away. Bravely ran away away. When danger\\nreared it’s wicked head, he bravely turned his tail and\\nfled. Brave Sir Chicken turned about and chickened out... Didn't he?"
    """
    ref = PlainText(ref)
    hyp = PlainText(hyp)
    return cls(*args, **kwargs).compare(ref, hyp)

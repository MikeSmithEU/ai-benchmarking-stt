import benchmarkstt.metrics as metrics
from io import StringIO
from benchmarkstt.input.core import PlainText
from benchmarkstt.normalization.core import Config
from benchmarkstt.normalization import NormalizationComposite
from benchmarkstt.normalization.logger import LogCapturer

factory = metrics.factory


def callback(cls, ref: str, hyp: str, config: str = None, return_logs: bool = None, *args, **kwargs):
    """
    :param ref: Reference text
    :param hyp: Hypothesis text
    :param config: The config to use
    :param bool return_logs: Return normalization logs

    :example ref: 'Hello darkness my OLD friend'
    :example hyp: 'Hello darkness my old foe'
    :example config:

            .. code-block:: text

                [normalization]
                # using a simple config file
                Lowercase

    :example result: ""
    """

    normalizer_ref = None
    normalizer_hyp = None

    if config is not None and len(config.strip()):
        normalizer = Config(StringIO(config), section='normalization')
        normalizer_ref = NormalizationComposite(title='Reference')
        normalizer_ref.add(normalizer)
        normalizer_hyp = NormalizationComposite(title='Hypothesis')
        normalizer_hyp.add(normalizer)

    ref = PlainText(ref, normalizer=normalizer_ref)
    hyp = PlainText(hyp, normalizer=normalizer_hyp)

    metric = cls(*args, **kwargs)
    cls_name = cls.__name__.lower()

    def get_result():
        result = metric.compare(ref, hyp)
        if isinstance(result, tuple) and hasattr(result, '_asdict'):
            result = result._asdict()
        return result

    if not return_logs:
        return {
            cls_name: get_result()
        }

    with LogCapturer(dialect='html', diff_formatter_dialect='dict') as logcap:
        return {
            cls_name: get_result(),
            "logs": logcap.logs
        }

"""
Calculate metrics based on the comparison of a hypothesis with a reference.
"""

from benchmarkstt.input import core
from benchmarkstt.output import factory as output_factory
from benchmarkstt.metrics import factory
from benchmarkstt.cli import args_from_factory
from benchmarkstt.cli import ActionWithArgumentsFormatter
import argparse
from inspect import signature, Parameter


Formatter = ActionWithArgumentsFormatter


def argparser(parser: argparse.ArgumentParser):
    # steps: input normalize[pre?] segmentation normalize[post?] compare

    parser.add_argument('reference', help='file to use as reference')
    parser.add_argument('hypothesis', help='file to use as hypothesis')

    parser.add_argument('-rt', '--reference-type', default='infer',
                        help='type of reference file')
    parser.add_argument('-ht', '--hypothesis-type', default='infer',
                        help='type of hypothesis file')

    parser.add_argument('-o', '--output-format', default='restructuredtext', choices=output_factory.keys(),
                        help='format of the outputted results')

    metrics_desc = "A list of metrics to calculate. At least one metric needs to be provided."

    subparser = parser.add_argument_group('available metrics', description=metrics_desc)
    args_from_factory('metrics', factory, subparser)
    return parser


def file_to_iterable(file, type_, normalizer=None):
    if type_ == 'argument':
        return core.PlainText(file, normalizer=normalizer)
    return core.File(file, type_, normalizer=normalizer)


def main(parser, args, normalizer=None):
    ref = file_to_iterable(args.reference, args.reference_type, normalizer=normalizer)
    hyp = file_to_iterable(args.hypothesis, args.hypothesis_type, normalizer=normalizer)

    ref = list(ref)
    hyp = list(hyp)

    if 'metrics' not in args or not len(args.metrics):
        parser.error("need at least one metric")

    with output_factory.create(args.output_format) as out:
        for item in args.metrics:
            metric_name = item.pop(0).replace('-', '.')
            cls = factory.get_class(metric_name)
            kwargs = dict()

            # somewhat hacky default diff formats for metrics
            sig = signature(cls.__init__).parameters
            sigkeys = list(sig)

            if 'dialect' in sigkeys:
                idx = sigkeys.index('dialect') - 1
                sig = sig['dialect']
                if sig.kind in (Parameter.POSITIONAL_OR_KEYWORD, Parameter.POSITIONAL_ONLY):
                    if len(item) <= idx:
                        if args.output_format == 'json':
                            kwargs['dialect'] = 'list'
                        else:
                            kwargs['dialect'] = 'cli'

            metric = cls(*item, **kwargs)
            result = metric.compare(ref, hyp)
            out.title(metric_name)
            if type(result) is list and len(result) > 0 and isinstance(result[0], list):
                for row in result:
                    out.section(title=row['title'], result=row['result'])
            else:
                out.result(result)

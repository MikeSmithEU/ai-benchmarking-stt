"""
Do a complete flow of input -> normalization -> segmentation -> metrics
"""

from benchmarkstt.metrics.cli import argparser as args_metrics
from benchmarkstt.metrics.cli import main as do_metrics
from benchmarkstt.normalization.cli import args_inputfile, args_logs, args_normalizers, get_normalizer_from_args
import argparse


def argparser(parser: argparse.ArgumentParser):
    args_logs(parser)
    args_inputfile(parser)

    args_metrics(parser)
    args_normalizers(parser)
    return parser


def main(parser, args):
    if 'metrics' not in args or not len(args.metrics):
        parser.error("need at least one metric")

    normalizer = get_normalizer_from_args(args)
    do_metrics(parser, args, normalizer)
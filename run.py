"""
Voicevox runner
"""

import argparse
import sys

from http_runner import HttpRunner
from repl_runner import ReplRunner

RUNNERS = {
    'repl': ReplRunner,
    'http': HttpRunner,
}


def usage():
    """usage: {file}  repl | http"""
    print(__doc__.format(file=__file__))
    sys.exit(1)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", type=str, default='repl', choices=RUNNERS, help='mode')
    parser.add_argument("--speaker_id", type=int, default=25, metavar='ID', help='speaker id')

    args = parser.parse_args()

    runner_cls = RUNNERS[args.mode]
    runner = runner_cls(args.speaker_id)
    runner.main_loop()

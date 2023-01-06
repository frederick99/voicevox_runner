import argparse
from http_runner import HttpRunner
from repl_runner import ReplRunner

RUNNERS = dict(
    repl=ReplRunner,
    http=HttpRunner,
)

def usage():
    msg = f"""usage: {__file__}  repl | http"""
    print(msg)
    exit(1)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", type=str, default='repl', choices=RUNNERS, help='mode, default is repl')
    parser.add_argument("--speaker_id", type=int, default=25, metavar='ID', help='speaker id')

    args = parser.parse_args()

    runner = RUNNERS[args.mode]
    runner(args.speaker_id).run()

"""
Repl runner
"""

import runner


class ReplRunner(runner.Runner):
    """Repl runner class"""

    def tts_loop(self):
        while True:
            data = input('> ')
            self.queue_tts(data)

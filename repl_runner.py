import asyncio
import runner

class ReplRunner(runner.Runner):
    def interactive_loop(self):
        while True:
            self.enqueue(input('> '))

    def run(self):
        async def _run():
            wave_task = asyncio.create_task(self.wave_thread())
            text_task = asyncio.create_task(self.text_thread())
            repl_task = asyncio.to_thread(self.interactive_loop)
            await asyncio.gather(wave_task, text_task, repl_task)

        try: asyncio.run(_run())
        except KeyboardInterrupt: ...

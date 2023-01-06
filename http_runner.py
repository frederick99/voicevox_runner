import asyncio
import http
import http.server
import runner

class HttpRunner(runner.Runner):
    def __init__(self, port=5001):
        super().__init__()
        self.host = '0.0.0.0'
        self.port = port

        http_runner = self
        class TTSRequestHandler(http.server.BaseHTTPRequestHandler):
            def log_message(*_): ...
            def do_POST(self):
                if n := int(self.headers.get('Content-Length', 0)):
                    encoded = self.rfile.read(n)
                    decoded = encoded.decode('utf-8', 'surrogateescape')
                    print('got:', decoded)
                    http_runner.enqueue(decoded)
                self.send_response(http.HTTPStatus.OK)
                self.send_header('Content-Length', 0)
                self.end_headers()

        self.server = http.server.ThreadingHTTPServer((self.host, self.port), TTSRequestHandler)
        print(f"Serving HTTP on {self.host} port {self.port} "
              f"(http://{self.host}:{self.port}/) ...")

    def run(self):
        async def _run():
            wave_task = asyncio.create_task(self.wave_thread())
            text_task = asyncio.create_task(self.text_thread())
            http_task = asyncio.to_thread(self.server.serve_forever)
            await asyncio.gather(wave_task, text_task, http_task)

        try: asyncio.run(_run())
        except (KeyboardInterrupt, RuntimeError):
            print('shutting down http server...')
            self.server.shutdown()
#RuntimeError('Event loop is closed')

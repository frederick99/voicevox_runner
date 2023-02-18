"""
HTTP runner
"""

import http
import http.server
import runner


class HttpRunner(runner.Runner):
    """HTTP runner class"""

    def __init__(self, speaker_id=None, port=5001):
        super().__init__(speaker_id)
        self.host = '0.0.0.0'
        self.port = port

    def tts_loop(self):
        try:
            http_runner = self

            class TTSRequestHandler(http.server.BaseHTTPRequestHandler):
                """Text-to-speech request handler"""
                def log_message(self, *_): ...

                # pylint: disable=invalid-name
                def do_POST(self):
                    """Handle POST request"""
                    if length := int(self.headers.get('Content-Length', 0)):
                        encoded = self.rfile.read(length)
                        decoded = encoded.decode('utf-8', 'surrogateescape')
                        print('got:', decoded)
                        http_runner.queue_tts(decoded)
                    self.send_response(http.HTTPStatus.OK)
                    self.send_header('Content-Length', 0)
                    self.end_headers()

            server = http.server.ThreadingHTTPServer((self.host, self.port), TTSRequestHandler)
            print(f"Serving HTTP at http://{self.host}:{self.port}/ ...")
            server.serve_forever()
        except (KeyboardInterrupt, RuntimeError):
            print('shutting down http server...')
            server.shutdown()

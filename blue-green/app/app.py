import os
from http.server import BaseHTTPRequestHandler, HTTPServer

VERSION = os.environ.get("APP_VERSION", "1")
COLOR = os.environ.get("APP_COLOR", "unknown")
BROKEN = os.environ.get("BREAK", "0") == "1"


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/health":
            if BROKEN:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(b"unhealthy")
            else:
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b"ok")
        else:
            self.send_response(200)
            self.end_headers()
            self.wfile.write(f"Hello! Version {VERSION} running on {COLOR}\n".encode())


HTTPServer(("0.0.0.0", 8000), Handler).serve_forever()

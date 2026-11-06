from http.server import BaseHTTPRequestHandler, HTTPServer
import json

class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        data = json.loads(self.rfile.read(length))
        for alert in data.get("alerts", []):
            print("ALERT", alert["status"], alert["labels"].get("alertname"), "-", alert["annotations"].get("summary"), flush=True)
        self.send_response(200)
        self.end_headers()

    def log_message(self, *args):
        pass

HTTPServer(("0.0.0.0", 5001), Handler).serve_forever()

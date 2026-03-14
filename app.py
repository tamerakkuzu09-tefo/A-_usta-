from http.server import HTTPServer, BaseHTTPRequestHandler
import os

PORT = int(os.environ.get("PORT", 8080))

with open("index.html", encoding="utf-8") as f:
    HTML = f.read()

HTML_BYTES = HTML.encode("utf-8")

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(HTML_BYTES)))
        self.end_headers()
        self.wfile.write(HTML_BYTES)
    def log_message(self, format, *args):
        pass

print(f"Sunucu baslatiliyor: port {PORT}")
HTTPServer(("0.0.0.0", PORT), Handler).serve_forever()

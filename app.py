from http.server import HTTPServer, BaseHTTPRequestHandler
import os

PORT = int(os.environ.get("PORT", 8080))

HTML = open("index.html", encoding="utf-8").read()

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(HTML.encode("utf-8"))
    def log_message(self, format, *args):
        pass

print(f"Sunucu baslatiliyor: port {PORT}")
HTTPServer(("0.0.0.0", PORT), Handler).serve_forever()

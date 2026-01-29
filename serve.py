#!/usr/bin/env python3
"""serve.py - local dev server for the standalone EchoValentines Canvas 5-page site

Usage:
  python3 serve.py
Then open:
  http://localhost:8092/index.html
"""

from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
import webbrowser, os

PORT = int(os.environ.get("PORT","8092"))

class NoCache(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Cache-Control", "no-store, max-age=0")
        super().end_headers()

if __name__ == "__main__":
    httpd = ThreadingHTTPServer(("0.0.0.0", PORT), NoCache)
    print(f"Serving on http://localhost:{PORT}/index.html")
    try:
        webbrowser.open(f"http://localhost:{PORT}/index.html")
    except Exception:
        pass
    httpd.serve_forever()

"""
AURA Web Launcher
Starts a local web server and automatically opens the AURA sanctuary in your default browser.
"""

import http.server
import socketserver
import webbrowser
import os
import sys

import socket

PORT = 5000
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

def find_available_port(start_port=5000, max_attempts=50):
    for port in range(start_port, start_port + max_attempts):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(('127.0.0.1', port))
                return port
            except OSError:
                continue
    return 8000

def main():
    os.chdir(DIRECTORY)
    port = find_available_port(5000)
    url = f"http://127.0.0.1:{port}/index.html"
    if sys.stdout.encoding.lower() != 'utf-8':
        try:
            sys.stdout.reconfigure(encoding='utf-8')
        except Exception:
            pass

    print("=" * 60)
    print("AURA: Women's Empowerment, Style & Mindset Sanctuary")
    print(f"Serving at: {url}")
    print("Press Ctrl+C to stop the server.")
    print("=" * 60)

    webbrowser.open(url)

    socketserver.TCPServer.allow_reuse_address = True
    try:
        with socketserver.TCPServer(("127.0.0.1", port), Handler) as httpd:
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nAURA server stopped. Stay radiant!")
        sys.exit(0)

if __name__ == "__main__":
    main()

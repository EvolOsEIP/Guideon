#!/bin/python3

from http.server import BaseHTTPRequestHandler, HTTPServer
from dotenv import load_dotenv

load_dotenv()

class GithubHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        # print the request
        print("Received POST request")
        print(f"Headers: {self.headers}")
        print(f"Path: {self.path}")

        # send response
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

if __name__ == "__main__":
    # Set up the server
    server_address = ('', 8000)  # Listen on port 8000
    httpd = HTTPServer(server_address, GithubHandler)
    print("Starting server on port 8000...")

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        httpd.server_close()
        print("Server stopped.")

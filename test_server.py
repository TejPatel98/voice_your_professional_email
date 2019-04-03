from http.server import HTTPServer, BaseHTTPRequestHandler

class BoilermakeHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(s):
        s.send_response(200)
        s.send_header('Content-type', 'text/html')
        s.end_headers()
        s.wfile.write(b'Hello world!')

server_address = ('', 8000)
httpd = HTTPServer(server_address, BoilermakeHTTPRequestHandler)
httpd.serve_forever()
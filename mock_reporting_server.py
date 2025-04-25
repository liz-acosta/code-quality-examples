from http.server import BaseHTTPRequestHandler, HTTPServer
import json

class MockReportingServer(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/api/status':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            try:
                data = json.loads(post_data.decode('utf-8'))
                print(f"Mock Server received status: {data}")
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response = json.dumps({'message': 'Status received successfully'})
                self.wfile.write(response.encode('utf-8'))
            except json.JSONDecodeError:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response = json.dumps({'error': 'Invalid JSON'})
                self.wfile.write(response.encode('utf-8'))
        else:
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = json.dumps({'error': 'Not Found'})
            self.wfile.write(response.encode('utf-8'))

def run_mock_server(port=8081):
    http = HTTPServer(('localhost', port), MockReportingServer)
    print(f"Mock reporting server running on http://localhost:{port}")
    http.serve_forever()

if __name__ == "__main__":
    run_mock_server()
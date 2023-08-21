import http.server
import requests

class ProxyHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        # Modify the Solr API URL accordingly
        solr_url = 'http://localhost:8983/solr/documents2/select' + self.path
        response = requests.get(solr_url)
        self.send_response(response.status_code)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(response.content)

def run(server_class=http.server.HTTPServer, handler_class=ProxyHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print('Starting proxy server on port', port)
    httpd.serve_forever()

if __name__ == '__main__':
    run()

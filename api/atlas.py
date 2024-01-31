from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib import parse
import requests

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        s = self.path
        url_components = parse.urlsplit(s)
        query_string_list = parse.parse_qsl(url_components.query)
        dictionary = dict(query_string_list)

        if "country" in dictionary:
            country_name = dictionary["country"]
            url = f"https://restcountries.com/v3.1/name/{country_name}"
            r = requests.get(url)
            
            if r.status_code == 200:
                data = r.json()
                capital = data[0]['capital'][0] if 'capital' in data[0] else "Unknown"
                message = f"The capital of {country_name} is {capital}."
                self.send_response(200)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(message.encode())
            else:
                self.send_error(404, f"Country '{country_name}' not found")
        else:
            self.send_error(400, "Bad Request: Missing 'country' parameter")

if __name__ == "__main__":
    server_address = ('', 8080)
    httpd = HTTPServer(server_address, handler)
    print("Server running on port 8080...")
    httpd.serve_forever()

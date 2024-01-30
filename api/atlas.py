from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib import parse
import requests
import json

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        s = self.path
        url_components = parse.urlsplit(s)
        query_string_list = parse.parse_qsl(url_components.query)
        dicctionary = dict(query_string_list)


        if "country" in dicctionary:
            url = f"https://restcountries.com/v3.1/name/"
            r = requests.get(url + dicctionary["country"])


            if r.status_code == 200:
                data = r.json()
                capitals = [country_data['capital'][0] if 'capital' in country_data else "No Capital" for country_data in data]
                self.send_response(200)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(json.dumps({'capitals': capitals}).encode())
            else:
                self.send_error(404, "Country not found")
        else:
                self.send_error(400, "Bad Request: Missing 'country' parameter")

if __name__ == "__main__":
    server_address = ('',8080)
    httpd = HTTPServer(server_address, handler)
    print("Server running on port 8080...")
    httpd.serve_forever()
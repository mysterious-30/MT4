from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs
import json

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        data = parse_qs(post_data)
        
        # Process MT4 data
        action = data.get('action', [''])[0]
        symbol = data.get('symbol', [''])[0]
        price = data.get('price', [''])[0]
        
        print(f"Received: {action}, {symbol}, {price}")
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        response = {"status": "success", "data": {"action": action, "symbol": symbol, "price": price}}
        self.wfile.write(json.dumps(response).encode('utf-8'))

from http.server import BaseHTTPRequestHandler
from infinity_ai import AI
import json
import time

client = AI()
MAX_RETRIES = 3

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            # Read input
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data)
            
            # Retry logic
            for attempt in range(MAX_RETRIES):
                try:
                    response = client.chat.completions.create(
                        model=data.get('model', 'Orion'),
                        messages=data['messages'],
                        web_search=data.get('web_search', False)
                    )
                    
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({
                        "response": response.choices[0].message.content
                    }).encode())
                    return
                    
                except Exception as e:
                    if attempt < MAX_RETRIES - 1:
                        time.sleep(0.5 * (attempt + 1))
                        continue
                    raise

        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({
                "error": str(e)
            }).encode())
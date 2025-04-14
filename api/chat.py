from http.server import BaseHTTPRequestHandler
from infinity_ai import AI
import json
import signal
import time

client = AI()
MAX_TOKENS = 300  # Reduce response length
TIMEOUT = 8       # 8 second timeout

class TimeoutException(Exception):
    pass

def handler(signum, frame):
    raise TimeoutException()

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        signal.signal(signal.SIGALRM, handler)
        signal.alarm(TIMEOUT)
        
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data)
            
            # Optimize AI parameters
            response = client.chat.completions.create(
                model="Orion",
                messages=data['messages'],
                web_search=False,
                max_tokens=MAX_TOKENS,
                temperature=0.7
            )
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({
                "response": response.choices[0].message.content
            }).encode())
            
        except TimeoutException:
            self.send_response(504)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({
                "error": "Processing timeout",
                "advice": "Please try again with a shorter query"
            }).encode())
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({
                "error": str(e),
                "type": type(e).__name__
            }).encode())
            
        finally:
            signal.alarm(0)

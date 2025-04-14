from http.server import BaseHTTPRequestHandler
from infinity_ai import AI
import json
import traceback

client = AI()  # Ensure this is properly initialized

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            # Read input
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data)
            
            # Debugging log
            print("Received request:", data)
            
            # Process request
            response = client.chat.completions.create(
                model=data.get('model', 'Orion'),
                messages=data['messages'],
                web_search=False,
                max_tokens=150  # Limit response size
            )
            
            # Send response
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({
                "response": response.choices[0].message.content
            }).encode())
            
            print("Request processed successfully")
            
        except Exception as e:
            print(f"Error: {str(e)}\n{traceback.format_exc()}")
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({
                "error": "Internal server error",
                "details": str(e)
            }).encode())

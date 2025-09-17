from flask import Flask
import requests

app = Flask(__name__)

class APIGateway:
    def __init__(self):
        self.services = {
            'user': 'http://localhost:5001',
            'order': 'http://localhost:5002'
        }
    
    @app.route('/api/<service>/<path:path>')
    def proxy_request(service, path):
        if service in self.services:
            url = f"{self.services[service]}/{path}"
            return requests.get(url).json()
        return {'error': 'Service not found'}, 404

if __name__ == '__main__':
    app.run(port=5000)
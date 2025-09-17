import jwt
from flask import Flask, request, jsonify
from werkzeug.security import check_password_hash

app = Flask(__name__)

class AuthService:
    def __init__(self):
        self.secret_key = "your-secret-key"
    
    @app.route('/login', methods=['POST'])
    def login(self):
        data = request.get_json()
        # Authenticate user logic here
        token = jwt.encode({'user_id': data['user_id']}, self.secret_key)
        return jsonify({'token': token})
    
    @app.route('/verify', methods=['POST'])
    def verify_token(self):
        token = request.headers.get('Authorization')
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=['HS256'])
            return jsonify({'valid': True, 'user_id': payload['user_id']})
        except jwt.InvalidTokenError:
            return jsonify({'valid': False}), 401
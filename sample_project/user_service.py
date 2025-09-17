from flask import Flask, jsonify
import mysql.connector

app = Flask(__name__)

class UserService:
    def __init__(self):
        self.db = mysql.connector.connect(host='localhost', database='users')
    
    @app.route('/users', methods=['GET'])
    def get_users(self):
        return jsonify({'users': []})

if __name__ == '__main__':
    app.listen(5000)
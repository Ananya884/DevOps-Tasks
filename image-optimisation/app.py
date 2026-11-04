from flask import Flask, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify(message='Hello from the optimised container')

@app.route('/health')
def health():
    return jsonify(status='ok', requests_version=requests.__version__)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)

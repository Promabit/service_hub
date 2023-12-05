from flask import Flask, jsonify
from flask_cors import CORS
import random
from read_serial import read_scale_data 

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": ["http://localhost:3000"]}}, supports_credentials=True)

@app.route('/')
def scale_reading():
    return jsonify({'status': 'ok'})

@app.route('/scale')
def scale_reading():
    weight, is_stable = read_scale_data('/dev/ttyUSB0')
    return jsonify({'weight': weight, 'stable': is_stable})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)

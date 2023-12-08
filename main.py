from flask import Flask, jsonify, Response
from flask_cors import CORS
from read_serial import read_scale_data 
from threading import Lock

scale_lock = Lock()

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": ["http://localhost:3000", "https://staging.promabit.com", "https://insider.cszoldseg.com", "https://cszoldseg.com"]}}, supports_credentials=True)

@app.route('/')
def status_check():
    return Response(status=200)

@app.route('/scale')
def scale_reading():
    try: 
        with scale_lock:
            weight, is_stable = read_scale_data('/dev/ttyUSB0')
            return jsonify({'weight': weight, 'stable': is_stable})
    except Exception as e:
        print(e)
        return Response(status=400)

if __name__ == '__main__':
    app.run(host='192.168.0.111', port=443, ssl_context=('/home/csz/certs/192.168.0.111+1.pem', '/home/csz/certs/192.168.0.111+1-key.pem'))

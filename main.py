from flask import Flask
import random

app = Flask(__name__)

@app.route('/scale')
def scale_reading():
    # Replace this with the actual scale reading logic
    scale_value = random.randint(1, 100)  # Simulated scale value
    return str(scale_value)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)

from flask import Flask, render_template, send_from_directory
from .service import quantum
from random import Random
import requests

app = Flask(__name__)

@app.route('/assets/<path:path>')
def send_js(path):
    return send_from_directory('assets', path)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

gen = quantum.GenerateQRandService(Random())
a = ""
x = ""
response = ""

@app.route('/measure', methods=['GET'])
def measure():
    global a, x, response
    (a, x, vec) = gen.generate()
    response = requests.post('http://qrand-server:5001/measure', json = {'psi': [str(vec[0]), str(vec[1])]})
    return str(response.json())

@app.route('/verify', methods=['GET'])
def verify():
    global a, x, response
    verification = requests.post(
        'http://qrand-server:5001/verify',
        json = {'a': a, 'x': x},
        cookies = response.cookies
    )
    if (verification.content == b"True"):
        return str(int(response.json()) ^ a)
    else:
        return str("failed")

if __name__ == '__main__':
    app.run(host='0.0.0.0')

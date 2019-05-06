from flask import Flask, jsonify, make_response, request, Response, session
from . import controller
from . import service
from . import repository
from random import Random
import math

app = Flask(__name__)

app.secret_key = 'test'

result = repository.result.ResultRepository(session)
qrand = service.qrand.MeasureQRandService(None, Random(), result)
measureController = controller.masure.MeasureQRandController(qrand)

@app.route('/measure', methods=['POST'])
def measure():
    json = request.get_json()
    alpha = complex(math.sqrt(float(json['alpha'])))
    beta = complex(math.sqrt(float(json['beta'])))

    return str(measureController.postQubit(alpha, beta))

@app.route('/verify', methods=['POST'])
def verify():
    json = request.get_json()
    a = int(json['a'])
    x = int(json['x'])

    return str(measureController.postAX(a, x))
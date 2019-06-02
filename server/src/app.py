from flask import Flask, jsonify, make_response, request, Response, session
from . import controller
from . import service
from . import repository
from random import Random
import numpy as np

app = Flask(__name__)

app.secret_key = 'test'

result = repository.result.ResultRepository(session)
qrand = service.qrand.MeasureQRandService(Random(), result)
measureController = controller.masure.MeasureQRandController(qrand)

@app.route('/measure', methods=['POST'])
def measure():
    json = request.get_json()
    psi = json['psi']
    return str(measureController.postQubit(complex(psi[0]), complex(psi[1])))

@app.route('/verify', methods=['POST'])
def verify():
    json = request.get_json()
    a = int(json['a'])
    x = int(json['x'])

    return str(measureController.postAX(a, x))
from flask import Flask, request, session
from . import controller
from . import service
from . import repository
from random import Random

app = Flask(__name__)

app.secret_key = 'test'

result = repository.result.ResultRepository(session)
qrand = service.qrand.MeasureQRandService(Random(), result)
measureController = controller.masure.MeasureQRandController(qrand)

# クライアントは次のようなJSON形式で1 qubitを送信する。
#   {'psi': ['(0.7071067811865476+0j)', '(-0.7071067811865476+0j)']}
# `psi`の配列（タプル）を利用して
#    psi[0] * |0> + psi[1] * |1>
# という1 qubitが送信されたものとする。
@app.route('/measure', methods=['POST'])
def measure():
    json = request.get_json()
    psi = json['psi']
    return str(measureController.post_qubit(complex(psi[0]), complex(psi[1])))

# クライアントは次のようなJSON形式で`x`と`a`を公開する。
#   {'a': 0, 'x': 0}
# また、HTTPのセッション（Cookie）情報をもとに`/measure`で作成した
# 乱数や測定結果を取り出し検証を行う。
@app.route('/verify', methods=['POST'])
def verify():
    json = request.get_json()
    a = int(json['a'])
    x = int(json['x'])

    return str(measureController.post_ax(a, x))
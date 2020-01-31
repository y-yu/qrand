from flask import Flask, request, session
from .controller import measure, verify as verify_cont
from .service import qrand, verify
from .repository import result
from random import Random
import pickle
import base64

app = Flask(__name__)

# TODO: 適当なのをどうにかしろ
app.secret_key = 'test'

# DI配線。
result_repository = result.ResultRepository(session)
qrand_service = qrand.MeasureQRandService(Random(), result_repository)
verify_service = verify.VerifyQRandService(result_repository)
measure_controller = measure.MeasureQRandController(qrand_service)
verify_controller = verify_cont.VerifyQRandController(verify_service)

# クライアントは次のようなJSON形式で1 qubitを送信する。
#   {'alpha': 'base64string', 'beta': 'base64string']}
# これらはpickleでシリアライズした複素数をBase64（UTF-8）で移動させる。
# これにより`alpha|0> + beta|1>`という1 qubitが送信されたものとする。
# そしてサーバーは乱数bをクライアントへ返答する。
@app.route('/measure', methods=['POST'])
def measure():
    json = request.get_json()
    (alpha, beta) = (
        pickle.loads(base64.b64decode(json['alpha'])),
        pickle.loads(base64.b64decode(json['beta']))
    )
    return measure_controller.post_qubit(alpha, beta)

# クライアントは次のようなJSON形式で`x`と`a`を公開する。
#   {'a': 0, 'x': 0}
# また、HTTPのセッション（Cookie）情報をもとに`/measure`で作成した
# 乱数や測定結果を取り出し検証しその結果を返す。
@app.route('/verify', methods=['POST'])
def verify():
    json = request.get_json()
    return verify_controller.post_ax(int(json['a']), int(json['x']))

if __name__ == '__main__':
    app.run(host='0.0.0.0')
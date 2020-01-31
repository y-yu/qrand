from ..service import qrand
from ..domain.qubit import Qubit
from flask import jsonify, json

# 測定部分のコントローラー
class MeasureQRandController:
    def __init__(self, measure_service_impl: qrand.MeasureQRandService):
        # 測定する部分の詳細をDIする。
        self.measure_service = measure_service_impl

    # `alpha`と`beta`という2つの複素数という形で1 qubitを受けとり測定する。
    # また測定結果およびその際に利用した乱数などをセッションに保存する。
    # 乱数でつくられたbをJSONで返す。
    def post_qubit(self, alpha, beta) -> json:
        qubit = Qubit(alpha, beta)
        print("qubit is %s, %s" % (qubit.alpha, qubit.beta))
        return jsonify(
            {'b': self.measure_service.measure(qubit)}
        )
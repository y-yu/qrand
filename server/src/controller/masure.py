from .. import service
from ..domain.qubit import Qubit

# HTTPのコントローラー
class MeasureQRandController:
    def __init__(self, measure_service_impl: service.qrand.MeasureQRandService):
        self.measure_service = measure_service_impl

    # `alpha`と`beta`という2つの複素数という形で1 qubitを受けとり測定する。
    # また測定結果およびその際に利用した乱数などをセッションに保存する。
    def post_qubit(self, alpha: complex, beta: complex) -> int:
        qubit = Qubit(alpha, beta)
        return self.measure_service.measure(qubit)

    # クライアントはサーバーに対して`a`と`x`を公開して
    # それとセッションに保存された1 qubitの測定結果を元に
    # コイントスが正常に行なわれたかを判定する。
    def post_ax(self, a: int, x: int) -> int:
        return self.measure_service.verify(a, x)
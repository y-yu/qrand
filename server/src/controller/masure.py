from .. import service
from ..domain.qubit import Qubit


class MeasureQRandController:
    def __init__(self, measure_service_impl: service.qrand.MeasureQRandService):
        self.measure_service = measure_service_impl

    def postQubit(self, alpha: complex, beta: complex) -> int:
        qubit = Qubit(alpha, beta)
        return self.measure_service.measure(qubit)

    def postAX(self, a: int, x: int) -> int:
        return self.measure_service.verify(a, x)
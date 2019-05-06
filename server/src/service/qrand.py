from ..domain import qubit
from ..repository import result
from random import Random

class MeasureQRandService:
    def __init__(self, qulacs_impl, random_impl: Random, result_impl: result.ResultRepository):
        self.qulacs_impl = qulacs_impl
        self.random_impl = random_impl
        self.result_impl = result_impl

    def measure(self, qubit: qubit.Qubit) -> int:
        a_hat = self.random_impl.choice([0, 1])
        x_hat = self._qulacs_measure(a_hat)
        b = self.random_impl.choice([0, 1])
        print(a_hat, x_hat)
        self.result_impl.save(a_hat, x_hat, b)
        return b

    def verify(self, a: int, x: int) -> bool:
        (a_hat, x_hat, b) = self.result_impl.pop()
        if a == a_hat and x == x_hat:
            return x ^ b
        else:
            raise Exception()

    def _qulacs_measure(self, a_hat: int) -> int:
        return self.random_impl.choice([0, 1])
from ..domain.qubit import Qubit
from ..repository import result
from random import Random
from qulacs import Observable, QuantumCircuit, QuantumState
from qulacs.gate import DenseMatrix
from qulacs.state import inner_product
import numpy as np

class MeasureQRandService:
    def __init__(self, random_impl: Random, result_impl: result.ResultRepository):
        self.random_impl = random_impl
        self.result_impl = result_impl

    def measure(self, qubit: Qubit) -> int:
        a_hat = self.random_impl.choice([0, 1])
        x_hat = self._qulacs_measure(a_hat, qubit)
        b = self.random_impl.choice([0, 1])
        print("a^: %s, x^: %s" % (a_hat, x_hat))
        self.result_impl.save(a_hat, x_hat, b)
        return b

    def verify(self, a: int, x: int) -> bool:
        (a_hat, x_hat, b) = self.result_impl.pop()
        if a == a_hat and x != x_hat:
            raise Exception()
        else:
            return a ^ b

    def _qulacs_measure(self, a_hat: int, qubit: Qubit) -> int:
        # TODO: コピペをやめろ
        s1 = QuantumState(1)
        s1.set_computational_basis(0)
        s2 = QuantumState(1)
        s2.set_computational_basis(1)

        c1 = QuantumCircuit(1)
        c1.add_H_gate(0)

        s3 = QuantumState(1)
        s3.set_computational_basis(0)
        c1.update_quantum_state(s3)
        s4 = QuantumState(1)
        s4.set_computational_basis(1)
        c1.update_quantum_state(s4)

        psi = [
            [s1, s2], [s3, s4]
        ]
        p = self.random_impl.choice(psi[a_hat])

        state = qubit.toQulacsState()

        c = np.sqrt(inner_product(state, p) * inner_product(p, state))
        f = lambda x: x / c
        p_ = f(np.outer(p.get_vector(), p.get_vector())) if c > 0 else np.outer(p.get_vector(), p.get_vector())



        gate = DenseMatrix(0, p_)
        gate.update_quantum_state(state)

        observable = Observable(1)
        if a_hat == 0:
            print("a^ is 0")
            observable.add_operator(1.0, "X 0 X 0")
            e = observable.get_expectation_value(state)
            print(e)
        else:
            print("a^ is 1")
            observable.add_operator(1.0, "Z 0 Z 0")
            e = observable.get_expectation_value(state)
            print(e)

        return 0 if int(e) == 1 else 1

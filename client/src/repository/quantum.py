from random import Random
from qulacs import QuantumState, QuantumCircuit
from qulacs.gate import DenseMatrix
import numpy
from ..domain.aggregate import QuntumStateAndTwoRandom


class GenerateQuantumStateRepository:
    def __init__(self, random_impl: Random):
        self.random_impl = random_impl

        # ここでは次のような1 qubit状態をつくっている。
        #   s1 = √(0.9)|0> + √(0.1)|1>
        #   s2 = √(0.1)|0> - √(0.9)|1>
        #   s3 = √(0.9)|0> - √(0.1)|1>
        #   s4 = √(0.1)|0> + √(0.9)|1>
        c1 = DenseMatrix(0, [[numpy.sqrt(0.9), 0], [numpy.sqrt(0.1), 0]])
        c2 = DenseMatrix(0, [[numpy.sqrt(0.1), 0], [-numpy.sqrt(0.9), 0]])
        c3 = DenseMatrix(0, [[numpy.sqrt(0.9), 0], [-numpy.sqrt(0.1), 0]])
        c4 = DenseMatrix(0, [[numpy.sqrt(0.1), 0], [numpy.sqrt(0.9), 0]])

        s1 = QuantumState(1)
        s1.set_computational_basis(0)
        c1.update_quantum_state(s1)

        s2 = QuantumState(1)
        s2.set_computational_basis(0)
        c2.update_quantum_state(s2)

        s3 = QuantumState(1)
        s3.set_computational_basis(0)
        c3.update_quantum_state(s3)

        s4 = QuantumState(1)
        s4.set_computational_basis(0)
        c4.update_quantum_state(s4)
        self.psi = [
            s1, s2, s3, s4
        ]

    def generate(self) -> QuntumStateAndTwoRandom:
        # `a`と`x`によって`psi`からqubitを選択する。
        a = self.random_impl.choice([0, 1])
        x = self.random_impl.choice([0, 1])

        print("a: %s x: %s" % (a, x))

        p = self._choice(self.psi, a, x)

        return QuntumStateAndTwoRandom(a, x, p.get_vector())

    def generate_with_cheat(self) -> numpy.ndarray:
        # チート用のステート|+>を作成する。
        state = QuantumState(1)
        state.set_computational_basis(0)
        h_gate = QuantumCircuit(1)
        h_gate.add_H_gate(0)
        h_gate.update_quantum_state(state)
        return state.get_vector()

    def _choice(self, psi: [QuantumState], a: int, x: int) -> QuantumState:
        if a == 0 and x == 0:
            return psi[0]
        elif a == 0 and x == 1:
            return psi[1]
        elif a == 1 and x == 0:
            return psi[2]
        else:
            return psi[3]
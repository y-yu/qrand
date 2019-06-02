from qulacs import QuantumState
from qulacs.gate import DenseMatrix

class Qubit:
    def __init__(self, alpha: complex, beta: complex):
        self.alpha = alpha
        self.beta = beta

    def toQulacsState(self) -> QuantumState:
        s = QuantumState(1)
        s.set_computational_basis(0)

        gate = DenseMatrix(0, [[self.alpha, 0], [self.beta, 0]])
        gate.update_quantum_state(s)
        return s

from qulacs import QuantumState
from qulacs.gate import DenseMatrix

class Qubit:
    def __init__(self, alpha, beta):
        self.alpha = alpha
        self.beta = beta

    # 複素数の組である`Qubit`型からqulacsの型へと変換する。
    def to_qulacs_state(self) -> QuantumState:
        s = QuantumState(1)
        s.set_computational_basis(0)

        gate = DenseMatrix(0, [[self.alpha, 0], [self.beta, 0]])
        gate.update_quantum_state(s)
        print("qulacs qubit is (%.18f, %.18f)" % (s.get_vector()[0], s.get_vector()[1]))
        return s

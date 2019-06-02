from random import Random
from qulacs import QuantumCircuit, QuantumState

class GenerateQRandService:
    def __init__(self, random_impl: Random):
        self.random_impl = random_impl

    def generate(self) -> (int, int, any):
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
            s1, s2, s3, s4
        ]

        a = self.random_impl.choice([0, 1])
        x = self.random_impl.choice([0, 1])

        print("a: %s x: %s" % (a, x))

        p = self._choice(psi, a, x)

        return (a, x, p.get_vector())


    def _choice(self, psi: [QuantumState], a: int, x: int) -> QuantumState:
        if a == 0 and x == 0:
            return psi[0]
        elif a == 0 and x == 1:
            return psi[1]
        elif a == 1 and x == 0:
            return psi[2]
        else:
            return psi[3]
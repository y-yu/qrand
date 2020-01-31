from ..repository import quantum, qrand_api_caller
from random import Random
from qulacs import QuantumState
from qulacs.gate import H


# クライアントがチートをするためのサービス。
class PostCheatStateService:
    def __init__(
        self,
        random_impl: Random,
        send_qubit_impl: qrand_api_caller.QRandApiRepository,
    ):
        self.random_impl = random_impl
        self.send_qubit_impl = send_qubit_impl

        # チート用の2 qubitである|+>, |->を用意する。
        h_gate = H(0)

        s1 = QuantumState(1)
        s1.set_computational_basis(0)
        h_gate.update_quantum_state(s1)
        s2 = QuantumState(1)
        s2.set_computational_basis(1)
        h_gate.update_quantum_state(s2)

        self.psi = [s1, s2]

    # チートを実行する。
    # 本来の1 qubitとは異なり|+>, |->を送信する。
    def post_cheat(self) -> object:
        qubit = self.random_impl.choice(self.psi)
        response = self.send_qubit_impl.send_measure(qubit.get_vector())

        # a, xはチートの進行に応じて決めるため、クライアントに返さない。
        return {
            'is_cheating': True,
            'b': response.json()['b'],
            'session': response.cookies['session']
        }

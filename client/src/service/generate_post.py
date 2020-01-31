from ..repository import quantum, qrand_api_caller

class GenerateAndPostService:
    def __init__(
        self,
        send_qubit_impl: qrand_api_caller.QRandApiRepository,
        quantum_impl: quantum.GenerateQuantumStateRepository
    ):
        self.send_qubit_impl = send_qubit_impl
        self.quantum_impl = quantum_impl

    # 最初の処理を何もかもやる。
    def execute(self) -> object:
        state_and_randoms = self.quantum_impl.generate()
        response = self.send_qubit_impl.send_measure(state_and_randoms.qubit)

        return {
            'a': state_and_randoms.a,
            'x': state_and_randoms.x,
            'is_cheating': False,
            'b': response.json()['b'],
            'session': response.cookies['session']
        }

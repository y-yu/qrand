from ..domain.qubit import Qubit
from ..repository import result
from random import Random
from qulacs import QuantumCircuit

class MeasureQRandService:
    def __init__(self, random_impl: Random, result_impl: result.ResultRepository):
        # ここでのランダムはクラスのコンストラクタ引数として注入してある。
        # テストのときに狙った方しか出ないようにするといったことをしやすするため。
        self.random_impl = random_impl

        # プロトコルの途中状態へアクセスするためのモジュール。
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
        # クライアントから公開された`a`と`a^`が等しいならば、
        # クライアント側の`x`と`x^`は等しくなければならない。
        if a == a_hat and x != x_hat:
            raise Exception()
        else:
            return a ^ b

    # 測定を行うプライベート関数
    def _qulacs_measure(self, a_hat: int, qubit: Qubit) -> int:
        # APIのボディから受けとった1 qubitをqulacsの表現へ変換する。
        state = qubit.to_qulacs_state()
        print("state is (%s, %s)" % (qubit.alpha, qubit.beta))

        if a_hat == 0:
            print("a^ is 0")
            e = state.get_zero_probability(0)
        else:
            print("a^ is 1")
            # |+>, |->で測定したいため、Hゲートを作用させる。
            gate = QuantumCircuit(1)
            gate.add_H_gate(0)

            gate.update_quantum_state(state)

            e = state.get_zero_probability(0)

        print(e)

        # Z基底測定で0となる確率が99%より上なら0とする。
        return 0 if e > 0.99 else 1

from ..domain.qubit import Qubit
from ..repository import result
from random import Random
from qulacs.gate import Z, merge, RY
from numpy import sqrt, arccos

class MeasureQRandService:
    def __init__(self, random_impl: Random, result_impl: result.ResultRepository):
        # ここでのランダムはクラスのコンストラクタ引数として注入してある。
        # テストのときに狙った方しか出ないようにするといったことをしやすくするため。
        self.random_impl = random_impl

        # プロトコルの途中状態へアクセスするためのモジュール。
        self.result_impl = result_impl

    # クライアントから送信された`qubit`を測定してその結果を返す。
    # また測定につかったデータa^, x^を保存する。
    # このとき生成した`b in {0, 1}`を返す。
    def measure(self, qubit: Qubit) -> int:
        a_hat = self.random_impl.choice([0, 1])
        x_hat = self._qulacs_measure(a_hat, qubit)
        print("a^: %s, x^: %s" % (a_hat, x_hat))

        b = self.random_impl.choice([0, 1])
        self.result_impl.save(a_hat, x_hat, b)
        return b

    # 測定を行うプライベート関数
    def _qulacs_measure(self, a_hat: int, qubit: Qubit) -> int:
        # APIのボディから受けとった1 qubitをqulacsの表現へ変換する。
        state = qubit.to_qulacs_state()

        ry_gate = RY(0, 2 * arccos(sqrt(9 / 10)))
        if a_hat == 0:
            print("a^ is 0")
            # このs1, s2をそれぞれ|0>, |1>へ移動させるためY軸回転させる。
            #   s1 = √(0.9)|0> + √(0.1)|1>
            #   s2 = √(0.1)|0> - √(0.9)|1>
            # もしこれ以外のときはへんな座標に飛んでいってしまうが、
            # そうしたときにサーバー側は検証ができない（a^ != a)ため気にする必要はない。
            ry_gate = RY(0, 2 * arccos(sqrt(9 / 10)))
            ry_gate.update_quantum_state(state)
        else:
            print("a^ is 1")
            # 次のs3, s4はs1, s2とそれぞれZ軸対象なので回転させる。
            #   s3 = √(0.9)|0> - √(0.1)|1>
            #   s4 = √(0.1)|0> + √(0.9)|1>
            # そのうえでY軸回転してZ軸測定したときs3, s4（つまりa^ == a）なら
            # 0, 1が手にはいり、そうでなければ適当な数となる。
            gate = merge(Z(0), ry_gate)
            gate.update_quantum_state(state)

        # Z基底測定で0となる確率を取得する。
        e = state.get_zero_probability(0)
        print("state is %s" % state.get_vector())
        print("e: %.18f" % e)

        # Z基底測定で0となる確率がよりも小さい乱数が出れば0、そうでなければ1として
        # 測定を模倣する。
        return 0 if self.random_impl.random() <= e else 1


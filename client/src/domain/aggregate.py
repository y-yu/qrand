import numpy

# 1 qubitと付随するデータのアクセシビリティをあげるためのデータ構造。
class QuntumStateAndTwoRandom:
    def __init__(self, a: int, x: int, qubit: numpy.ndarray):
        self.qubit = qubit
        self.a = a
        self.x = x
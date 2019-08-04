# HTTPのセッションを利用して`a^`や`x^`などを格納しておく。
class ResultRepository:
    def __init__(self, session_impl):
        self.session_impl = session_impl

    # 保存
    def save(self, a_hat: int, x_hat: int, b: int) -> None:
        self.session_impl['a_hat'] = str(a_hat)
        self.session_impl['x_hat'] = str(x_hat)
        self.session_impl['b'] = str(b)

    # 取り出し
    def pop(self) -> (int, int, int):
        a_hat = int(self.session_impl['a_hat'])
        x_hat = int(self.session_impl['x_hat'])
        b = int(self.session_impl['b'])
        return (a_hat, x_hat, b)
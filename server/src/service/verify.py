from ..repository import result


class VerifyQRandService:
    def __init__(self, result_impl: result.ResultRepository):
        self.result_impl = result_impl

    # クライアントから送信されたa, xを保存されたa^, x^と突合する。
    def verify(self, a: int, x: int) -> bool:
        (a_hat, x_hat, b) = self.result_impl.pop()
        # クライアントから公開された`a`と`a^`が等しいならば、
        # クライアント側の`x`と`x^`は等しくなければならない。
        if a == a_hat and x != x_hat:
            return False
        # a == a^ではないときは検証ができないため常にTrueとなる。
        else:
            return True


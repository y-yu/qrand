from ..repository import qrand_api_caller


# サーバーへ検証をリクエストして結果を返す。
class VerifyRandomService:
    def __init__(self, qrand_api_impl: qrand_api_caller.QRandApiRepository):
        self.qrand_api_impl = qrand_api_impl

    def execute(self, a: int, x: int, session: str) -> bool:
        response = self.qrand_api_impl.call_verify(a, x, session).json()
        return response['is_valid']
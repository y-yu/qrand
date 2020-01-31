from ..service import verify
from flask import json, jsonify

class VerifyQRandController:
    def __init__(self, verify_service_impl: verify.VerifyQRandService):
        self.verify_service_impl = verify_service_impl

    # クライアントはサーバーに対して公開した`a`と`x`と
    # サーバーのセッションに保存された1 qubitの測定結果を元に
    # コイントスが正常に行なわれたかを判定する。
    def post_ax(self, a: int, x: int) -> json:
        return jsonify(
            {'is_valid': self.verify_service_impl.verify(a, x)}
        )

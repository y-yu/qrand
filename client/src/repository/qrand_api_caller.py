import requests
import numpy
import pickle
import base64


# サーバーへのAPI Caller
class QRandApiRepository:
    # 本当は`requests`もDIにする方がいいだろう……。
    def __init__(self):
        self.measure_url = 'http://qrand-server:5001/measure'
        self.verify_url = 'http://qrand-server:5001/verify'

    # 1 qubitを複素数の配列として受けとってサーバーへ測定をリクエストする。
    # `Qubit`データ構造を使いたかったが、サーバーとクライアントでドメインエンティティを
    # 共有するよい方法がわからなかたったので雑に`numpy.ndarray`を使っている。
    # TODO: Qubitを使えるようにしろ
    def send_measure(self, vector: numpy.ndarray) -> requests.Response:
        return requests.post(
            self.measure_url,
            json={
                'alpha': base64.b64encode(pickle.dumps(vector[0])).decode("utf-8"),
                'beta': base64.b64encode(pickle.dumps(vector[1])).decode("utf-8")
            }
        )

    # サーバーにa, xを公開して検証を実行する。
    # サーバーのデータ参照のため測定APIが返答したセッションを必要とする。
    def call_verify(self, a: int, x: int, session: str) -> requests.Response:
        return requests.post(
            self.verify_url,
            json={'a': str(a), 'x': str(x)},
            cookies={'session': session}
        )

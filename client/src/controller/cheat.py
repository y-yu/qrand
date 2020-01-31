from random import Random
from ..service import send_cheat_state, verify_random
from flask import jsonify, json


class CheatController:
    def __init__(
        self,
        random_impl: Random,
        post_cheat_state_impl: send_cheat_state.PostCheatStateService,
        verify_random_impl: verify_random.VerifyRandomService
    ):
        self.random_impl = random_impl
        self.post_cheat_state_impl = post_cheat_state_impl
        self.verify_random_impl = verify_random_impl

    def measure_with_cheat(self) -> json:
        return jsonify(self.post_cheat_state_impl.post_cheat())

    # チート時の検証は運任にa, xを送信するので、普通の検証サービスをよべばよい。
    def verify_with_cheat(self, json_request: json) -> json:
        # チートのときはフロントから必要な結果を取得する。
        # この期待された結果とサーバーの送信したbによってaを決定する。
        wanted_result = int(json_request['wanted_result'])
        b = int(json_request['b'])
        # `a != a^`ならばその時点でチートは成功する。
        a = wanted_result ^ b

        #　xもaと同様に決める。
        # `a == a^`なら運良く送信した1 qubit（|+> or |->）の結果であるx^が
        # このxと等しくなる確率に賭けることになる。
        x = wanted_result ^ b
        session = str(json_request['session'])

        result = self.verify_random_impl.execute(a, x, session)
        return jsonify(
            {
                # `x = b ^ wanted_result`なのでもう一度bとXORすることで
                # bがキャンセルされてwanted_resultとなる。
                'result': b ^ x,
                'is_verify_valid': result
            }
        )



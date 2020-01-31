from ..service import verify_random
from flask import json, jsonify


class VerifyRequestController:
    def __init__(self, verify_random_impl: verify_random.VerifyRandomService):
        self.verify_random_impl = verify_random_impl

    def render(self, json_request: json) -> json:
        a = int(json_request['a'])
        x = int(json_request['x'])
        b = int(json_request['b'])
        session = str(json_request['session'])

        result = self.verify_random_impl.execute(a, x, session)
        return jsonify(
            {
                'result': b ^ x,
                'is_verify_valid': result
            }
        )

from ..service import generate_post
from flask import json, jsonify

class MeasureRequestController:
    def __init__(self, generate_post_impl: generate_post.GenerateAndPostService):
        self.generate_post_impl = generate_post_impl

    def render(self) -> json:
        return jsonify(
            self.generate_post_impl.execute()
        )
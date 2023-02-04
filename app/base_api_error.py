from flask import jsonify


class BaseApiError(Exception):
    def __init__(self, message, error_code):
        super().__init__(message)
        self.error_code = error_code

    def build_error(code, message):
        return BaseApiError(message, code)

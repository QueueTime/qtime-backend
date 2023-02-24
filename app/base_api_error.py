from flask import jsonify


class BaseApiError(Exception):
    def __init__(self, message: str, error_code: int):
        super().__init__(message)
        self.message = message
        self.error_code = error_code

    def build_error(self):
        return {"success": False, "message": self.message}, self.error_code

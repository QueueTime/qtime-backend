from flask import jsonify


class BaseApiError(Exception):
    def __init__(self, message, error_code):
        super().__init__(message)
        self.message = message
        self.error_code = error_code

    def buildError(self):
        return jsonify({"success": False, "message": self.message}), self.error_code

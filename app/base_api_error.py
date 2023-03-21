from flask import jsonify


class BaseApiError(Exception):
    def __init__(self, message, error_code):
        super().__init__(message)
        self.message = message
        self.error_code = error_code

    def build_error(self):
        return {"success": False, "message": self.message}, self.error_code


class MissingQueryParameterError(BaseApiError):
    def __init__(self, parameter_name):
        super().__init__(f"Missing query parameter: {parameter_name}", 400)

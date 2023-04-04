import os
import re
from datetime import datetime, timezone
from flask import request
from setup import initialize_firebase, start_server, FIREBASE_CERT_PATH


initialize_firebase(FIREBASE_CERT_PATH)
app = start_server(__name__)


@app.route("/")
def home():
    return "<p>Queue Time</p>"


if __name__ == "__main__":
    env = os.environ.get("ENV", "dev")
    if env == "prod":
        # Run the app in production mode with waitress.
        from waitress import serve
        import logging

        logger = logging.getLogger("waitress")
        logger.setLevel(logging.DEBUG)
        SEP = " "
        REPLACE_EXPR = "\s*[\n\r\t]\s*"

        @app.app.after_request
        def after_request_func(response):
            response.direct_passthrough = False  # Allow swagger-ui to work
            logger.debug(
                f'[{datetime.now(timezone.utc).strftime("%d/%b/%Y %H:%M:%S")}] {request.remote_addr} "{request.method} {request.path}{"?"+request.query_string.decode("utf-8") if request.query_string else ""} {request.scheme.upper()}" {response.status_code}'
                f'{SEP + str(request.form.to_dict()) if request.form else ""}'
                f'{SEP + str(request.json) if request.is_json else ""}'
                f'{SEP + re.sub(REPLACE_EXPR, SEP, response.data.decode("utf-8")) if response.data else ""}'
            )
            return response

        serve(app, host="0.0.0.0", port=5000)
    elif env == "dev":
        app.run(debug=True)
    else:
        raise Exception("Unsupported environment, must one of [dev, prod].")

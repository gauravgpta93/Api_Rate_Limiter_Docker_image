from flask import Flask, jsonify
from app.utils.authentication_decorator import AuthenticationChecker, AuthError
from app.utils.rate_limiter_decorator import RateLimiter, RateExceedError

app = Flask(__name__)
api_auth = AuthenticationChecker("X-API-KEY")
rate_limiter = RateLimiter(10, 1)


@app.errorhandler(AuthError)
def handle_auth_error(ex):
    """
    This covers the exceptions raised by authentication failures.
    :param ex: Exception object
    :return:
    """
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response


@app.errorhandler(RateExceedError)
def handle_rate_error(ex):
    """
    This covers the exceptions raised by authentication failures.
    :param ex: Exception object
    :return:
    """
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response


@app.route("/limit")
@api_auth.requires_auth
@rate_limiter.check_limit
def get_limit():
    """
    This is used to create a endpoint for /limits
    :return:
    """
    return "Correct Request", 200


# if __name__ == "__main__":
#     app.run()

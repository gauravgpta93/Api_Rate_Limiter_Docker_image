from functools import wraps
from flask import request


class AuthError(Exception):
    """
    Authentication Error custom exception
    """
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


class AuthenticationChecker:
    """
    This checks if the request is correctly authenticated
    """
    def __init__(self, header):
        self._mandatory_header = header

    def requires_auth(self, func):
        """
        This is a decorator to check if the correct authentication is received in the request. Otherwise it raised an
        authentication error
        :param func: Decorator function to be called.
        :return: Decorator function if authentication successful else raises AuthError
        """

        @wraps(func)
        def decorator(*args, **kwargs):
            if self._check_header():
                # only when the header is present we go to the function
                return func(*args, **kwargs)
            else:
                raise AuthError({"code": "invalid_header",
                                 "description": "Unable to authenticate with the headers provided"}, 401)

        return decorator

    # ------------------------------------------Helper Functions--------------------------------------------------------
    def _check_header(self):
        """
        This function is used to check if a certain header exists in the system.
        :return: Boolean value based of existence of header
        """
        return bool(request.headers.get(self._mandatory_header, None))

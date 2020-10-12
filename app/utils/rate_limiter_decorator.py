import threading
import time
from collections import deque
from functools import wraps
from flask import request


class RateExceedError(Exception):
    """
    Custom Exception for exceeding the rate
    """

    def __init__(self, error, code):
        self.error = error
        self.status_code = code


class _UserObject:
    """
    This is the class which defines the object structure of each user. We use a Queue to keep track of the all the
    timestamps for accepted requests.
    """

    def __init__(self, total_requests, window_time_limit):
        """
        :param total_requests: Total Requests in the time window provided
        :param window_time_limit: The time window for the maximum requests (in seconds)
        """
        self._timestamps = deque()
        self._total_allowed = total_requests
        self._window_limit = window_time_limit
        self.lock = threading.Lock()

    def check_if_available(self, current_time):
        """
        Check if request can be accommodated in the given
        :param current_time:
        :return:
        """
        self._internal_clean_up(current_time)
        if len(self._timestamps) < self._total_allowed:
            return True
        return False

    def add_request(self, request_time):
        """
        This adds the current request time to the queue
        :param request_time: time of the request
        :return:
        """
        self._timestamps.append(request_time)

    # ------------------------------------------Helper Functions--------------------------------------------------------
    def _internal_clean_up(self, current_time):
        """
        This clears the queue for entries where the time window has elapsed
        :param current_time: current time in time.time()
        :return:
        """
        while self._timestamps and (current_time - self._timestamps[0] > self._window_limit):
            self._timestamps.popleft()


class RateLimiter:
    def __init__(self, total_requests=10, window_time_limit=1):
        """
        :param total_requests: Total Requests in the time window provided
        :param window_time_limit: The time window for the maximum requests (in seconds)
        """
        self._total_requests = total_requests
        self._window_limit = window_time_limit
        self._user_dict = dict()
        self._lock = threading.Lock()

    def check_limit(self, func):
        """
        This decorator function limits the rate for each user. It will raise error if the rate exceeds, otherwise it
        calls the function.
        :param func: Function on which decorator is called
        :return:
        """

        @wraps(func)
        def limiter_check(*args, **kwargs):
            user_id = request.headers.get("X-API-KEY", None)
            if not user_id:
                # We intentionally do not raise an exception here as this is an internal exception should be caught by
                # authentication decorator. This is a design choice as it helps to debug the code. However i have
                # provided the code for how to raise the exception.

                # raise AuthError({"code": "invalid_header",
                #                  "description": "Unable to authenticate with the headers provided"}, 401)
                pass

            if user_id and user_id not in self._user_dict:
                self._add_user(user_id)
            if self._check_request_added(user_id):
                return func(*args, **kwargs)
            else:
                raise RateExceedError({"code": "Exceeding request rate",
                                       "description": "Too many requests have been made from a single id. Please try"
                                                      " again after some time"},
                                      429)

        return limiter_check

    # ------------------------------------------Helper Functions--------------------------------------------------------
    def _add_user(self, user_id):
        """
        Creates and adds the user to the internal user dict.
        We use a lock in case of 2 different clients calling the same user id for the first time at the same time.
        :param user_id: User ID provided in the header
        :return:
        """
        with self._lock:
            self._user_dict[user_id] = _UserObject(self._total_requests, self._window_limit)

    def _check_request_added(self, user_id):
        """
        Tries to add the request if possible. If not it returns False
        We use a user object lock in case we have 2 different clients calling the same user id at the same time.
        :param user_id: User ID provided in the header
        :return: Returns True if request added, else returns False
        """
        user = self._user_dict[user_id]  # we do not use dict.get() to create exception here in case of internal error.
        with user.lock:
            current_time = time.time()
            if user.check_if_available(current_time):
                user.add_request(current_time)
                return True
            return False

from utils import log
from utils import find_item_by_json_path


class ResponseHandler:
    """Handle HTTP response using requests module and helper funcs."""

    def __init__(self, resp, status_code_check=True):
        """
        Performs status_code check if True.
        Logs response dody and headers.

        :param resp: Response object returned by HTTP request
        :param status_code_check: <bool>, check status_code or not
        """
        log(f'RESPONSE HEADERS: {resp.headers}')
        log(f'RESPONSE BODY: {resp.text}')
        if status_code_check:
            assert resp.status_code == 200, \
                f'Non-200 status code returned: {resp.status_code}'

    @staticmethod
    def get_status_code(resp):
        """
        Get status code of HTTP request.

        :param resp: Response object returned by HTTP request
        :return: status_code: <int> HTTP status code
        """
        status_code = resp.status_code
        return status_code

    @staticmethod
    def get_json_key_value(resp, key):
        """
        Gets JSON response key value.

        :param resp: Response object returned by HTTP request
        :param key: <str>, json response key
        :return: key value: <str>
        """
        actual_json = resp.json()
        value = find_item_by_json_path(actual_json, key)
        return value

import json

import requests

from utils import log
from utils.http_utils import (
    BaseUrl,
    BaseRequest
)


class PostRequest(BaseUrl, BaseRequest):
    """Performs POST HTTP request using requests module."""
    def __init__(self, path=''):
        """
        Initialises base url and endpoint path.

        :param path: <str> endpoint path
        """
        super().__init__()
        self.path = path

    def call(self, request_body, headers=None):
        """
        Performs POST HTTP request based on passed base url, path, request body, headers (optional).
        Logs request url, body, headers.

        :param request_body: <dict>
        :param headers: dictionary of POST request headers, , e.g. {'User-Agent': 'test'}
        :return: Response object returned by HTTP request.
        """
        resp = requests.post(self.base_url + self.path,
                             verify=False,
                             data=json.dumps(request_body),
                             headers=headers)

        log(f'POST REQUEST: {self.base_url + self.path}')
        log(f'POST REQUEST BODY: {request_body}')
        log(f'POST REQUEST HEADERS: {headers}')
        return resp

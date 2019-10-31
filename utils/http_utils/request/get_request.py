import requests

from utils import log
from utils.http_utils import (
    BaseUrl,
    BaseRequest
)


class GetRequest(BaseUrl, BaseRequest):
    """Performs GET HTTP request using requests module."""
    def __init__(self, path=''):
        """
        Initialises base url and endpoint path.

        :param path: <str> endpoint path
        """
        super().__init__()
        self.path = path

    def call(self, query_params=None, headers=None):
        """
        Performs GET HTTP request based on passed base_url, path, query params (optional), headers (optional).
        Logs request url, body, headers.

        :param query_params: dictionary of GET request query params, e.g. {'User-Agent': 'test'}
        :param headers: dictionary of GET request headers, e.g. {'key1': 'value1'}
        :return: Response object returned by HTTP request
        """
        resp = requests.get(self.base_url + self.path,
                            verify=False,
                            params=query_params,
                            headers=headers)

        log(f'GET REQUEST: {self.base_url + self.path}')
        log(f'GET REQUEST BODY: {query_params}')
        log(f'GET REQUEST HEADERS: {headers}')
        return resp

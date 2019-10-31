import requests

from utils import log
from utils.http_utils import (
    BaseUrl,
    BaseRequest
)


class DeleteRequest(BaseUrl, BaseRequest):
    """Performs DELETE HTTP request using requests module."""
    def __init__(self, path=''):
        """
        Initialises base url and endpoint path.

        :param path: <str> endpoint path
        """
        super().__init__()
        self.path = path

    def call(self, query_params=None, headers=None):
        """
        Performs DELETE HTTP request based on passed base_url, path, query params (optional), headers (optional).
        Logs request url, body, headers.

        :param query_params: dictionary of DELETE request query params, e.g. {'User-Agent': 'test'}
        :param headers: dictionary of DELETE request headers, e.g. {'key1': 'value1'}
        :return: Response object returned by HTTP request
        """
        resp = requests.delete(self.base_url + self.path,
                               verify=False,
                               params=query_params,
                               headers=headers)

        log(f'DELETE REQUEST: {self.base_url + self.path}')
        log(f'DELETE REQUEST BODY: {query_params}')
        log(f'DELETE REQUEST HEADERS: {headers}')
        return resp

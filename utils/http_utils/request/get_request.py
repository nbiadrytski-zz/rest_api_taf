import logging
from urllib.parse import urljoin

import requests

from utils.http_utils import BaseRequest


class GetRequest(BaseRequest):
    """Performs GET HTTP request using requests module."""

    def __init__(self, host, path):
        """
        Initialise GET request.

        :param host: environment host
        :param path: endpoint path
        """
        self.host = host
        self.path = path
        self.base_url = urljoin(self.host, self.path)
        self.logger = logging.getLogger(__name__)

    def call(self, query_params=None, headers=None):
        """
        Performs GET HTTP request.
        Based on passed base_url, query params (optional), headers (optional).

        :param query_params: dictionary of GET request query params, e.g. {'User-Agent': 'test'}
        :param headers: dictionary of GET request headers, e.g. {'key1': 'value1'}
        :return: Response object returned by HTTP request
        """
        resp = requests.get(self.base_url,
                            verify=False,
                            params=query_params,
                            headers=headers)

        self.logger.debug(f'GET REQUEST: {self.base_url}\n'
                          f'GET REQUEST PARAMS: {query_params}\n'
                          f'GET REQUEST HEADERS: {headers}\n')
        return resp

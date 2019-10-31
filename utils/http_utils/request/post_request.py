import logging
from urllib.parse import urljoin

import json
import requests

from utils.http_utils import BaseRequest


class PostRequest(BaseRequest):
    """Performs POST HTTP request using requests module."""

    def __init__(self, host, path):
        """
        Initialise POST request.

        :param host: environment host
        :param path: endpoint path
        """

        self.host = host
        self.path = path
        self.base_url = urljoin(self.host, self.path)
        self.logger = logging.getLogger(__name__)

    def call(self, request_body, headers=None):
        """
        Performs POST HTTP reques.
        Based on passed base_url, request body, headers (optional).

        :param request_body:<dict>
        :param headers: dictionary of POST request headers, , e.g. {'User-Agent': 'test'}
        :return: Response object returned by HTTP request.
        """
        resp = requests.post(self.base_url,
                             data=json.dumps(request_body),
                             headers=headers)

        self.logger.debug(f'POST REQUEST: {self.base_url}\n'
                          f'POST REQUEST BODY: {request_body}\n'
                          f'POST REQUEST HEADERS: {headers}\n')
        return resp

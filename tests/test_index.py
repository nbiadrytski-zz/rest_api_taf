import unittest

from utils.http_utils.request import GetRequest
from utils.http_utils.response import ResponseHandler
from tests.data.constants import MESSAGE
from utils import log


class TestIndex(unittest.TestCase):

    def test_index(self):
        """Check response message for server index."""
        log(f'RUNNING: {self.test_index.__name__} test.')

        resp = GetRequest().call()
        handler = ResponseHandler(resp)
        msg = handler.get_json_key_value(resp=resp,
                                         key=MESSAGE)

        self.assertEqual(msg, 'Simple Test Management System API',
                         f'Server index response message is incorrect: {msg}')

import unittest
import re

from utils.logger import log
from utils.http_utils.request import PostRequest
from utils.http_utils.response import ResponseHandler
from tests.data.constants import (
    APPLICATION_JSON,
    VALID_CREDS,
    TOKEN_REGEXP,
    INVALID_CREDS,
    TOKEN,
    LOGIN_PATH
)


class TestLogin(unittest.TestCase):

    def test_login(self):
        """Check that access_token can be obtained with valid credentials."""
        log(f'RUNNING: {self.test_login.__name__} test.')

        resp = PostRequest(path=LOGIN_PATH).call(request_body=VALID_CREDS,
                                                 headers=APPLICATION_JSON)
        handler = ResponseHandler(resp)
        access_token = handler.get_json_key_value(resp=resp,
                                                  key=TOKEN)
        # regexp is split into 3 groups:
        # 1. 36 character-long alpha-numeric string
        # 2. 196 character-long alpha-numeric string
        # 3. 43 character-long alpha-numeric string with -, _ characters allowed
        access_token_matches = re.match(TOKEN_REGEXP, access_token)

        self.assertIsNotNone(access_token_matches,
                             f'Access token does not match pattern: {TOKEN_REGEXP}')

    def test_login_invalid_creds_status_code(self):
        """Check 401 status code is returned when log in with invalid password."""
        log(f'RUNNING: {self.test_login_invalid_creds_status_code.__name__} test.')

        resp = PostRequest(path=LOGIN_PATH).call(request_body=INVALID_CREDS,
                                                 headers=APPLICATION_JSON)
        handler = ResponseHandler(resp=resp,
                                  status_code_check=False)
        status_code = handler.get_status_code(resp)

        self.assertEqual(status_code, 401,
                         f'Status code is not 401. Actual status code: {status_code}')

    def test_login_invalid_creds_message(self):
        """Check response message when log in with invalid password."""
        log(f'RUNNING: {self.test_login_invalid_creds_message.__name__} test')

        resp = PostRequest(path=LOGIN_PATH).call(request_body=INVALID_CREDS,
                                                 headers=APPLICATION_JSON)
        handler = ResponseHandler(resp=resp,
                                  status_code_check=False)
        msg = handler.get_json_key_value(resp=resp,
                                         key='message')
        expected_msg = 'No such username or password'

        self.assertEqual(msg, expected_msg,
                         f'Expected "{expected_msg}" message in response, but got: {msg}')

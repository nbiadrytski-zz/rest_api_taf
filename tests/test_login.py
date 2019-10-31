import logging
import re

import pytest

from utils.http_utils.request import PostRequest
from utils.http_utils.response import ResponseHandler
from utils.helper_funcs import get_from_json_path_config
from utils.constants import (
    BASE_PATH,
    APPLICATION_JSON,
    VALID_CREDS,
    TOKEN_REGEXP,
    INVALID_CREDS
)


LOGGER = logging.getLogger()


@pytest.mark.login
def test_login(host):
    """
    Check that access_token can be obtained with valid credentials.

    :param host: setup fixture to set request host+port, e.g. http://127.0.0.1:5000
    """
    LOGGER.info('Testing that access_token can be obtained with valid credentials.')
    resp = PostRequest(host, f'{BASE_PATH}/login').call(request_body=VALID_CREDS,
                                                        headers=APPLICATION_JSON)
    validator = ResponseHandler(resp)

    access_token = validator.get_value_from_json(resp=resp,
                                                 json_path=get_from_json_path_config('token'))
    # regexp is split into 3 groups:
    # 1. 36 character-long alpha-numeric string
    # 2. 196 character-long alpha-numeric string
    # 3. 43 character-long alpha-numeric string with -, _ characters allowed
    access_token_matches = re.match(TOKEN_REGEXP, access_token)

    assert access_token_matches is not None, \
        f'Access token does not match pattern: {TOKEN_REGEXP}'


@pytest.mark.login
def test_login_invalid_creds_status_code(host):
    """
    Check that 401 status code is returned when log in with invalid password.

    :param host: setup fixture to set request host+port, e.g. http://127.0.0.1:5000
    """
    LOGGER.info('Testing 401 status code returned when log in with invalid password.')
    resp = PostRequest(host, f'{BASE_PATH}/login').call(request_body=INVALID_CREDS,
                                                        headers=APPLICATION_JSON)
    validator = ResponseHandler(resp, status_code_check=False)

    status_code = validator.get_status_code(resp=resp)

    assert status_code == 401, \
        f'Status code is not 401. Actual status code: {status_code}'


@pytest.mark.login
def test_login_invalid_creds_message(host):
    """
    Check response message when log in with invalid password.

    :param host: setup fixture to set request host+port, e.g. http://127.0.0.1:5000
    """
    LOGGER.info('Testing response message when log in with invalid password.')
    resp = PostRequest(host, f'{BASE_PATH}/login').call(request_body=INVALID_CREDS,
                                                        headers=APPLICATION_JSON)
    validator = ResponseHandler(resp, status_code_check=False)

    msg = validator.get_value_from_json(resp=resp,
                                        json_path=get_from_json_path_config('message'))

    assert msg == 'No such username or password', \
        f'Unexpected message in response body: {msg}'

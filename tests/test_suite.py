import logging

import pytest

from utils.http_utils.request import PostRequest
from utils.http_utils.response import ResponseHandler
from utils.helper_funcs import get_from_json_path_config
from utils.constants import (
    BASE_PATH,
    TEST_SUITE,
    APPLICATION_XML,
    APPLICATION_JSON
)


LOGGER = logging.getLogger()


@pytest.mark.suite
def test_create_suite(host, auth_header, delete_suite):
    """
    Check that test suite can be created.

    :param host: setup fixture to set request host+port, e.g. http://127.0.0.1:5000
    :param auth_header: authorisation token fixture
    :param delete_suite: teardown fixture
    """
    LOGGER.info('Testing test suite creation.')
    resp = PostRequest(host, f'{BASE_PATH}/test_suites').call(request_body=TEST_SUITE,
                                                              headers={**APPLICATION_JSON, **auth_header})
    validator = ResponseHandler(resp)

    msg = validator.get_value_from_json(resp=resp,
                                        json_path=get_from_json_path_config('message'))
    suite_id = validator.get_value_from_json(resp=resp,
                                             json_path=get_from_json_path_config('id'))

    delete_suite(suite_id)

    assert msg == 'Test suite successfully added', \
        f'Unexpected message in response body: {msg}.'


@pytest.mark.suite
def test_create_suite_invalid_content_type_status_code(host, auth_header):
    """
    Check 415 status code returned with 'Content-Type': 'application/xml' request header for suite creation.

    :param host: setup fixture to set request host+port, e.g. http://127.0.0.1:5000
    :param auth_header: authorisation token fixture
    """
    LOGGER.info('Testing 415 status code returned with invalid request header for suite creation')
    resp = PostRequest(host, f'{BASE_PATH}/test_suites').call(request_body=TEST_SUITE,
                                                              headers={**APPLICATION_XML, **auth_header})
    validator = ResponseHandler(resp, status_code_check=False)
    status_code = validator.get_status_code(resp)

    assert status_code == 415, \
        f'Expected 415 status code, but {status_code} returned.'


@pytest.mark.suite
def test_create_suite_invalid_content_type_message(host, auth_header):
    """
    Check response message with 'Content-Type': 'application/xml' request header.

    :param host: setup fixture to set request host+port, e.g. http://127.0.0.1:5000
    :param auth_header: authorisation token fixture
    """
    LOGGER.info('Testing response messafe for suite creation with invalid request header.')
    resp = PostRequest(host, f'{BASE_PATH}/test_suites').call(request_body=TEST_SUITE,
                                                              headers={**APPLICATION_XML, **auth_header})
    validator = ResponseHandler(resp, status_code_check=False)
    msg = validator.get_value_from_json(resp=resp,
                                        json_path=get_from_json_path_config('message'))

    assert msg == 'Content-type must be application/json', \
        f'Unexpected message in response body: {msg}'

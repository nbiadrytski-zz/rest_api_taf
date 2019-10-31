import logging

import pytest

from utils.http_utils.request import PostRequest
from utils.http_utils.response import ResponseHandler
from utils.helper_funcs import (
    case_body,
    get_from_json_path_config
)
from utils.constants import (
    BASE_PATH,
    APPLICATION_JSON,
    CASE_TITLE,
    CASE_DESCRIPTION,
    NON_EXISTING_SUITE_ID,
    CASE_NO_SUITE_ID
)


LOGGER = logging.getLogger()


@pytest.mark.case
def test_create_case(create_suite,
                     host,
                     auth_header,
                     delete_suite,
                     delete_case):
    """
    Check that test case can be created.

    :param create_suite: setup fixture to create a test suite
    :param host: setup fixture to set request host+port, e.g. http://127.0.0.1:5000
    :param auth_header: authorisation token fixture
    :param delete_suite: fixture to delete test suite
    :param delete_case: fixture to delete test case
    """
    suite_id = create_suite

    LOGGER.info('Testing test case creation.')
    resp = PostRequest(host, f'{BASE_PATH}/test_cases')\
        .call(request_body=case_body(suite_id, CASE_TITLE, CASE_DESCRIPTION),
              headers={**APPLICATION_JSON, **auth_header})
    validator = ResponseHandler(resp)

    msg = validator.get_value_from_json(resp=resp,
                                        json_path=get_from_json_path_config('message'))
    case_id = validator.get_value_from_json(resp=resp,
                                            json_path=get_from_json_path_config('id'))

    # deleting just created test suite and test case
    delete_case(case_id)
    delete_suite(suite_id)

    assert msg == 'Test case successfully added', \
        f'Unexpected message in response body: {msg}'


@pytest.mark.case
def test_create_case_for_nonexisting_suite_message(host, auth_header):
    """
    Check response message when trying to create test case for non-existing test suite.

    :param host: setup fixture to set request host+port, e.g. http://127.0.0.1:5000
    :param auth_header: authorisation token fixture
    """
    LOGGER.info('Testing response message when trying to create test case for non-existing test suite')
    resp = PostRequest(host, f'{BASE_PATH}/test_cases')\
        .call(request_body=case_body(NON_EXISTING_SUITE_ID, CASE_TITLE, CASE_DESCRIPTION),
              headers={**APPLICATION_JSON, **auth_header})
    validator = ResponseHandler(resp, status_code_check=False)

    msg = validator.get_value_from_json(resp=resp,
                                        json_path=get_from_json_path_config('message'))

    assert msg == 'Test suite does not exist', \
        f'Unexpected message in response body: {msg}'


@pytest.mark.case
def test_create_case_for_nonexisting_suite_code(host, auth_header):
    """
    Check response message when trying to create test case for non-existing test suite.

    :param host: setup fixture to set request host+port, e.g. http://127.0.0.1:5000
    :param auth_header: authorisation token fixture
    """
    LOGGER.info('Testing status codee when trying to create test case for non-existing test suite')
    resp = PostRequest(host, f'{BASE_PATH}/test_cases')\
        .call(request_body=case_body(NON_EXISTING_SUITE_ID, CASE_TITLE, CASE_DESCRIPTION),
              headers={**APPLICATION_JSON, **auth_header})
    validator = ResponseHandler(resp, status_code_check=False)

    status_code = validator.get_status_code(resp=resp)

    assert status_code == 404, \
        f'Status code is {status_code}, but 404 is expected.'


@pytest.mark.case
def test_create_case_without_suite_id_code(host, auth_header):
    """
    Check status code when trying to create test case without suite_id.

    :param host: setup fixture to set request host+port, e.g. http://127.0.0.1:5000
    :param auth_header: authorisation token fixture
    """
    LOGGER.info('Testing status code when trying to create test case without suite_id.')
    resp = PostRequest(host, f'{BASE_PATH}/test_cases')\
        .call(request_body=CASE_NO_SUITE_ID,
              headers={**APPLICATION_JSON, **auth_header})
    validator = ResponseHandler(resp, status_code_check=False)

    status_code = validator.get_status_code(resp=resp)

    assert status_code == 400, \
        f'Status code is {status_code}, but 404 is expected.'


@pytest.mark.case
def test_create_case_without_suite_id_message(host, auth_header):
    """
    Check response message when trying to create test case without suite_id.

    :param host: setup fixture to set request host+port, e.g. http://127.0.0.1:5000
    :param auth_header: authorisation token fixture
    """
    LOGGER.info('Testing response message when trying to create test case without suite_id.')
    resp = PostRequest(host, f'{BASE_PATH}/test_cases')\
        .call(request_body=CASE_NO_SUITE_ID,
              headers={**APPLICATION_JSON, **auth_header})
    validator = ResponseHandler(resp, status_code_check=False)

    msg = validator.get_value_from_json(resp=resp,
                                        json_path=get_from_json_path_config('message'))

    assert msg == 'Bad request body', \
        f'Unexpected message in response body: {msg}'

import logging
import re

from pytest import (
    fixture,
    hookimpl
)

from utils.errors import NoEnvArgException
from utils.http_utils.request import (
    PostRequest,
    DeleteRequest
)
from utils.http_utils.response import ResponseHandler
from utils.helper_funcs import (
    get_host,
    get_from_json_path_config
)
from utils.constants import (
    BASE_PATH,
    APPLICATION_JSON,
    VALID_CREDS,
    TEST_SUITE,
    TOKEN_REGEXP
)


LOGGER = logging.getLogger()


def pytest_addoption(parser):
    """Adds command line arg '--env' to define environment for tests"""
    parser.addoption('--env', action='store', help='Env to run tests against')


@fixture(scope='session')
def env(request):
    """
    Pytest built-in request keeps all command line session info.
    Raises custom NoEnvArgException if --env command line arg was not passed.
    """
    if request.config.getoption('--env') is None:
        raise NoEnvArgException(request.config.getoption('--env'))
    return request.config.getoption('--env')


@fixture(scope='session')
def host(env):
    """
    Returns environment host (e.g. http://127.0.0.1:5000).
    Based on passed commannd-line arg '--env'.
    Pass this fixture to each test method.

    :param env:<str> desired environment, e.g. dev, uat, etc.
    :return: current_host:<str>, e.g. http://127.0.0.1:5000
    """
    current_host = get_host(env)
    return current_host


@fixture(scope='function')
def auth_header(host):
    """
    Returns auth header (used for logging in) as dict by calling api/v1/login endpoint.

    :param host: setup fixture to set request host+port, e.g. http://127.0.0.1:5000
    :return: Authorization header <dict>
    """
    resp = PostRequest(host, f'{BASE_PATH}/login').\
        call(request_body=VALID_CREDS,
             headers=APPLICATION_JSON)
    validator = ResponseHandler(resp)
    access_token = validator.\
        get_value_from_json(resp=resp,
                            json_path=get_from_json_path_config('token'))
    access_token_matches = re.match(TOKEN_REGEXP, access_token)
    assert access_token_matches is not None, \
        f'Access token does not match pattern: {TOKEN_REGEXP}'

    return {'Authorization': f'Bearer {access_token}'}


@fixture(scope='function')
def delete_suite(host, auth_header):
    """
    Used as teardown fixture to delete test suite.
    By calling DELETE api/v1/test_suites/<test_suite_id> endpoint.

    :param host: setup fixture to set request host+port, e.g. http://127.0.0.1:5000
    :param auth_header: authorisation token fixture
    :return: delete function
    """

    def delete(suite_id):
        resp = DeleteRequest(host, f'{BASE_PATH}/test_suites/{suite_id}').\
            call(headers={**APPLICATION_JSON, **auth_header})
        msg = ResponseHandler(resp).\
            get_value_from_json(resp=resp,
                                json_path=get_from_json_path_config('message'))
        if not re.search(r'Test suite successfully deleted', msg):
            LOGGER.warning(msg)

    return delete


@fixture(scope='function')
def delete_case(host, auth_header):
    """
    Used as teardown fixture to delete test case.
    By calling DELETE api/v1/test_cases/<test_case_id> endpoint.

    :param host: setup fixture to set request host+port, e.g. http://127.0.0.1:5000
    :param auth_header: authorisation token fixture
    :return: delete function
    """

    def delete(case_id):
        resp = DeleteRequest(host, f'{BASE_PATH}/test_cases/{case_id}').\
            call(headers={**APPLICATION_JSON, **auth_header})
        msg = ResponseHandler(resp).\
            get_value_from_json(resp=resp,
                                json_path=get_from_json_path_config('message'))
        if not re.search(r'Test case successfully deleted', msg):
            LOGGER.warning(msg)

    return delete


@fixture(scope='function')
def create_suite(host, auth_header):
    """
    Used as setup fixture to create test suite.
    By calling POST api/v1/test_suites endpoint.

    :param host: setup fixture to set request host+port, e.g. http://127.0.0.1:5000
    :param auth_header: authorisation token fixture
    :return: suite_id<str>
    """
    resp = PostRequest(host, f'{BASE_PATH}/test_suites').\
        call(request_body=TEST_SUITE,
             headers={**APPLICATION_JSON, **auth_header})
    suite_id = ResponseHandler(resp).\
        get_value_from_json(resp=resp,
                            json_path=get_from_json_path_config('id'))
    assert suite_id, \
        f'Cannot get suite_id when creating test suite: {suite_id}'
    return suite_id


def pytest_sessionstart(session):
    """Create the results attributed for the session instance."""
    session.results = dict()


@hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item):
    """Add test result to session.results once result is ready."""
    outcome = yield
    result = outcome.get_result()

    if result.when == 'call':
        item.session.results[item] = result


def pytest_sessionfinish(session, exitstatus):
    """Print overall test execution status."""
    print('\nExit code:', exitstatus)
    passed = sum(
        1 for result in session.results.values() if result.outcome == 'passed')
    failed = sum(
        1 for result in session.results.values() if result.failed)
    skipped = sum(
        1 for result in session.results.values() if result.skipped)
    print(f'There were {passed} tests passed, {failed} tests failed, '
          f'{skipped} tests skipped.')

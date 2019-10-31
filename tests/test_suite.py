import unittest

from utils import log
from tests.app_client import AppClient
from utils.http_utils.request import PostRequest
from utils.http_utils.response import ResponseHandler
from tests.data.constants import (
    TEST_SUITE,
    APPLICATION_XML,
    APPLICATION_JSON,
    CREATE_SUITE_PATH,
    MESSAGE,
    ID
)


app_client = AppClient()


class TestCreateSuite(unittest.TestCase):

    def setUp(self):
        """Creates Authorisation request header for each test method."""
        log(f'RUNNING SETUP (auth_header) for: {self.test_create_suite.__name__} test.')

        self.auth_header = app_client.auth_header()

    def tearDown(self):
        """Deletes test suite created in test method."""
        log(f'RUNNING TEARDOWN (delete_suite) for: {self.test_create_suite.__name__} test')

        app_client.delete_suite(self.suite_id)

    def test_create_suite(self):
        """Check that test suite can be created."""
        log(f'RUNNING: {self.test_create_suite.__name__} test.')

        resp = PostRequest(path=CREATE_SUITE_PATH).call(request_body=TEST_SUITE,
                                                        headers={**APPLICATION_JSON,
                                                                 **self.auth_header})
        validator = ResponseHandler(resp)
        msg = validator.get_json_key_value(resp=resp,
                                           key=MESSAGE)
        self.suite_id = validator.get_json_key_value(resp=resp,
                                                     key=ID)

        self.assertEqual(msg, 'Test suite successfully added',
                         f'Test suite creation failed. See message in response: "{msg}"')


class TestCreateSuiteNegativeScenarios(unittest.TestCase):

    def setUp(self):
        """Creates Authorisation request header for each test method."""
        log(f'RUNNING SETUP (auth_header) for: {self._testMethodName} test.')

        self.auth_header = app_client.auth_header()

    def test_create_suite_invalid_content_type_status_code(self):
        """Check 415 status code returned with invalid request header for suite creation."""
        log(f'RUNNING: {self.test_create_suite_invalid_content_type_status_code.__name__} test.')

        resp = PostRequest(path=CREATE_SUITE_PATH).call(request_body=TEST_SUITE,
                                                        headers={**APPLICATION_XML,
                                                                 **self.auth_header})
        handler = ResponseHandler(resp=resp,
                                  status_code_check=False)
        status_code = handler.get_status_code(resp)

        self.assertEqual(status_code, 415,
                         f'Expected 415 status code, but {status_code} was returned.')

    def test_create_suite_invalid_content_type_message(self):
        """Check response message with invalid request header for suite creation."""
        log(f'RUNNING: {self.test_create_suite_invalid_content_type_message.__name__} test.')

        resp = PostRequest(CREATE_SUITE_PATH).call(request_body=TEST_SUITE,
                                                   headers={**APPLICATION_XML,
                                                            **self.auth_header})
        validator = ResponseHandler(resp=resp,
                                    status_code_check=False)
        msg = validator.get_json_key_value(resp=resp,
                                           key=MESSAGE)

        self.assertEqual(msg, 'Content-type must be application/json',
                         f'Content-type is not application/json. See response body message: "{msg}"')

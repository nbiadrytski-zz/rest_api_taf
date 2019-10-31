import unittest

from utils.logger import log
from tests.app_client import AppClient
from utils.http_utils.request import PostRequest
from utils.http_utils.response import ResponseHandler
from utils.helper_funcs import case_body
from tests.data.constants import (
    APPLICATION_JSON,
    CASE_TITLE,
    CASE_DESCRIPTION,
    NON_EXISTING_SUITE_ID,
    CASE_NO_SUITE_ID,
    CREATE_CASE_PATH,
    MESSAGE,
    ID
)


app_client = AppClient()


class TestCreateCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Creates test suite."""
        log(f'RUNNING SETUP (create_suite) for: {TestCreateCase.__name__} class.')

        cls.suite_id = app_client.create_suite()

    @classmethod
    def tearDownClass(cls):
        """Deletes test suite created in setUpClass()."""
        log(f'RUNNING TEARDOWN (delete_suite) for: {TestCreateCase.__name__} class.')

        app_client.delete_suite(cls.suite_id)

    def setUp(self):
        """Creates Authorisation header for each test method."""
        log(f'RUNNING SETUP (auth_header) for: {self._testMethodName} test.')

        self.auth_header = app_client.auth_header()

    def tearDown(self):
        """Deletes test case created in test method."""
        log(f'RUNNING TEARDOWN (delete_case) for: {self._testMethodName} test.')

        app_client.delete_case(self.case_id)

    def test_create_case(self):
        """Check that test case can be created."""
        log(f'RUNNING: {self.test_create_case.__name__} test.')

        resp = PostRequest(path=CREATE_CASE_PATH).call(
            request_body=case_body(self.suite_id,
                                   CASE_TITLE,
                                   CASE_DESCRIPTION),
            headers={**APPLICATION_JSON,
                     **self.auth_header})
        handler = ResponseHandler(resp)
        msg = handler.get_json_key_value(resp=resp,
                                         key=MESSAGE)
        # get test case id to be deleted in tearDown()
        self.case_id = handler.get_json_key_value(resp=resp,
                                                  key=ID)

        self.assertEqual(msg, 'Test case successfully added',
                         f'Test case creation failed. See response message: "{msg}"')


class TestCreateCaseNegativeScenarios(unittest.TestCase):

    def setUp(self):
        """Creates Authorisation request header for each test method."""
        log(f'RUNNING SETUP (auth_header) for: {self._testMethodName} test.')

        self.auth_header = app_client.auth_header()

    def test_create_case_for_nonexisting_suite_message(self):
        """Check response message when trying to create test case for non-existing test suite."""
        log(f'RUNNING: {self.test_create_case_for_nonexisting_suite_message.__name__} test.')

        resp = PostRequest(path=CREATE_CASE_PATH).call(
            request_body=case_body(NON_EXISTING_SUITE_ID,
                                   CASE_TITLE,
                                   CASE_DESCRIPTION),
            headers={**APPLICATION_JSON,
                     **self.auth_header})
        handler = ResponseHandler(resp=resp,
                                  status_code_check=False)
        msg = handler.get_json_key_value(resp=resp,
                                         key=MESSAGE)

        self.assertEqual(msg, 'Test suite does not exist',
                         f'Test suite should not exist, but got this message in response body: "{msg}"')

    def test_create_case_for_nonexisting_suite_code(self):
        """Check status code when trying to create test case for non-existing test suite."""
        log(f'RUNNING: {self.test_create_case_for_nonexisting_suite_code.__name__} test.')

        resp = PostRequest(path=CREATE_CASE_PATH).call(
            request_body=case_body(NON_EXISTING_SUITE_ID,
                                   CASE_TITLE,
                                   CASE_DESCRIPTION),
            headers={**APPLICATION_JSON,
                     **self.auth_header})
        handler = ResponseHandler(resp=resp,
                                  status_code_check=False)
        status_code = handler.get_status_code(resp)

        self.assertEqual(status_code, 404,
                         f'Expected 404 status code, but {status_code} was returned.')

    def test_create_case_without_suite_id_code(self):
        """Check status code when trying to create test case without suite_id."""
        log(f'RUNNING: {self.test_create_case_without_suite_id_code.__name__} test.')

        resp = PostRequest(path=CREATE_CASE_PATH).call(
            request_body=CASE_NO_SUITE_ID,
            headers={**APPLICATION_JSON,
                     **self.auth_header})
        handler = ResponseHandler(resp=resp,
                                  status_code_check=False)
        status_code = handler.get_status_code(resp)

        self.assertEqual(status_code, 400,
                         f'Expected 400 status code, but {status_code} was returned.')

    def test_create_case_without_suite_id_message(self):
        """Check response message when trying to create test case without suite_id."""
        log(f'RUNNING: {self.test_create_case_without_suite_id_message.__name__} test.')

        resp = PostRequest(path=CREATE_CASE_PATH).call(
            request_body=CASE_NO_SUITE_ID,
            headers={**APPLICATION_JSON,
                     **self.auth_header})
        handler = ResponseHandler(resp=resp,
                                  status_code_check=False)

        msg = handler.get_json_key_value(resp=resp,
                                         key='message')

        self.assertEqual(msg, 'Bad request body',
                         f'Expected "Bad request body" response message, but got: "{msg}"')

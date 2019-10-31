import re

from utils import log
from utils.http_utils.response import ResponseHandler
from utils.http_utils.request import (
    PostRequest,
    DeleteRequest
)
from tests.data.constants import (
    VALID_CREDS,
    APPLICATION_JSON,
    TOKEN,
    TOKEN_REGEXP,
    MESSAGE,
    TEST_SUITE,
    ID,
    LOGIN_PATH,
    CREATE_SUITE_PATH,
    DELETE_CASE_PATH,
    DELETE_SUITE_PATH
)


class AppClient:
    """Provides app-related setup and teardown methods for tests."""

    @staticmethod
    def auth_header():
        """
        Returns auth header (used for logging in) as dict by calling POST api/v1/login endpoint.

        :return: authorisation header: <dict>
        """
        resp = PostRequest(path=LOGIN_PATH).call(request_body=VALID_CREDS,
                                                 headers=APPLICATION_JSON)
        handler = ResponseHandler(resp)
        access_token = handler.get_json_key_value(resp=resp,
                                                  key=TOKEN)
        access_token_matches = re.match(TOKEN_REGEXP, access_token)
        assert access_token_matches is not None, \
            f'Access token does not match pattern: {TOKEN_REGEXP}'

        return {'Authorization': f'Bearer {access_token}'}

    @staticmethod
    def create_suite():
        """
        Creates test suite by calling POST api/v1/test_suites endpoint.

        :return: suite_id: <str>, test suite id
        """
        resp = PostRequest(path=CREATE_SUITE_PATH).call(request_body=TEST_SUITE,
                                                        headers={**APPLICATION_JSON,
                                                                 **AppClient.auth_header()})
        suite_id = ResponseHandler(resp).get_json_key_value(resp=resp,
                                                            key=ID)
        assert suite_id, f'Suite creation failed. See suite_id: {suite_id}'

        return suite_id

    @staticmethod
    def delete_suite(suite_id):
        """
        Delete test suite by calling DELETE api/v1/test_suites/<test_suite_id> endpoint.

        :param suite_id: <str>, test suite id
        """
        resp = DeleteRequest(path=DELETE_SUITE_PATH + suite_id).call(
            headers={**APPLICATION_JSON,
                     **AppClient.auth_header()})
        msg = ResponseHandler(resp).get_json_key_value(resp=resp,
                                                       key=MESSAGE)
        try:
            assert msg == 'Test suite successfully deleted', \
                f'Cannot delete test suite with id: {suite_id}'
        except AssertionError as e:
            log(e, 'warning')

    @staticmethod
    def delete_case(case_id):
        """
        Deletes test case by calling DELETE api/v1/test_cases/<test_case_id> endpoint.

        :param case_id: <str>, test case id
        """
        resp = DeleteRequest(path=DELETE_CASE_PATH + case_id).call(
            headers={**APPLICATION_JSON, **AppClient.auth_header()})
        msg = ResponseHandler(resp).get_json_key_value(resp=resp,
                                                       key=MESSAGE)
        try:
            assert msg == 'Test case successfully deleted', \
                f'Cannot delete test case with id: {case_id}'
        except AssertionError as e:
            log(e, 'warning')

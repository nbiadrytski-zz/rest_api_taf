import logging

from utils.helper_funcs import (
    find_item_by_jsonpath,
    file_content,
    convert_json_to_dict,
    compare_dicts
)
from utils.config_parser import DataConfigParser
from utils.constants import JSON_KEYS_CONFIG_PATH


class ResponseHandler:
    """
    Validate HTTP response using requests module and helper funcs.
    Log request status code, response headers and body when ResponseHandler object is created.

    Parameters:
        resp (Response): Response object returned by HTTP request.
    """

    def __init__(self, resp, status_code_check=True):
        """
        Initialise ResponseHandler.
        Log status code, response headers and response body.
        Status code validation.

        :param resp: Response object returned by HTTP request
        :param status_code_check:<bool> check staust code or not
        """
        self.logger = logging.getLogger(__name__)
        self.logger.debug(f'STATUS CODE: {resp.status_code}\n')
        self.logger.debug(f'RESPONSE HEADERS: {resp.headers}\n')
        self.logger.debug(f'RESPONSE BODY: {resp.text}\n')
        if status_code_check:
            assert resp.status_code == 200, \
                f'Non-200 status code returned: {resp.status_code}'

    @staticmethod
    def get_status_code(resp):
        """
        Get status code of HTTP request.

        :param resp: Response object returned by HTTP request
        :return: status_code:<int> HTTP status code
        """
        status_code = resp.status_code
        return status_code

    @staticmethod
    def get_response_header(resp, header_name):
        """
        Get response header of HTTP request.

        :param resp: Response object returned by HTTP request
        :param header_name:<str> response header name
        :return: response_header:<str> response header value
        """
        response_header = resp.headers[header_name]
        return response_header

    @staticmethod
    def get_value_from_json(resp, json_path):
        """
        Get JSON key value by provided json path.

        :param resp: Response object returned by HTTP request.
        :param json_path:<str> path to JSON key
        :return: value:<str> JSON key value
        """
        actual_json = resp.json()
        value = find_item_by_jsonpath(actual_json, json_path)
        return value

    @staticmethod
    def response_equals(actual_response, expected_response):
        """
        Compare actual HTTP response in plain text with expected response stored in .txt file.

        :param actual_response: Response object returned by HTTP request
        :param expected_response:<str> relative path to txt file with expected content
        :return: <bool> True if actual_response has the same content as expected_response, otherwise False
        """
        expected_response = file_content(expected_response)
        return actual_response.text == expected_response

    @staticmethod
    def contains(resp):
        """
        Get response as text.

        :param resp: Response object returned by HTTP request.
        :return: text_response:<str>
        """
        text_response = resp.text
        return text_response

    @staticmethod
    def json_response_equals(actual_response,
                             expected_response,
                             config_section_title,
                             ignore_keys=()):
        """
        Check if actual JSON response has the same content as expected response stored in .json file.

        1. Get json_keys_config.ini by creating DataConfigParser object (provide path to config file).
        2. Convert actual json response to dict.
        3. Convert expected json response from .json file to dict.
        4. Compare 2 dicts and log diff if they do not match.

        :param actual_response: Response object returned by HTTP request
        :param expected_response: path to .json file with stored expected response
        :param config_section_title: tile of config.ini section
        :param ignore_keys:<tuple> optional, a tuple of config.ini keys to be ignored when comparing responses
        :return: <bool> whether actual and expected responses match
        """
        config_parser = DataConfigParser(JSON_KEYS_CONFIG_PATH)
        ignored_keys = config_parser.get_ignored_keys(config_section_title, ignore_keys)
        actual_response = actual_response.json()
        expected_response = convert_json_to_dict(expected_response)
        responses_match = compare_dicts(actual_response, expected_response, ignored_keys)
        return responses_match

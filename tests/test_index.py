import logging

import pytest

from utils.http_utils.request import GetRequest
from utils.http_utils.response import ResponseHandler
from utils.constants import BASE_PATH
from utils.helper_funcs import get_from_json_path_config


LOGGER = logging.getLogger()


@pytest.mark.index
def test_index(host):
    """
    Check response message for server index.

    :param host: setup fixture to set request host+port, e.g. http://127.0.0.1:5000
    """
    LOGGER.info('Testing server index response message.')
    resp = GetRequest(host, BASE_PATH).call()
    validator = ResponseHandler(resp)

    msg = validator.get_value_from_json(resp=resp,
                                        json_path=get_from_json_path_config('message'))

    assert msg == 'Simple Test Management System API',\
        f'Unexpected message in response: {msg}'

"""Contains common variables used across the project."""

import uuid

from pathlib import Path


THIS_FILE_PATH = Path().resolve().parent

ENVS_CONFIG_PATH = THIS_FILE_PATH.joinpath('utils/data/envs_config.ini')

JSON_KEYS_CONFIG_PATH = THIS_FILE_PATH.joinpath('utils/data/json_keys_config.ini')

BASE_PATH = '/api/v1'

APPLICATION_JSON = {"Content-Type": "application/json"}

APPLICATION_XML = {"Content-Type": "application/xml"}

AUTH_HEADER = {'Authorization': 'auth_header_value'}

VALID_CREDS = {"username": "test", "password": "test"}

INVALID_CREDS = {"username": "test", "password": "test1"}

TOKEN_REGEXP = r'^[a-zA-Z0-9]{36}\.[a-zA-Z0-9]{194}\.[a-zA-Z0-9\-_]{43}$'

TEST_SUITE = {"title": str(uuid.uuid4())}

CASE_TITLE = 'case title: ' + str(uuid.uuid4())

CASE_DESCRIPTION = 'case description: ' + str(uuid.uuid4())

NON_EXISTING_SUITE_ID = str(uuid.uuid4())

CASE_NO_SUITE_ID = {"title": "test case title",
                    "description": "test case description"}

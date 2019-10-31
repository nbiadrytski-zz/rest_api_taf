import uuid


# HTTP request data
BASE_HOST = 'http://127.0.0.1:5000'
BASE_PATH = '/api/v1'
LOGIN_PATH = '/login'
CREATE_SUITE_PATH = '/test_suites'
CREATE_CASE_PATH = '/test_cases'
DELETE_SUITE_PATH = '/test_suites/'
DELETE_CASE_PATH = '/test_cases/'

# Request headers
APPLICATION_JSON = {"Content-Type": "application/json"}
APPLICATION_XML = {"Content-Type": "application/xml"}

# Tests request body
VALID_CREDS = {"username": "test", "password": "test"}
INVALID_CREDS = {"username": "test", "password": "test1"}
TEST_SUITE = {"title": str(uuid.uuid4())}
CASE_TITLE = 'case title: ' + str(uuid.uuid4())
CASE_DESCRIPTION = 'case description: ' + str(uuid.uuid4())
NON_EXISTING_SUITE_ID = str(uuid.uuid4())
CASE_NO_SUITE_ID = {"title": "test case title",
                    "description": "test case description"}

TOKEN_REGEXP = r'^[a-zA-Z0-9]{36}\.[a-zA-Z0-9]{194}\.[a-zA-Z0-9\-_]{43}$'

# Response json paths
MESSAGE = 'message'
ID = 'id'
TOKEN = 'access_token'

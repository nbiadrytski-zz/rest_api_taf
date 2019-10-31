*** Settings ***
Documentation    Test fixtures mostly used for setup and teardown.

Library          RequestsLibrary
Library          ../libraries/helper_funcs.py
Resource         http_keywords.robot
Variables        ../data/variables.py


*** Keywords ***
Get Access Token
    [Documentation]   Get access_token using Get Token keyword.
    ...               Set access_token as Test Variable to be used in Test Setup.
    ${ACCESS_TOKEN}=   Get Token
    Set Test Variable   ${ACCESS_TOKEN}

Create Test Suite
    [Documentation]   Create test suite by POST api/v1/test_suites endpoint.
    ...               Set suite_id as Suite Variable to be used in Suite Setup.
    ${ACCESS_TOKEN}=   Get Token
    ${HEADERS}=   Request Headers   ${APPLICATION_JSON}
    ...                             ${ACCESS_TOKEN}
    ${RESPONSE}=   Post Call
    ...   PATH=${CREATE_SUITE_PATH}
    ...   BODY=${TEST_SUITE}
    ...   HEADERS=${HEADERS}
    ${MESSAGE}=   Get Json Key Value   ${RESPONSE}   ${MESSAGE}
    ${SUITE_ID}=   Get Json Key Value   ${RESPONSE}   ${ID}
    Should Be Equal As Strings   ${MESSAGE}   Test suite successfully added
    Set Suite Variable  ${SUITE_ID}

Delete Test Suite
    [Documentation]   Delete test suite by calling DELETE api/v1/test_suites/<suite_id> endpoint.
    ...               Can be used in Test or Suite Setup.
    [Arguments]   ${SUITE_ID}=
    ${ACCESS_TOKEN}=   Get Token
    ${HEADERS}=   Request Headers   ${APPLICATION_JSON}
    ...                             ${ACCESS_TOKEN}
    ${RESPONSE}=   Delete Call
    ...   PATH=${DELETE_SUITE_PATH}${SUITE_ID}
    ...   HEADERS=${HEADERS}
    ${MESSAGE}=   Get Json Key Value   ${RESPONSE}   ${MESSAGE}
    Should Be Equal As Strings   ${MESSAGE}   Test suite successfully deleted

Delete Test Case
    [Documentation]   Delete test case by calling DELETE api/v1/test_cases/<test_case_id> endpoint.
    [Arguments]
    ...   ${CASE_ID}=
    ${ACCESS_TOKEN}=   Get Token
    ${HEADERS}=   Request Headers   ${APPLICATION_JSON}
    ...                             ${ACCESS_TOKEN}
    ${RESPONSE}=   Delete Call
    ...   PATH=${DELETE_CASE_PATH}${CASE_ID}
    ...   HEADERS=${HEADERS}
    ${MESSAGE}=   Get Json Key Value   ${RESPONSE}   ${MESSAGE}
    Should Be Equal As Strings   ${MESSAGE}   Test case successfully deleted

Get Token
    [Documentation]   Get access_token returned by POST api/v1/login endpoint.
    ${RESPONSE}=   Post Call
    ...   PATH=${LOGIN_PATH}
    ...   BODY=${VALID_CREDS}
    ...   HEADERS=${APPLICATION_JSON}
    ${ACCESS_TOKEN}=   Get Json Key Value   ${RESPONSE}   ${TOKEN}
    Should Match Regexp   ${ACCESS_TOKEN}   ${ACCESS_TOKEN_REGEXP}
    [Return]   ${ACCESS_TOKEN}

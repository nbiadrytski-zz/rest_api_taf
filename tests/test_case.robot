*** Settings ***
Documentation    Test case tests

Library          ../libraries/helper_funcs.py
Variables        ../data/variables.py
Resource         ../keywords/http_keywords.robot
Resource         ../keywords/test_keywords.robot

Suite Setup      Create Test Suite
Suite Teardown   Delete Test Suite   ${SUITE_ID}
Test Setup       Get Access Token


*** Test Cases ***
Create test case
    [Documentation]   Check response body message is correct
    #[Setup]   Get Access Token
    ${HEADERS}=   Request Headers   ${APPLICATION_JSON}
    ...                             ${ACCESS_TOKEN}
    ${REQUEST_BODY}=   Case Body
    ...   ${SUITE_ID}
    ...   ${CASE_TITLE}
    ...   ${CASE_DESCRIPTION}
    ${RESPONSE}=   Post Call
    ...   PATH=${CREATE_CASE_PATH}
    ...   BODY=${REQUEST_BODY}
    ...   HEADERS=${HEADERS}
    ${MESSAGE}=   Get Json Key Value   ${RESPONSE}   ${MESSAGE}
    ${CASE_ID}=   Get Json Key Value   ${RESPONSE}   ${ID}
    Should Be Equal As Strings   ${MESSAGE}   Test case successfully added
    [Teardown]   Delete Test Case   ${CASE_ID}


Create test case for non-existing test suite
    [Documentation]   Check response body message is correct
    ${HEADERS}=   Request Headers   ${APPLICATION_JSON}
    ...                             ${ACCESS_TOKEN}
    ${REQUEST_BODY}=   Case Body
    ...   ${NON_EXISTING_SUITE_ID}
    ...   ${CASE_TITLE}
    ...   ${CASE_DESCRIPTION}
    ${RESPONSE}=   Post Call
    ...   PATH=${CREATE_CASE_PATH}
    ...   BODY=${REQUEST_BODY}
    ...   HEADERS=${HEADERS}
    ...   CODE_CHECK=False
    ${MESSAGE}=   Get Json Key Value   ${RESPONSE}   ${MESSAGE}
    Should Be Equal As Strings   ${MESSAGE}   Test suite does not exist


Create test case for non_existing test suite
    [Documentation]   Check status code is 404
    ${HEADERS}=   Request Headers   ${APPLICATION_JSON}
    ...                             ${ACCESS_TOKEN}
    ${REQUEST_BODY}=   Case Body
    ...   ${NON_EXISTING_SUITE_ID}
    ...   ${CASE_TITLE}
    ...   ${CASE_DESCRIPTION}
    ${RESPONSE}=   Post Call
    ...   PATH=${CREATE_CASE_PATH}
    ...   BODY=${REQUEST_BODY}
    ...   HEADERS=${HEADERS}
    ...   CODE_CHECK=False
    Should Be Equal As Integers   ${RESPONSE.status_code}   404


Create test case without suite_id in request body
    [Documentation]   Check status code is 404
    ${HEADERS}=   Request Headers   ${APPLICATION_JSON}
    ...                             ${ACCESS_TOKEN}
    ${RESPONSE}=   Post Call
    ...   PATH=${CREATE_CASE_PATH}
    ...   BODY=${CASE_NO_SUITE_ID}
    ...   HEADERS=${HEADERS}
    ...   CODE_CHECK=False
    Should Be Equal As Integers   ${RESPONSE.status_code}   400


Create test case without suite id in request body
    [Documentation]   Check response body message is correct
    ${HEADERS}=   Request Headers   ${APPLICATION_JSON}
    ...                             ${ACCESS_TOKEN}
    ${RESPONSE}=   Post Call
    ...   PATH=${CREATE_CASE_PATH}
    ...   BODY=${CASE_NO_SUITE_ID}
    ...   HEADERS=${HEADERS}
    ...   CODE_CHECK=False
    ${MESSAGE}=   Get Json Key Value   ${RESPONSE}   ${MESSAGE}
    Should Be Equal As Strings   ${MESSAGE}   Bad request body

*** Settings ***
Documentation    Test suite tests

Library          ../libraries/helper_funcs.py
Variables        ../data/variables.py
Resource         ../keywords/http_keywords.robot
Resource         ../keywords/test_keywords.robot

Test Setup       Get Access Token


*** Test Cases ***
Test suite creation
    [Documentation]   Check response body message is correct
    ${HEADERS}=   Request Headers   ${APPLICATION_JSON}
    ...                             ${ACCESS_TOKEN}
    ${RESPONSE}=   Post Call
    ...   PATH=${CREATE_SUITE_PATH}
    ...   BODY=${TEST_SUITE}
    ...   HEADERS=${HEADERS}
    ${MESSAGE}=   Get Json Key Value   ${RESPONSE}   ${MESSAGE}
    ${SUITE_ID}=   Get Json Key Value   ${RESPONSE}   ${ID}
    Should Be Equal As Strings   ${MESSAGE}   Test suite successfully added
    [Teardown]   Delete Test Suite   ${SUITE_ID}


Create suite with invalid Content-Type
    [Documentation]   Check response body message is correct
    ${HEADERS}=   Request Headers   ${APPLICATION_XML}
    ...                             ${ACCESS_TOKEN}
    ${RESPONSE}=   Post Call
    ...   PATH=${CREATE_SUITE_PATH}
    ...   BODY=${TEST_SUITE}
    ...   HEADERS=${HEADERS}
    ...   CODE_CHECK=False
    ${MESSAGE}=   Get Json Key Value   ${RESPONSE}   ${MESSAGE}
    Should Be Equal As Strings    ${MESSAGE}   Content-type must be application/json


Create suite using invalid Content-Type
    [Documentation]   Check status code is 415
    ${HEADERS}=   Request Headers   ${APPLICATION_XML}
    ...                             ${ACCESS_TOKEN}
    ${RESPONSE}=   Post Call
    ...   PATH=${CREATE_SUITE_PATH}
    ...   BODY=${TEST_SUITE}
    ...   HEADERS=${HEADERS}
    ...   CODE_CHECK=False
    Should Be Equal As Integers   ${RESPONSE.status_code}   415

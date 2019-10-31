*** Settings ***
Documentation    Login tests

Library          ../libraries/helper_funcs.py
Variables        ../data/variables.py
Resource         ../keywords/http_keywords.robot


*** Test Cases ***
Login with valid creds
    [Documentation]   Check access_token matches regexp
    ${RESPONSE}=   Post Call
    ...   PATH=${LOGIN_PATH}
    ...   BODY=${VALID_CREDS}
    ...   HEADERS=${APPLICATION_JSON}
    ${ACESS_TOKEN}=   Get Json Key Value   ${RESPONSE}   ${TOKEN}
    Should Match Regexp   ${ACESS_TOKEN}   ${ACCESS_TOKEN_REGEXP}

Login with invalid password
    [Documentation]   Check response body message is correct
    ${RESPONSE}=   Post Call
    ...   PATH=${LOGIN_PATH}
    ...   BODY=${INVALID_CREDS}
    ...   HEADERS=${APPLICATION_JSON}
    ...   CODE_CHECK=False
    ${MESSAGE}=   Get Json Key Value   ${RESPONSE}   ${MESSAGE}
    Should Be Equal As Strings   ${MESSAGE}   No such username or password

Login using invalid password
    [Documentation]   Check status code is 401
    ${RESPONSE}=   Post Call
    ...   PATH=${LOGIN_PATH}
    ...   BODY=${INVALID_CREDS}
    ...   HEADERS=${APPLICATION_JSON}
    ...   CODE_CHECK=False
    Should Be Equal As Strings   ${RESPONSE.status_code}   401

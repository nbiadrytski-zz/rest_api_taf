*** Settings ***
Documentation    Server index tests

Library   ../libraries/helper_funcs.py
Resource   ../keywords/http_keywords.robot


*** Test Cases ***
Server index call
    [Documentation]   Check response body message is correct
    ${RESPONSE}=    Get Call
    ${MESSAGE}=  Get Json Key Value   ${RESPONSE}   ${MESSAGE}
    Should Be Equal As Strings    ${MESSAGE}   Simple Test Management System API

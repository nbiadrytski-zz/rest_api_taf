*** Settings ***
Documentation    HTTP GET, POST, DELETE methods keywords using RequestsLibrary

Library          RequestsLibrary
Library          ../libraries/helper_funcs.py
Variables        ../data/variables.py


*** Keywords ***
Get Call
    [Documentation]   Return HTTP GET response object. Optional status code check
    [Arguments]
    ...   ${URL}=${BASE_URL}
    ...   ${PATH}=
    ...   ${CODE_CHECK}=True
    Create Session   localhost   ${BASE_URL}
    ${RESPONSE}=   Get Request   localhost   ${PATH}
    Run Keyword If   ${CODE_CHECK}
    ...   Should Be Equal As Integers   ${RESPONSE.status_code}   200
    [Return]   ${RESPONSE}


Post Call
    [Documentation]   Return HTTP POST response object. Optional status code check
    [Arguments]
    ...   ${URL}=${BASE_URL}
    ...   ${PATH}=
    ...   ${BODY}=
    ...   ${HEADERS}=
    ...   ${CODE_CHECK}=True
    Create Session   localhost   ${BASE_URL}
    ${RESPONSE}=   Post Request
    ...   localhost
    ...   ${PATH}
    ...   data=${BODY}
    ...   headers=${HEADERS}
    Run Keyword If   ${CODE_CHECK}
    ...   Should Be Equal As Integers   ${RESPONSE.status_code}   200
    [Return]   ${RESPONSE}

Delete Call
    [Documentation]   Return HTTP DELETE response object. Optional status code check
    [Arguments]
    ...   ${URL}=${BASE_URL}
    ...   ${PATH}=
    ...   ${HEADERS}=
    ...   ${CODE_CHECK}=True
    Create Session   localhost   ${BASE_URL}
    ${RESPONSE}=   Delete Request
    ...   localhost
    ...   ${PATH}
    ...   headers=${HEADERS}
    Run Keyword If   ${CODE_CHECK}
    ...   Should Be Equal As Integers   ${RESPONSE.status_code}   200
    [Return]   ${RESPONSE}

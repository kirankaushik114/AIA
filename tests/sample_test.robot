*** Settings ***
Resource    resources/keywords.resource
Library     RequestsLibrary
Library     Collections
Suite Setup    Log    Starting suite
Suite Teardown    Log    Suite finished

*** Variables ***
${BASE_URL}    https://httpbin.org

*** Test Cases ***
Get status 200
    [Documentation]    Simple GET to verify HTTP status 200
    Create Session    httpbin    ${BASE_URL}
    ${resp}=    GET On Session    httpbin    /status/200    verify=${True}
    Should Be Equal As Integers    ${resp.status_code}    200

Echo JSON
    [Documentation]    POST JSON and verify response contains the same value
    Create Session    httpbin    ${BASE_URL}
    ${payload}=    Create Dictionary    name=robot    value=framework
    ${resp}=    POST On Session    httpbin    /post    json=${payload}    verify=${True}
    Should Be Equal As Strings    ${resp.json()['json']['name']}    robot


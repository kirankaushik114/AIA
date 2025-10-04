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
    ${resp}=    GET    httpbin    /status/200
    Should Be Equal As Integers    ${resp.status_code}    200

Echo JSON
    [Documentation]    POST JSON and verify response contains the same value
    Create Session    httpbin    ${BASE_URL}
    ${payload}=    Create Dictionary    name=robot    value=framework
    ${resp}=    POST    httpbin    /post    json=${payload}
    Should Be Equal As Strings    ${resp.json()['json']['name']}    robot

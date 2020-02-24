*** Settings ***
Library    ImapLibrary2

*** Test Cases ***
Email Verification
    Open Mailbox    host=imap.gmail.com    user=softnextqcshock@gmail.com    password=Arborabc1234
    ${LATEST} =    Wait For Email    sender=notify@push.proex.io    timeout=300
    ${HTML} =    Open Link From Email    ${LATEST}
    Should Contain    ${HTML}    Welcome to use ProEx
    Close Mailbox

Multipart Email Verification
    Open Mailbox    host=imap.gmail.com    user=softnextqcshock@gmail.com    password=Arborabc1234
    ${LATEST} =    Wait For Email    sender=notify@push.proex.io    timeout=300
    ${parts} =    Walk Multipart Email    ${LATEST}
    :FOR    ${i}    IN RANGE    ${parts}
    \\    Walk Multipart Email    ${LATEST}
    \\    ${content-type} =    Get Multipart Content Type
    \\    Continue For Loop If    '${content-type}' != 'text/html'
    \\    ${payload} =    Get Multipart Payload    decode=True
    \\    Should Contain    ${payload}    Welcome to use ProEx
    \\    ${HTML} =    Open Link From Email    ${LATEST}
    \\    Should Contain    ${HTML}    Welcome to use ProEx
    Close Mailbox



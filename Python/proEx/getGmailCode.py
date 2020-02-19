import imaplib
import smtplib
import email

imap_ssl_host = 'imap.gmail.com'
imap_ssl_port = 993
username = 'softnextqcshock@gmail.com'
password = 'Arborabc1234'
server = imaplib.IMAP4_SSL(imap_ssl_host, imap_ssl_port)

server.login(username, password)
server.select('INBOX')

data = server.uid('search',None, '(SUBJECT "MY QUERY HERE!")')
print(data)

status, count =server.select('Inbox')
status, data = server.fetch(count[0], '(UID BODY[TEXT])')
content = data[0][1]
#print(content)
server.close()
server.logout()



# for response_part in data :
#     if isinstance(response_part,tuple):
#         print(response_part)
#         msg = email.message_from_string(response_part[1])
#         print("subj:", msg['subject'])
#         print("from:", msg['from'])
#         print("body:")
#         for part in msg.walk():
#             if part.get_content_type() == 'text/plain':
#                 print(part.get_payload())

# for num in data[0].split():
#     status, data = server.fetch(num, '(RFC822)')
#     email_msg = data[0][1]
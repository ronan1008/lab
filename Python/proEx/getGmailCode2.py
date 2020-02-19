import email, getpass, imaplib, os
from io import StringIO

# connecting to the gmail imap server
m = imaplib.IMAP4_SSL("imap.gmail.com")
m.login("softnextqcshock@gmail.com","Arborabc1234")
m.select("Inbox")

resp, items = m.search(None, "FROM ronan1008@yahoo.com.tw") # the newsletter which i am 
# trying to get the email body of
items = items[0].split() # getting the mails id

for emailid in items:
    resp, data = m.fetch(emailid, "(RFC822)") # fetching the mail, "`(RFC822)`" means "get the whole stuff", but you can ask for headers only, etc
    email_body = data[0][1] # getting the mail content
    print(email_body)
    mail = email.message_from_bytes(email_body) # parsing the mail content to get a mail object
    print(mail)
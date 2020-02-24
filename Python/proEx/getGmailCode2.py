import email, imaplib, os, mailparser
from html.parser import HTMLParser
from datetime import datetime, timedelta

imapServer = 'imap.gmail.com'
mailAccount = 'softnextqcshock@gmail.com'
mailPass = 'Arborabc1234'

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

# connecting to the gmail imap server
m = imaplib.IMAP4_SSL(imapServer)
m.login(mailAccount,mailPass)
m.select("Inbox")

resp, items = m.search(None, "FROM ProEX") # the newsletter which i am 
# trying to get the email body of
items = items[0].split() # getting the mails id

for emailid in items:
    resp, data = m.fetch(emailid, "(RFC822)") # fetching the mail, "`(RFC822)`" means "get the whole stuff", but you can ask for headers only, etc
    email_body = data[0][1] # getting the mail content
#    mail = email.message_from_bytes(email_body) # parsing the mail content to get a mail object
    mail = mailparser.parse_from_bytes(email_body)
    maildate = datetime.strptime(str(mail.date),'%Y-%m-%d %H:%M:%S')
    nowdate = datetime.now()
    nowdate_a = datetime.now() -  timedelta(seconds=30)
    if maildate > nowdate_a :
        maildate = mail.date
        mailbody = mail.body
        mailfrom = mail.from_
        mailsubject = mail.subject
        print(mailsubject)
        print(maildate)
        print(mailfrom)
        print(strip_tags(mailbody))
    #    m.store(emailid, '+FLAGS', '\\Deleted')
    else:   
        pass

#m.expunge()
m.close()
m.logout()
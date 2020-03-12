# IBM's method
# REF: https://developer.ibm.com/tutorials/pattern-analysis-of-emails-using-python/

# Requires IMAP to be enabled in gmail
# requires less sequre apps...

import imaplib
import email
import getpass
import pandas as pd
import keyring


# login
username = 'officialkwade@gmail.com'
password = keyring.get_password('gmail', 'officialkwade@gmail.com')

mail = imaplib.IMAP4_SSL('imap.gmail.com') #EMAIL SERVER
mail.login(username, password)

# grab some emails
mail.select("inbox")
result, numbers = mail.uid('search', None, "ALL")
uids = numbers[0].split()
result, messages = mail.uid('fetch', b','.join(uids), '(BODY[])')
date_list = []
from_list = []
message_text = []
count = 0
for _, message in messages[::2]:
  count += 1
  if count % 100 == 0:
    print(count)
  msg = email.message_from_string(message)
  if msg.is_multipart():
    t = []
    for p in msg.get_payload():
      t.append(p.get_payload(decode=True))
    message_text.append(t[0])
  else:
     message_text.append(msg.get_payload(decode=True))
     
  date_list.append(msg.get('date'))
  from_list.append(msg.get('from'))
  date_list = pd.to_datetime(date_list)
  print( len(message_text))
  print( len(from_list))
  df = pd.DataFrame(data={'Date':date_list,'Sender':from_list,'Message':message_text})
  print( df.head())
  df.to_csv('~inbox_email.csv',index=False)
  

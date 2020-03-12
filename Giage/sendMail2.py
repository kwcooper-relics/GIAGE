# send mail 2: methods to send mail via gmail API

"""Send an email message from the user's account.
    https://developers.google.com/gmail/api/guides/sending
"""

import base64
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email import encoders 
import mimetypes
import os
from apiclient import errors


# TODO:
# Think about how I want the print settings (here or the class?)

def SendMessage(service, user_id, message):
  """Send an email message.

  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    message: Message to be sent.

  Returns:
    Sent Message.
  """
  Verbose = True
  
  try:
    message = (service.users().messages().send(userId=user_id, body=message)
               .execute())
    if Verbose:
      print('Sent! (Message Id: %s)' % message['id'])

    return message

  except errors.HttpError or error:
    print('An error occurred: %s' % error)



def CreateMessage(sender, to, subject, message_text):
  """Create a message for an email.

  Args:
    sender: Email address of the sender.
    to: Email address of the receiver.
    subject: The subject of the email message.
    message_text: The text of the email message.

  Returns:
    An object containing a base64url encoded email object.
  """
  message = MIMEText(message_text)
  message['to'] = to
  message['from'] = sender
  message['subject'] = subject
  #return {'raw': base64.urlsafe_b64encode(message.as_string())}
  return {'raw': base64.urlsafe_b64encode(message.as_string().encode()).decode()}
  # https://stackoverflow.com/questions/43352496/gmail-api-error-from-code-sample-a-bytes-like-object-is-required-not-str




def CreateMessageWithAttachment(sender, to, subject, message_text, file_dir,
                                filename):
  """Create a message for an email.

  Args:
    sender: Email address of the sender.
    to: Email address of the receiver.
    subject: The subject of the email message.
    message_text: The text of the email message.
    file_dir: The directory containing the file to be attached.
    filename: The name of the file to be attached.

  Returns:
    An object containing a base64url encoded email object.
  """
  message = MIMEMultipart()
  message['to'] = to
  message['from'] = sender
  message['subject'] = subject

  msg = MIMEText(message_text)
  message.attach(msg)

  path = os.path.join(file_dir, filename)
  content_type, encoding = mimetypes.guess_type(path)

  if content_type is None or encoding is not None:
    content_type = 'application/octet-stream'
  main_type, sub_type = content_type.split('/', 1)
  if main_type == 'text':
    fp = open(path, 'rb')
    msg = MIMEText(fp.read(), _subtype=sub_type)
    fp.close()
  elif main_type == 'image':
    fp = open(path, 'rb')
    msg = MIMEImage(fp.read(), _subtype=sub_type)
    fp.close()
  elif main_type == 'audio':
    fp = open(path, 'rb')
    msg = MIMEAudio(fp.read(), _subtype=sub_type)
    fp.close()
  else:
    fp = open(path, 'rb')
    msg = MIMEBase(main_type, sub_type)
    msg.set_payload(fp.read())
    #msg = encoders.encode_base64(msg)
    fp.close()

  msg.add_header('Content-Disposition', 'attachment', filename=filename)
  message.attach(msg)

  #return {'raw': base64.urlsafe_b64encode(message.as_string())}
  return {'raw': base64.urlsafe_b64encode(message.as_bytes().encode()).decode()}




def CreateMessageWithAttachToo(sender, to, subject, message_text, file_dir, filename):
  """Create and endode a message for an email with an attachment.

  Args:
    sender: Email address of the sender.
    to: Email address of the receiver.
    subject: The subject of the email message.
    message_text: The text of the email message.
    file_dir: The directory containing the file to be attached.
    filename: The name of the file to be attached.

  Returns:
    An object containing a base64url encoded email object.

  Edits:
    fixed the google's version for python 3+
  """
  message = MIMEMultipart()
  message['to'] = to
  message['from'] = sender
  message['subject'] = subject

  msg = MIMEText(message_text)
  message.attach(msg)
  
  # open the file to be sent
  path = os.path.join(file_dir, filename)
  attachment = open(path, "rb") 
    
  p = MIMEBase('application', 'octet-stream') 
  p.set_payload((attachment).read()) 
  encoders.encode_base64(p) 
     
  p.add_header('Content-Disposition', "attachment; filename= %s" % filename) 
  message.attach(p)

  return {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}


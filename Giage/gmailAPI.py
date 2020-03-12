from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

from sendMail2 import SendMessage, CreateMessage, CreateMessageWithAttachment, CreateMessageWithAttachToo
from getMsgs import ListMessagesMatchingQuery,GetMessage

from apiclient import errors
import base64
import email



class Giage:
    
    def __init__(self):
        self.service = self.build_auth() # init the service and auth

        # Define scopes
        # If modifying these scopes, delete the file token.json.
        # https://stackoverflow.com/questions/32143126/how-do-i-get-around-httperror-403-insufficient-permission-gmail-api-python
        self.SCOPES = 'https://mail.google.com/'
        #self.SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'
        

    def get_docs(self):
        print('https://developers.google.com/gmail/api/quickstart/python')

    def build_auth(self):

        # build auth and necessary files
        # TODO: have to do this, maybe init when giage is called?
        
        # if there is an error either the scope has changed,
        # the auth has epiried, or something else is going on.

        # get credentials from the DOCS file above
        try:
            store = file.Storage('token.json')
            creds = store.get()
            if not creds or creds.invalid:
                flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
                creds = tools.run_flow(flow, store)
                
        except oauth2client.client.HttpAccessTokenRefreshError:
            print('Need to refresh token...')
            print('Try re-running or configuring the credentials file.')
            print('See https://developers.google.com/gmail/api/quickstart/python for more info.')

        return build('gmail', 'v1', http=creds.authorize(Http()))

    def send_mail(self, msg):
        # Helper function for unpacking and sending emails with the API
        # converts to a base64url encoded email object
        msgPacked = CreateMessage(msg['from'], msg['to'], msg['subject'], msg['body'])
        SendMessage(self.service, 'me', msgPacked)

    def send_mail_attach(self, msg):
        # Helper function for unpacking and sending emails with the API
        # converts to a base64url encoded email object
        msgPacked = CreateMessageWithAttachToo(msg['from'], msg['to'], msg['subject'], msg['body'], msg['fDir'], msg['fName'])
        SendMessage(self.service, 'me', msgPacked)


def grabMessagesIds(service):
    # collect messages
    #msgs = service.users().messages().list(userId='me').execute()
    
    user_id = 'me'
    query = 'Haro'
    msgs = ListMessagesMatchingQuery(service, user_id, query)

    
    
    print(len(msgs))
    return msgs


def getIDs(msgs):
    ids = []
    for ms in msgs:
        ids.append(ms['id'])
    return ids

'''
    Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    msg_id: The ID of the Message required.

  Returns:
    A Message.

    '''
def grabMessages(service):
    GetMessage(service, 'me', msg_id)


def GetMessageBody(service, user_id, msg_id):
    # from https://stackoverflow.com/questions/31967587/python-extract-the-body-from-a-mail-in-plain-text
    try:
            message = service.users().messages().get(userId=user_id, id=msg_id, format='raw').execute()
            msg_str = base64.urlsafe_b64decode(message['raw'].encode('ASCII'))
            mime_msg = email.message_from_string(msg_str)
            messageMainType = mime_msg.get_content_maintype()
            if messageMainType == 'multipart':
                    for part in mime_msg.get_payload():
                            if part.get_content_maintype() == 'text':
                                    return part.get_payload()
                    return ""
            elif messageMainType == 'text':
                    return mime_msg.get_payload()
    except errors.HttpError as error:
            print( 'An error occurred: %s' % error)
    

if __name__ == '__main__':

    G = Giage()
    
    #service = buildAuth()
    service = G.service

    # send a regular message
    msg = dict()
    msg['from'] = 'bla' #'officialkwade@gmail.com'
    msg['to'] = 'officialkwade@gmail.com'
    msg['subject'] = 'tst'
    msg['body'] = 'Hello, how are you today?'
    #G.send_mail(msg)


    # send a message with attachment
    msg = dict()
    msg['from'] = 'bla' #'officialkwade@gmail.com'
    msg['to'] = 'officialkwade@gmail.com'
    msg['subject'] = 'tst'
    msg['body'] = 'Hello, how are you today?'
    msg['fDir'] = '/Users/K/Pictures/'
    msg['fName'] = 'baby.jpg'
    #G.send_mail_attach(msg)
    
    msgs = grabMessagesIds(service)
    ids = getIDs(msgs)
    print(len(ids))

    msg = GetMessage(service, 'me', msgs[0]['id'])

    bdy = GetMessageBody(service, 'me', msgs[0]['id'])
    print(type(bdy))
    print(len(bdy))
    print('fin')




    # Example call of the Gmail API: print labels
##    results = service.users().labels().list(userId='me').execute()
##    labels = results.get('labels', [])
##
##    if not labels:
##        print('No labels found.')
##    else:
##        print('Labels:')
##        for label in labels:
##            print(label['name'])
##
##    print(service.users())

    

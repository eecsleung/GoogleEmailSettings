#!/usr/bin/python
import gdata.apps.emailsettings.client
import gdata.gauth
import getpass, getopt, HTMLParser, sys
from oauth2client.client import SignedJwtAssertionCredentials

def main(argv):

     try:
          opts, args = getopt.getopt(argv,"hadgb",["add","delete","get","bulk"])
     except getopt.GetoptError:
          print 'python forwarding.py [-a,--add; -d,--delete; -g,--get; -b,--bulk]'
          sys.exit(2)

     for opt, args in opts:
          if opt in ("-b", "--bulk"):
               file = raw_input("Please provide the input filename: ")
          else:
               user = raw_input("Enter the username (first.last): ")

     for opt, args in opts:
          if opt == '-h':
               print 'python forwarding.py [-a,--add; -d,--delete; -g,--getl -b,--bulk]'
               sys.exit()
          elif opt in ("-a", "--add"):
               print "\n--- Add Forwarder ---"
               setForwarding(user)
          elif opt in ("-d", "--delete"):
               print "\n--- Delete Forwarder ---"
               removeForwarding(user)
          elif opt in ("-g", "--get"):
               print "\n--- Retrieving Forwarder ---"
               getForwarding(user)
          elif opt in ("-b", "--bulk"):
               getBulkForwarding(file)

def google_get_emailsettings_credentials():
    SERVICE_ACCOUNT_EMAIL = "CLIENT-ID-FROM-DEV-CONSOLE@developer.gserviceaccount.com"
    SERVICE_ACCOUNT_PKCS12_FILE_PATH = "path/to/keyfile.pk12"
    GOOGLE_ADMIN_USER = "username@company.com"

    with open(SERVICE_ACCOUNT_PKCS12_FILE_PATH) as f:
        private_key = f.read()

    client = gdata.apps.emailsettings.client.EmailSettingsClient(domain='company.com')

    credentials = SignedJwtAssertionCredentials(
        SERVICE_ACCOUNT_EMAIL,
        private_key,
        scope='https://apps-apis.google.com/a/feeds/emailsettings/2.0/',
        sub=GOOGLE_ADMIN_USER)

    auth2token = gdata.gauth.OAuth2TokenFromCredentials(credentials)
    auth2token.authorize(client)

    return client

def setForwarding(user):
    forward = raw_input("Enter the forwarding address (email@domain.com): ")
    # KEEP - Emails are left in the inbox.
    # ARCHIVE - Emails are archived, and, by default, are not visible in the inbox.
    # DELETE - When deleted, emails are moved to the Spam folder.
    # MARK_READ - Emails are marked as read in the inbox.

    client = google_get_emailsettings_credentials()
    client.UpdateForwarding(username=user, enable=True, forward_to=forward, action='KEEP')

def removeForwarding(user):
    client = google_get_emailsettings_credentials()
    client.UpdateForwarding(username=user, enable=False)

def getForwarding(user):
    client = google_get_emailsettings_credentials()
    result = client.RetrieveForwarding(username=user)
    print "\n--- FORWARDING INFORMATION ---"
    print "User: " + user
    print "Enabled: " + result.enable
    print "Forward To: " + result.forward_to
    print "Action: " + result.action
    print "\n"
    return

def getBulkForwarding(file):
    fh = open(file,'r')
    for line in fh.xreadlines():
        getForwarding(line.rstrip(),admin,pw)
    fh.close()

if __name__ == "__main__":
    main(sys.argv[1:])

#! /usr/bin/python
print "Content-Type:text/html\n"

import cgi,cgitb,os
cgitb.enable()

def loggedin(): # This has been commented on so much, just returns whether the person is logged in or not based on their ip address
    ip = os.environ['REMOTE_ADDR']
    inStream = open('../loggedin.txt','r')
    data = inStream.read().split('\n')
    inStream.close()
    accounts = {}
    for account in data:
        account = account.split(',')
        try:
            accounts[account[1]] = account[0]
        except:
            pass
    if accounts.has_key(ip): # Person is logged in from saved ip:
        return True
    else: # Person is not logged in or accessing from different ip
        return False

def main():
    if loggedin() == True: # If the person is already logged in, then they are redirected
        inStream = open('redirect.html','r')
        html = inStream.read()
        inStream.close()
    else: # If not, then the person is given the form to log in or register
        inStream = open('template.html','r')
        html = inStream.read()
        inStream.close()

    print html

main()

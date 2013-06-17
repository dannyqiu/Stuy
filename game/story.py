#! /usr/bin/python
print "Content-Type:text/html\n"

import cgi,cgitb,os
cgitb.enable()

def loggedin():
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
        retStr = '<li><a href="../home/"><i class="icon-user" style="vertical-align:-10%;"></i> ' + accounts[ip].capitalize() + '</a></li><li><a href="../logout.py">Logout</a></li>'
        return retStr
    else: # Person is not logged in or accessing from different ip
        return '<li><a href="../accounts/">Login / Register</a></li>'

def main():
    inStream = open('Entrance.html','r')
    html = inStream.read()
    inStream.close()
    html = html.replace('<li><a href="../accounts/">Login / Register</a></li>',loggedin())

    print html

main()

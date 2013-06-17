#!/usr/bin/python
print "Content-Type: text/html\n"

import cgi, os, cgitb
cgitb.enable()

def loggedin(profile): # Same code as always, checks to see if someone should be logged in or not by checking their ip address and comparing it to a file that stores the ip address associated with the user. There is some twist to this code where you have to input a 0 or a 1 - 0 would give you the html code for the navigation bar, 1 would give you the user that is logged in based on the ip address
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
        if profile == 1:
            return accounts[ip]
        else:
            retStr = '<li><a href="../home/"><i class="icon-user" style="vertical-align:-10%;"></i> ' + accounts[ip].capitalize() + '</a></li><li><a href="../logout.py">Logout</a></li>'
            return retStr
    else: # Person is not logged in or accessing from different ip
        if profile == 1:
            return 'noexist'
        else:
            return '<li><a href="../accounts/">Login / Register</a></li>'

username = loggedin(1) # This code just goes in and resets the progress of the user to 0%
if username != 'noexist':
    o = open("../profiles.txt", "r")
    data = o.read().split('\n-----\n')
    o.close()
    w = open("../profiles.txt","w")
    writeStr = ""
    for line in data:
        info = line.split('$!&spt&!$')
        if info[0] == username:
            info[3] = "0"
            line = '$!&spt&!$'.join(info)
        writeStr += line + '\n-----\n'
    w.write(writeStr)
    w.close()

inStream = open('story.html','r')
html = inStream.read()
inStream.close()
html = html.replace('<li><a href="../accounts/">Login / Register</a></li>',loggedin(0))
html = html.replace('STORY','''<br><h3>Your game has been reset!</h3><button class="btn btn-success btn-large pull-left" onclick="location.href='story.py'">&laquo; Go Back</button>''')

print html

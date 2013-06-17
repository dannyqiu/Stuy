#!/usr/bin/python
print "Content-Type: text/html\n"

import cgi,os,cgitb
cgitb.enable

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

inStream = open('redirect.html','r')
html = inStream.read()
inStream.close()
html = html.replace('<li><a href="../accounts/">Login / Register</a></li>',loggedin(0))

username = loggedin(1)
progress = "0"
if username != 'noexist': # For those people that are logged in, the save file is read
    o = open("../profiles.txt", "r")
    data = o.read().split('\n-----\n')
    o.close()
    for line in data:
        info = line.split('$!&spt&!$')
        if info[0] == username: # When it reaches the username that is equal to that of the user logged in, it will set the progress
            progress = info[3] # This makes the progress of the user equal to that in the profiles.txt file which is the saved progress of the user

if progress == "0" or progress == "19": # Since the progress is put in as percentages, this section of the code converts those percentages to their corresponding file
    progressFile = '1.py'
elif progress == "28":
    progressFile = '3.py'
elif progress == "42":
    progressFile = '2.py'
elif progress == "55":
    progressFile = '14.py'
elif progress == "57":
    progressFile = '4.py'
elif progress == "69":
    progressFile = '12.py'
elif progress == "73":
    progressFile = '8.py'
elif progress == "75":
    progressFile = '10.py'
elif progress == "78":
    progressFile = '16.py'
elif progress == "80":
    progressFile = '9.py'
elif progress == "83":
    progressFile = '5.py'
elif progress == "84":
    progressFile = '13b.py'
elif progress == "85":
    progressFile = '13.py'
elif progress == "89":
    progressFile = '7.py'
elif progress == "91":
    progressFile = '6.py'
elif progress == "99":
    progressFile = '15.py'
elif progress == "100":
    progressFile = 'death.py'
else:
    progressFile = '1.py'

html = html.replace('STORY_PROGRESS', progressFile) # Since it is a redirect file, the user will be automatically redirected to whatever their save progress was

print html

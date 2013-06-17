#!/usr/bin/python
print "Content-Type: text/html\n"

import cgi, os, cgitb
cgitb.enable()

text = "Hello, I see you are ready <br> to embark on your journey."
text2 = "<br>Where do you want to go?"

formatted = '<p style="text-align: center;">'+ '<font size = "20">' + text + text2

button1 ='<form name="input" action="1-2.html" method="get"><input type="submit" value="Into the cave"></form>'
button2 ='<form name="input" action="1-3.html" method="get"><input type="submit" value="To the forest"></form>'

formedb = '<div style="text-align:center">' + button1 + "&nbsp;&nbsp;&nbsp;&nbsp;" + button2 + "</div>"

html = formatted + formedb

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

username = loggedin(1) # This is the saving mechanism, where it goes through the profiles file, finds the user that is playing the game right now, and puts the % progress of the game into their part of the profile
if username != 'noexist': # This is so that those people not logged in don't experience errors
    o = open("../profiles.txt", "r")
    data = o.read().split('\n-----\n') # Splits data into the individual profiles
    data.pop()
    o.close()
    w = open("../profiles.txt","w")
    writeStr = ""
    for line in data:
        info = line.split('$!&spt&!$') # Splits the profiles into each component data
        if info[0] == username: # If the username is the same as the one logged in, then it will log the progress of the user
            info[3] = "19"
            line = '$!&spt&!$'.join(info)
        writeStr += line + '\n-----\n' # Rewrites the entire file with the progress updated
    w.write(writeStr)
    w.close()

inStream = open('story.html','r')
story = inStream.read()
inStream.close()
story = story.replace('<li><a href="../accounts/">Login / Register</a></li>',loggedin(0))
story = story.replace('STORY',html)

print story

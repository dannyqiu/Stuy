#!/usr/bin/python
print "Content-Type: text/html\n"

import cgi, os, cgitb
cgitb.enable ()

text = "Drip"
dripped = "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;" + text
drips = dripped + "<br>" + "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;" + dripped + "<br>" + "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;" + "&nbsp;&nbsp;" + dripped

text2 = "You hear water falling<br>from the ceiling."

formatted = '<font size = "25">' + drips + '</font>' + '<p style="text-align: center;">' + '<br>' + '<br>' + '<font size = "20">' + text2

button1 = '<form name="input" action="4.py" method="get"><input type="submit" value="Walk towards the water"></form>'
button2 = '<form name="input" action="5.py" method="get"><input type="submit" value="Away from the sound"></forms>'

formbuttons = '<div style="text-align:center">' + '<img src="Cave-Enter.gif" alt="cave"><br><br>' + button1 + '<br>' + button2 + '</div>'

html = formatted + formbuttons

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

username = loggedin(1)
if username != 'noexist':
    o = open("../profiles.txt", "r")
    data = o.read().split('\n-----\n')
    data.pop()
    o.close()
    w = open("../profiles.txt","w")
    writeStr = ""
    for line in data:
        info = line.split('$!&spt&!$')
        if info[0] == username:
            info[3] = "42"
            line = '$!&spt&!$'.join(info)
        writeStr += line + '\n-----\n'
    w.write(writeStr)
    w.close()

inStream = open('story.html','r')
story = inStream.read()
inStream.close()
story = story.replace('<li><a href="../accounts/">Login / Register</a></li>',loggedin(0))
story = story.replace('STORY',html)

print story

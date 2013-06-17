#!/usr/bin/python
print "Content-Type: text/html\n"

import cgi, os, cgitb
cgitb.enable ()

text = "As you walk closer to the sound"
text2 = "of water, it goes from a mere"
text3 = "trickle to a deluge, and you find"
text4 = "the source, a waterfall in a dead"
text5 = "end.  You can either climb up the"
text6 = "waterfall, or you could go with"
text7 = "the flow, and be carried down"
text8 = "the river."

combtext = '<font size = 20>' + '<p style="text-align: center;">' + text + '<br>' + text2 + '<br>' + text3 + '<br>' + text4 + '<br>' + text5 + '<br>' + text6 + '<br>' + text7  + '<br>' + text8 + '</font>'

button1 ='<form name="input" action="9.py" method="get"><input type="submit" value="Climb!"></form>'
button2 ='<form name="input" action="8.py" method="get"><input type="submit" value="Drift"></form>'
buttons ='<div style="text-align:center">' + '<img src="Waterfall.gif" alt="waterfall"><br>(Image credits: http://a2.ec-images.myspacecdn.com/images02/148/7281422d85f44e32929cfd57df1e63ab/l.gif)</font><br><br>' + button1 + '<br>' + button2 + '</div>'

html = combtext + buttons

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
            info[3] = "57"
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

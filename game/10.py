#!/usr/bin/python
print "Content-Type: text/html\n"

import cgi, os, cgitb
cgitb.enable ()

text= "Incedibly fatigued, you roll"
text2 = " climb out of the waterfall"
text3 = "into a dense forest..."
dots = "..."
text4 = "and right in front of a bear."
text5 = "You could run from it, or"
text6 = "climb up a tree.  Either way,"
text7 = "your luck sucks."

formatted = '<font size = "20"><p style="text-align: center;">' + text + '<br>' + text2 + '<br>' + text3 + '<br>' + dots + '<br>' + text4 + '<br>' + text5 + '<br>' + text6 + '<br>' + text7

button1 ='<form name="input" action="chased.html" method="get"><input type="submit" value="RUN!"></form>'
button2 ='<form name="input" action="13.py" method="get"><input type="submit" value="CLIMB!"></form>'

formatbutton = '<div style="text-align:center">' + '<img src="Bear.jpg" alt="bear"><br><font size="1">(Image credits: http://www.facebook.com/l.php?u=http%3A%2F%2Fwww.backcountrygallery.com%2Fphotos%2Fblack-bear-stare-down%2F&h=3AQEuDwS0)<br><br>' + button1 + '<br>' + button2
 
html = formatted + '<br></p>' + formatbutton

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
            info[3] = "75"
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

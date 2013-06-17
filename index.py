#! /usr/bin/python
print "Content-Type:text/html\n"

import cgi,cgitb,os
cgitb.enable()

def loggedin():
    ip = os.environ['REMOTE_ADDR'] # Saves the person's ip address as a variable
    inStream = open('loggedin.txt','r') # Opens the file for the users that are logged in
    data = inStream.read().split('\n')
    inStream.close()
    accounts = {}
    for account in data:
        account = account.split(',')
        try:
            accounts[account[1]] = account[0]
        except:
            pass
    if accounts.has_key(ip): # If the ip matches one of the ip's of the logged in users, change the navigation bar to reflect the user
        retStr = '<li><a href="home/"><i class="icon-user" style="vertical-align:-10%;"></i> ' + accounts[ip].capitalize() + '</a></li><li><a href="logout.py">Logout</a></li>'
        return retStr
    else: # If the ip matches nothing (person is not logged in), show the default navigation bar
        return '<li><a href="accounts/">Login / Register</a></li>'

def main():
    inStream = open('template.html','r') # Reads the template html file
    html = inStream.read()
    inStream.close()
    html = html.replace('<li><a href="accounts/">Login / Register</a></li>',loggedin()) # This allows multiple people to use the site at once since python generates the html pages based on whether they are logged in or not
    print html

main()

#! /usr/bin/python
print "Content-Type:text/html\n"

import cgi,cgitb,os
cgitb.enable()

def loggedin():
    ip = os.environ['REMOTE_ADDR'] # Gets the ip address of the user
    inStream = open('loggedin.txt','r') # Opens the file with the list of logged in users
    data = inStream.read().split('\n')
    inStream.close()
    accounts = {}
    for account in data:
        account = account.split(',')
        try:
            accounts[account[1]] = account[0] # Creates a dictionary out of the list of logged in users so that it'll be easier to search
        except:
            pass
    if accounts.has_key(ip): # Attempts to find the user that is logged in with the ip, if the ip is connected to a user, then change the navigation bar to reflect the user
        retStr = '<li><a href="home/"><i class="icon-user" style="vertical-align:-10%;"></i> ' + accounts[ip].capitalize() + '</a></li><li><a href="logout.py">Logout</a></li>'
        return retStr
    else: # Otherwise, just gives the original navigation bar
        return '<li><a href="accounts/">Login / Register</a></li>'

def main():
    inStream = open('header.html','r') # Opens the header file, which is bascially just the header for our pages
    html = inStream.read()
    inStream.close()
    html = html.replace('<li><a href="accounts/">Login / Register</a></li>',loggedin()) # Runs the function above to reflect logged in users
    try:
        search = cgi.FieldStorage()
        string = search['search'].value.lower() # Gets the value of the search input
        htmlStr = ""
        inStream = open('accounts.txt','r') # Opens the list of accounts and parses it
        accounts = inStream.read().split('\n')
        for account in accounts:
            account = account.split('$!&spt&!$')
            if account[0].lower().find(string) != -1: # If the username contains any part of the search string, it will include that in the generated html page
                htmlStr += '<h2><a href="home/?profile=' + account[0] + '">' + account[0].capitalize() + '</h2><hr>'
        if htmlStr == "": # If there are no results for the html page, then it returns that there are no results
            htmlStr = "<br><h1>Sorry! Your search returned no results</h1>"
        html = html.replace('placeholder="Search..."','placeholder="Search..." value="' + string + '"') # Keeps the person's search query in the search bar
        html = html.replace('Everything About Stuy','Search: ' + string) # Changes the title to reflect what the person searched
        html = html.replace('REPLACE',htmlStr) # This is the list of results that matched the search string
    except: # When the person does not search anything, it goes to this part of the code where it just tells them that no results were found
        html = html.replace('Everything About Stuy','Search: No results')
        html = html.replace('REPLACE','<br><h1>Sorry! Your search returned no results</h1>')
        
    print html

main()

#! /usr/bin/python
print "Content-Type:text/html\n"

import cgi,cgitb,os
cgitb.enable()

def logout():
    ip = os.environ['REMOTE_ADDR'] # Records the ip address of the user
    inStream = open('loggedin.txt','r') # Reads the list of users logged in to find the ip of the user currently logged in on the computer
    data = inStream.read().split('\n')
    data.pop()
    inStream.close()
    writeStr = ""
    for line in data:
        check = line.split(',')
        if check[1] != ip: # While it goes through each ip address in the file, it will skip over it, until it gets to the ip of the logged in user. It will take that ip and remove it from the file (basically does not rewrite that ip address back to the file).
            writeStr += line + '\n'
    logOut = open('loggedin.txt','w')
    logOut.write(writeStr)
    logOut.close() 

def main():
    logout()
    inStream = open('accounts/redirect.html','r') # This opens a redirect page for logging out
    html = inStream.read()
    inStream.close()
    html = html.replace('../home/','.') # Just some path references that need to be changed since redirect.html is not in the same folder as logout.py
    html = html.replace('../','')
    html = html.replace('.">Login','accounts/">Login')

    print html

main()

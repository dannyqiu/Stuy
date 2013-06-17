#! /usr/bin/python
print "Content-Type: text/html\n"

import cgi,cgitb,os
cgitb.enable()

def check(username,password):
    inStream = open('../accounts.txt','r') # Opens the file with all the usernames and passwords
    data = inStream.read().split('\n') # Parses the data that is read from it into lines that seperate each uers's info
    inStream.close()
    accounts = {}
    for account in data:
        account = account.split('$!&spt&!$')
        try:
            accounts[account[0]] = account[1] # Creates a dictionary in the format username:password
        except:
            pass
    try:
        return accounts[username] == password # Checks to see if the password inputted is the same as the password for that username in the accounts.txt file
    except:
        return "noexist" # This is the error part of the code where the user doesn't exist (person is trying to log into an account that doesn't exist)

def main():
    form = cgi.FieldStorage()
    try:
        if form['submit'].value == 'login': # Makes sure that the person is trying to login
            username = form['user'].value # Gets the username from the username field
            password = form['pass'].value # Gets the password from the password field
            checked = check(username,password) # Runs the above function on the username and password to see if the combination is correct for an account
            if checked == True: # If the account credentials are correct
                ip = os.environ['REMOTE_ADDR']
                logIn = open('../loggedin.txt','a') # It logs someone in so that they stay logged in 
                writeStr = username + ',' + ip + '\n'
                logIn.write(writeStr)
                logIn.close()
                inStream = open('redirect.html','r') # Redirects the user to their profile page when they log in
                html = inStream.read()
                inStream.close()
            elif checked == 'noexist':
                inStream = open('template.html','r') # If the account doesn't exist, the it will show the default message
                html = inStream.read()
                inStream.close()
                html = html.replace('<!-- Error -->','''
            <div class="alert alert-error">
                You don't seem to be registered. Please register on the right so that you can access the amazing features of this site!
            </div>''') # This shows an error message saying that the username doesn't exist
            else:
                inStream = open('template.html','r') # This else statement is for when the username/password combination is not correct
                html = inStream.read()
                inStream.close()
                html = html.replace('<!-- Error -->','''
            <div class="alert alert-error">
                Incorrect username/password combination
            </div>''') # The default page is shown except that there is an error message at the top explainging that the username/password combination is wrong
        else:
            open('error','r') # This will go to the except part of the code if the person is not logging in, basically returns the default page
    except:
        inStream = open('template.html','r') # Returns the deafult page
        html = inStream.read()
        inStream.close()

    print html

main()

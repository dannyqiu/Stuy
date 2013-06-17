#! /usr/bin/python
print "Content-Type: text/html\n"

import cgi,cgitb,os,random
cgitb.enable()

def usernameTaken(username):
    lowercaseUser = username.lower() # Changes the username to lowercase to prevent duplicate usernames that take advantage of case-sensitive stuff
    inStream = open('../accounts.txt','r')
    data = inStream.read().split('\n')
    inStream.close()
    accounts = {}
    for account in data:
        account = account.split('$!&spt&!$')
        if account[0].lower() == lowercaseUser: # Checks to see if the lowercase username is the same as a username that is already present (this check is all performed in lower case characters, so it is NOT case sensitive)
            return True # Returns that the username is taken
    return False # Username is available

def main():
    form = cgi.FieldStorage()
    try:
        if form['submit'].value == 'register': # Makes sure that the person is here to register
            username = form['user'].value
            password = form['pass'].value
            if form.has_key('email'): # Checks to see if the email form is filled out, if it's not, then just put in "None"
                email = form['email'].value
            else:
                email = 'None'
            if len(username) > 15:
                inStream = open('template.html','r')
                html = inStream.read()
                inStream.close()
                html = html.replace('<!-- Error -->','<div class="alert alert-error"> Your username is too long! Try using a shorter username!</div>')
            elif usernameTaken(username) == True: # Checks to see if the username is taken already
                inStream = open('template.html','r')
                html = inStream.read()
                inStream.close()
                error_msg = '''
            <div class="alert alert-error">
                Sorry! That username is already taken! Please choose a different username! Such as ''' + username + str(random.randint(0,10)) + '</div>'
                html = html.replace('<!-- Error -->',error_msg) # Gives an error message that the username is taken already and gives a suggestion which is just the username that was inputted concantenated with a number from 0-9
            else: # If the username is not taken
                ip = os.environ['REMOTE_ADDR'] # Gets the ip address of the person
                createAccount = open('../accounts.txt','a') # Opens the accounts.txt file and adds a new line for this new account
                writeStr = username + '$!&spt&!$' + password + '$!&spt&!$' + email + '\n'
                createAccount.write(writeStr)
                createAccount.close()
                loggingIn = open('../loggedin.txt','a') # Adds the user to a list of logged in users so that the person stays logged in
                writeStr = username + ',' + ip + '\n'
                loggingIn.write(writeStr)
                loggingIn.close()
                newProfile = open('../profiles.txt','a') # Creates a new profile for this person with default values for about, image, game progress, and wall posts
                writeStr = username + '$!&spt&!$Write Something About Yourself$!&spt&!$http://www.maynardiowa.org/No%20Photo%20Available.jpg$!&spt&!$0$!&spt&!$Stuy|userpost|Welcome to the site!|postsplit|\n-----\n'
                newProfile.write(writeStr)
                newProfile.close()
                inStream = open('redirect.html','r') # Redirects the person to their profile page upon successful creation of the account
                html = inStream.read()
                inStream.close()
                html = html.replace('content="0', 'content="3') # Changes the time for redirect so that people can see the message that they succesfully registered
                html = html.replace('<br>','''
            <div class="alert alert-success">
                Your account has been successfully created! Welcome to the site!
            </div>''') # Shows message that the person's account was created
        else:
            open('error','r') # To go to the except portion of the code so that it displays the default html code to register for an account
    except:
        inStream = open('template.html','r') # This is the default code for this html page
        html = inStream.read()
        inStream.close()

    print html

main()

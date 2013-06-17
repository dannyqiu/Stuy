#! /usr/bin/python
print "Content-Type:text/html\n"

import cgi,cgitb,os
cgitb.enable()

def loggedin(profile): # This is basically the same code to check if someone is logged in already. However, this has an input in which 0 would give the html ode for the navigation bar and 1 would give you the account that is logged in from that ip address
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
            retStr = '<li class="active"><a href="."><i class="icon-user" style="vertical-align:-10%;"></i> ' + accounts[ip].capitalize() + '</a></li><li><a href="../logout.py">Logout</a></li>'
            return retStr
    else: # Person is not logged in or accessing from different ip
        if profile == 1:
            return 'noexist'
        else:
            return '<li class="active"><a href="../accounts/">Login / Register</a></li>'

def getUser(user): # This function basically gets the information given a username
    inStream = open('../profiles.txt','r') # Opens the profile.txt file with the information on everyone's profile
    data = inStream.read().split('\n-----\n') # Splits up the profile file at the divider that we set
    inStream.close()
    profiles = {}
    for profile in data:
        profile = profile.split('$!&spt&!$') # Splits up each line of the profile into it's components: about, image link, game progress, wall posts
        try:
            profiles[profile[0]] = {'ABOUT':profile[1],'IMAGE':profile[2],'PROGRESS':profile[3],'POSTS':profile[4]} # Created a dictionary assigning values to each
        except:
            pass
    if profiles.has_key(user):
        return profiles[user]['ABOUT'],profiles[user]['IMAGE'],profiles[user]['PROGRESS'],profiles[user]['POSTS'] # Returns 4 values in the order shown

def main():
    inStream = open('settings.html','r') # Opens up the template file settings.html
    html = inStream.read()
    inStream.close()
    html = html.replace('<li class="active"><a href="../accounts/">Login / Register</a></li>',loggedin(0)) # Changes the navigation bar to reflect logged in users
    option = cgi.FieldStorage()
    profile = loggedin(1)
    accountEdit = open('../accounts.txt','r') # Reads the list of accounts to get the account data ready (Username + Password)
    accounts = accountEdit.read().split('\n')
    accounts.pop()
    accountEdit.close()
    profileEdit = open('../profiles.txt','r') # Reads the profile file to get the profiles data ready (About + Image Link + Game Progress + Wall Posts)
    profiles = profileEdit.read().split('\n-----\n')
    profiles.pop()
    profileEdit.close()
    if option.has_key('change'):
        try:
            if option['change'].value == 'password': # If the person pressed the change password button
                writeStr = ""
                for account in accounts:
                    line = account.split('$!&spt&!$') # Goes through each line of the accounts data and splits it into its component information
                    if line[0] == profile: # Checks to see if the account that you are currently trying to edit matches any usernames in the file
                        line[1] = option['password'].value # If it does, then that username's password is now set to the password that the person inputted in the box to change the password
                    account = '$!&spt&!$'.join(line) # Combies the information back into the format that is desired (split at every $!&spt&!$)
                    writeStr += account + '\n' # Puts everything in one write string and then finally seperated by a new line
                accountEdit = open('../accounts.txt','w') # Rewrites everything to the accounts file. It is designed so that nothing is changed except the password
                accountEdit.write(writeStr)
                accountEdit.close()
            elif option['change'].value == 'about': # If the person clicked the change about button
                writeStr = ""
                for user in profiles:
                    line = user.split('$!&spt&!$') # Goes through each line of the profile data and splits it into its components
                    if line[0] == profile: # When it loops through to the profile with the same username as the on that you are editting
                        line[1] = option['about'].value # Change the about value to the one set in the box
                    user = '$!&spt&!$'.join(line) # Combines the split data back into a string
                    writeStr += user + '\n-----\n' # Adds that string to the overall string that will be written back into the profiles.txt file along with the proper breaks between profiles
                profileEdit = open('../profiles.txt','w')
                profileEdit.write(writeStr) # Rewrites the profiles.txt file with the new profile data
                profileEdit.close()
            elif option['change'].value == 'image': # If the person clicked the change image button
                writeStr = ""
                for user in profiles:
                    line = user.split('$!&spt&!$') # This is basically the same code as the conditional clause above for changing the about, except now, it is designed to change the image link part of their profile data
                    if line[0] == profile:
                        line[2] = option['image'].value
                    user = '$!&spt&!$'.join(line)
                    writeStr += user + '\n-----\n'
                profileEdit = open('../profiles.txt','w')
                profileEdit.write(writeStr)
                profileEdit.close()
        except:
            pass
    accountEdit = open('../accounts.txt','r')
    accounts = accountEdit.read().split('\n')
    accounts.pop()
    for account in accounts:
        line = account.split('$!&spt&!$')
        if line[0] == profile:
            password = line[1] # These past 7 lines are to get the new password so that it's updated when the person changes their password
    try:
        about,image,progress,posts = getUser(profile) # Gets the data for the username, so it fetches the most up-to-date data on that username, meaning that it's updated the moment they change it on the edit.py page
        html = html.replace('USERNAME_ONLY',profile.capitalize()) # Just replaces the html template file with the data that pertains to the user
        html = html.replace('PASSWORD_ONLY',password)
        html = html.replace('USERNAME_ABOUT',about)
        html = html.replace('USERNAME_IMAGE',image)
    except: # This is the code that is run when the profile that they are trying to edit doesn't exist. Why is this necessary? Because some people like to break code, so yea, you probably won't ever see this error unless someone intentionally wants to break our code by trying to edit stuff that's not their's
        inStream = open('header.html','r')
        html = inStream.read()
        inStream.close()
        html = html.replace('Everything About Stuy','Nonexistant Profile')
        html = html.replace('<li><a href="../accounts/">Login / Register</a></li>',loggedin(0))
        html = html.replace('REPLACE','<h1>This profile does not exist!</h1>')

    print html

main()

#! /usr/bin/python
print "Content-Type:text/html\n"

import cgi,cgitb,os
cgitb.enable()

def loggedin(profile): # Same code as always, checks to see the logged in user associated with the ip address. Now it has an input where 1 would give the user that is logged in and 0 would give the html code for the navigation bar
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

def checkUser(profile): # Checks to see if the user's account is present in the list of accounts, if not, then it returns that the profile doesn't exist
    inStream = open('../accounts.txt','r')
    data = inStream.read().split('\n')
    for line in data:
        line = line.split('$!&spt&!$')
        if line[0] == profile:
            return profile
    return 'noexist'

def getUser(user): # Gets information about the profile and returns it in the format: about, image link, game progress, wall posts
    inStream = open('../profiles.txt','r')
    data = inStream.read().split('\n-----\n')
    inStream.close()
    profiles = {}
    for profile in data:
        profile = profile.split('$!&spt&!$')
        try:
            profiles[profile[0]] = {'ABOUT':profile[1],'IMAGE':profile[2],'PROGRESS':profile[3],'POSTS':profile[4]}
        except:
            pass
    if profiles.has_key(user):
        return profiles[user]['ABOUT'],profiles[user]['IMAGE'],profiles[user]['PROGRESS'],profiles[user]['POSTS']

def main():
    inStream = open('template.html','r') # Opens the template file for the user's profile page
    html = inStream.read()
    inStream.close()
    html = html.replace('<li class="active"><a href="../accounts/">Login / Register</a></li>',loggedin(0))
    option = cgi.FieldStorage()
    if option.has_key('profile'): # This is to check to see if the person wants to search up someone else's profile
        profile = checkUser(option['profile'].value) # Then it sets the current profile to that of the person requested in the query string, after checking to see if the profile exists using the checkUser function above
    else:
        profile = loggedin(1) # Otherwise, if there is no query string (the person wants to see their own profile)
    try:
        if option['submit'].value == 'post': # If the person is trying to post on someone else's wall
            inStream = open('../profiles.txt','r') # Opens the profiles file and reads it
            data = inStream.read().split('\n-----\n') # Splits the data read into its users
            data.pop()
            inStream.close()
            writeStr = ""
            for user in data:
                line = user.split('$!&spt&!$')
                if line[0] == profile: # When it gets to the line with the user that matches that of the current profile
                    if loggedin(1) == 'noexist': # If the person is not logged in
                        poster = 'ANONYMOUS' # It will post under the name 'ANONYMOUS'
                    else:
                        poster = loggedin(1).capitalize() # Otherwise, it will post under the user that's logged in's name
                    post = option['post'].value.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;').replace('|','&brvbar;').replace('\r\n','<br>').replace('\n','<br>') # Just replaces special characters for security reasons and replaces newlines in the submitted data with html line breaks so that they render in browser
                    appendStr = poster + '|userpost|' + post + '|postsplit|' # This will combine the poster and post with the necessary seperation data
                    user += appendStr # This is then added to the end of the line with the user matching the profile of the person having his wall posted on
                writeStr += user + '\n-----\n' # Writes it all back out to the profiles file with the line break to seperate each user
            postOut = open('../profiles.txt','w')
            postOut.write(writeStr)
            postOut.close()
    except: # If the person is not posting and decides to got to post.py, then it will just ignore the error that's generated from trying to retrieve what the person posted
        pass
    if profile == 'noexist': # If the profile doesn't exist, then display the html code for it telling them that the profile doesn't exist
        inStream = open('header.html','r')
        html = inStream.read()
        inStream.close()
        html = html.replace('Everything About Stuy','Nonexistant Profile')
        html = html.replace('<li><a href="../accounts/">Login / Register</a></li>',loggedin(0))
        html = html.replace('REPLACE','<h1>This profile does not exist!</h1>')
    else: # Otherwise if the profile existed, the it displays all the information that pertains to it by replacing the placeholders in the html file
        about,image,progress,posts = getUser(profile)
        html = html.replace('USERNAME_ONLY',profile.capitalize())
        html = html.replace('USERNAME_ABOUT',about)
        html = html.replace('USERNAME_IMAGE',image)
        html = html.replace('USERNAME_PROGRESS',progress)
        posts = posts.split('|postsplit|')
        postStr = ''
        for post in posts:
            post = post.split('|userpost|')
            try:
                postStr += '<div class="row"><div class="span2"><h4>' + post[0] + '</h4></div><div class="span6">' + post[1] + '</div></div><hr>'
            except:
                pass
        html = html.replace('USERNAME_POSTS',postStr)
    if os.environ['QUERY_STRING'] != "": # So if the person is not viewing their own profile (there is a query string that points to someone else's profile)
        html = html.replace('''<small><span class="pull-right"><button class="btn btn-info" onclick="location.href='edit.py'">Settings</button></small>''','') # The settings button is taken away since it's not your to edit
    query_string_handle = 'post.py?' + os.environ['QUERY_STRING'] # This code is to handle posting on someone else's page, it will change the post.py link to post.py with a query string attached so that when you post, the program will know who's wall you want to post to
    html = html.replace('post.py',query_string_handle) # Edits the post.py link to reflect the wall that you are posting to

    print html

main()

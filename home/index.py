#! /usr/bin/python
print "Content-Type:text/html\n"

import cgi,cgitb,os
cgitb.enable()

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
            retStr = '<li class="active"><a href="."><i class="icon-user" style="vertical-align:-10%;"></i> ' + accounts[ip].capitalize() + '</a></li><li><a href="../logout.py">Logout</a></li>'
            return retStr
    else: # Person is not logged in or accessing from different ip
        if profile == 1:
            return 'noexist'
        else:
            return '<li class="active"><a href="../accounts/">Login / Register</a></li>'

def checkUser(profile): # This is to check if the user that is passed into this function exists or not
    inStream = open('../accounts.txt','r')
    data = inStream.read().split('\n')
    for line in data:
        line = line.split('$!&spt&!$')
        if line[0] == profile: # Basically, if it can find the user in the accounts file, then it just returns the username with no problem
            return profile
    return 'noexist' # Otherwise, it will return that the username doesn't exist

def getUser(user): # This function gets the necessary data from the profiles.txt file on the user that you input into this function. It will return 4 things: about, image link, game progress, and the posts on the user's wall
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
    html = html.replace('<li class="active"><a href="../accounts/">Login / Register</a></li>',loggedin(0)) # Modifys the navigation bar to reflect users that are logged in
    option = cgi.FieldStorage()
    if option.has_key('profile'): # This is to check to see if the person wants to search up someone else's profile
        profile = checkUser(option['profile'].value) # Then it sets the current profile to that of the person requested in the query string, after checking to see if the profile exists using the checkUser function above
    else:
        profile = loggedin(1) # Otherwise, if there is no query string (the person wants to see their own profile)
    if profile == 'noexist': # If profile is equal to 'noexist', which is what the code right above is for, then open the header.html file (it is just a regular file with the navigation bar on it) and replace the elements so that it shows that the profile doesn't exist
        inStream = open('header.html','r')
        html = inStream.read()
        inStream.close()
        html = html.replace('Everything About Stuy','Nonexistant Profile')
        html = html.replace('<li><a href="../accounts/">Login / Register</a></li>',loggedin(0))
        html = html.replace('REPLACE','<h1>This profile does not exist!</h1>')
    else: # If the profile does exist
        about,image,progress,posts = getUser(profile) # Then it retrieves the information on that profile
        html = html.replace('USERNAME_ONLY',profile.capitalize()) # Replaces all the placeholders in the html file to reflect the profile information of the profile that is being looked at
        html = html.replace('USERNAME_ABOUT',about)
        html = html.replace('USERNAME_IMAGE',image)
        html = html.replace('USERNAME_PROGRESS',progress)
        posts = posts.split('|postsplit|') # This next section of the code formats the way that the posts will look like on the page, first splits it into seperate posts
        postStr = ''
        for post in posts: # Loops through each post
            post = post.split('|userpost|') # Seperates the posts into user that posted and post
            try:
                postStr += '<div class="row"><div class="span2"><h4>' + post[0] + '</h4></div><div class="span6">' + post[1] + '</div></div><hr>' # This is the layout code for each post
            except:
                pass
        html = html.replace('USERNAME_POSTS',postStr) # Replaces the posts section with the generated html for posts
    if os.environ['QUERY_STRING'] != "": # So if the person is not viewing their own profile (there is a query string that points to someone else's profile)
        html = html.replace('''<small><span class="pull-right"><button class="btn btn-info" onclick="location.href='edit.py'">Settings</button></small>''','') # The settings button is taken away since it's not your to edit
    query_string_handle = 'post.py?' + os.environ['QUERY_STRING'] # This code is to handle posting on someone else's page, it will change the post.py link to post.py with a query string attached so that when you post, the program will know who's wall you want to post to
    html = html.replace('post.py',query_string_handle) # Edits the post.py link to reflect the wall that you are posting to

    print html

main()

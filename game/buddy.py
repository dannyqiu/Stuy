#! /usr/bin/python
print "Content-Type: text/html\n"

import cgi,cgitb,os
cgitb.enable()

html = '''
<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8">
        <title>Your Interactive Buddy!</title>
        <meta name"description" content="Learn more about Stuyvesant High School! Everything from facts about the school, about the teachers, student reviews are all compiled in one place!">
        <link rel="stylesheet" href="../css/bootstrap.min.css">
        <link rel="stylesheet" href="../css/bootstrap-responsive.min.css">
        <link rel="stylesheet" href="../css/main.css">
        <script src="http://code.jquery.com/jquery.min.js"></script>
        <script>window.jQuery || document.write('<script src="../js/jquery-1.10.0.min.js"><\/script>')</script>
        <script src="../js/bootstrap.min.js"></script>
        <link href='http://fonts.googleapis.com/css?family=Open+Sans|Finger+Paint' rel='stylesheet' type='text/css'>
    </head>
    <body>
        <div class="navbar navbar-fixed-top" style="font-family:Open Sans;">
            <div class="navbar-inner">
                <div class="container">
                    <a class="brand" href=".."><i class="icon-home" style="vertical-align:0%;"></i> Stuy</a>
                        <form class="navbar-search pull-left" method="POST" action="../search.py">
                            <div class="input-append">
                                <input type="text" class="span6" name="search" placeholder="Search...">
                                <button type="submit" class="btn" name="submit" value="search"><i class="icon-search"></i></button>
                            </div>
                        </form>
                    <a class="btn btn-navbar" data-toggle="collapse" data-target=".nav-collapse">
                        <span class="icon-bar"></span>
                        <span class="icon-bar"></span>
                        <span class="icon-bar"></span>
                    </a>
                    <div class="nav-collapse collapse">
                        <ul class="nav pull-right">
                            <li class="active"><a href=".">Game</a></li>
                            <li class="divider-vertical"></li>
                            <li><a href="../accounts/">Login / Register</a></li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>
        <div class="container">
            <h1>Your Interactive Buddy!</h1>
            <div style="margin-top:45px;">
                <applet code="org.nlogo.lite.Applet" archive="https://dl.dropboxusercontent.com/u/66952951/NetLogo/NetLogoLite.jar" width="928" height="513">
                    <param name="DefaultModel" value="https://dl.dropboxusercontent.com/u/66952951/NetLogo/Interactive-Buddy.nlogo">
                    <param name="java_arguments" value="-Djnlp.packEnabled=true">
                </applet>
            </div>
        </div>
    </body>
</html>'''

def loggedin():
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
        retStr = '<li><a href="../home/"><i class="icon-user" style="vertical-align:-10%;"></i> ' + accounts[ip].capitalize() + '</a></li><li><a href="../logout.py">Logout</a></li>'
        return retStr
    else: # Person is not logged in or accessing from different ip
        return '<li><a href="../accounts/">Login / Register</a></li>'

html = html.replace('<li><a href="../accounts/">Login / Register</a></li>',loggedin())
print html

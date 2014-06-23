#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import webapp2
import os
import urllib
import jinja2
import datetime
import sys

from google.appengine.api import mail
from google.appengine.api import users
from google.appengine.api import urlfetch
from google.appengine.ext import db

from models import User

if 'libs' not in sys.path:
    sys.path[0:0] = ['libs']


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)

class MainHandler(webapp2.RequestHandler):
    def get(self):
        from tweepy import API
        template = JINJA_ENVIRONMENT.get_template('templates/home.html')
        self.response.write(template.render({}))

    def post(self):
        #env variables
        admin_mail = os.environ['admin_mail']
        hashtag = os.environ['hashtag']
        website_name = os.environ['website_name']

        #
        pseudo_taken = False
        mail_taken = False


        #Get variables from post
        date1 = int( self.request.get('date1') )
        date2 = int( self.request.get('date2') )
        date3 = int( self.request.get('date3') )
        email=self.request.get('mail')
        twitterUsername = self.request.get('twitterUsername')
        lastName=self.request.get('lastName')
        firstName=self.request.get('firstName')
        now = datetime.datetime(date3,date2,date1)

        #template
        template = JINJA_ENVIRONMENT.get_template('templates/template.html')

        #verify twitter pseudo is not taken
        users = db.GqlQuery("SELECT * FROM User WHERE twitterUsername ='%s'" %(twitterUsername,) )
        for res in users:
            pseudo_taken = True
            print 'your username is already taken'
            if res.active:
                print 'profile active'
                templateVars = { "message" : "There's already an account with this twitter username"}
                self.response.write(template.render(templateVars) )
                return
            else:
                print 'profile not active'
                res.active = True
                res.mail=email
                res.lastName = lastName
                res.firstName = firstName
                res.timestamp=now
                res.put()
                templateVars = { "message" : "you are signed in, you can now use the '%s' functionnality" %(hashtag,) }
                self.response.write(template.render(templateVars) )
                sendMail(email,twitterUsername,firstName,admin_mail,hashtag)

        #verify mail is not taken
        mails = db.GqlQuery("SELECT * FROM User WHERE mail ='%s'" %(email,) )
        for res in mails:
            mail_taken = True
            print 'your mail is already taken'
            if res.active:
                print 'profile active'   
                templateVars = { "message" : "There's already an account with this mail adress"}
                self.response.write(template.render(templateVars) )
                return
            else:
                print 'profile not active'
                res.active = True
                res.twitterUsername = twitterUsername
                res.lastName = lastName
                res.firstName = firstName
                res.timestamp=now
                res.put()
                templateVars = { "message" : "you are signed in, you can now use the '%s' functionnality" %(hashtag,) }
                self.response.write(template.render(templateVars) )
                sendMail(email,twitterUsername,firstName,admin_mail,hashtag)

        #Add user
        if not pseudo_taken and not mail_taken:
            self.user = User(
                lastName=lastName,
                firstName=firstName,
                twitterUsername=twitterUsername,
                mail=email,
                timestamp=now,
                active=True
            )
            self.user.put()

            templateVars = { "message" : "you are signed in, you can now use the '%s' functionnality" %(hashtag,) }
            self.response.write(template.render(templateVars) )

            sendMail(email,twitterUsername,firstName,admin_mail,hashtag)


def sendMail(email,twitterUsername,firstName,admin_mail,hashtag):
    message = mail.EmailMessage(sender="Admin <%s>"%(admin_mail,), subject="Inscription")
    message.to = "%s <%s>"%(twitterUsername,email)
    message.body = """
        Hi %s

        Thanks for your subscription, you can now use the %s functionnality, see you soon
    """ % (firstName,hashtag)
    message.send()



app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)














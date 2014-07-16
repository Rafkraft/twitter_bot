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
import hmac
import hashlib
import time

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

class addUser(webapp2.RequestHandler):
    def get(self):
        from tweepy import API
        template = JINJA_ENVIRONMENT.get_template('templates/template.html')
        templateVars = { "message" : "" }
        self.response.write(template.render(templateVars) )

    def post(self):
        #env variables
        admin_mail = os.environ['admin_mail']
        hashtag = os.environ['hashtag']
        website_name = os.environ['website_name']

        #initialize
        pseudo_taken = False
        mail_taken = False


        #Get variables from post
        secret_key = os.environ['PRIVATE_CRYPTO_KEY']

        date1 = self.request.get('date1')
        date2 = self.request.get('date2')
        date3 = self.request.get('date3')
        date = "%s-%s-%s" % (date3, date2,date1)

        email=self.request.get('mail')
        firstName=self.request.get('firstName')
        lastName=self.request.get('lastName')
        twitterUsername = self.request.get('twitterUsername')        
        timestamp=self.request.get('timestamp')
        recieved_crypto = self.request.get('message_auth')

        to_compose = [email, firstName, lastName, twitterUsername, date1, date2, date3, timestamp]
        to_compose = ";".join(str(x) for x in to_compose)

        hashobj = hmac.new(str(secret_key), to_compose, digestmod = hashlib.sha1)
        message_auth = hashobj.hexdigest()

        if recieved_crypto != message_auth:
            raise Exception('ppooo')
        else:
            print "request verified"

        date1 = int(date1)
        date2 = int(date2)
        date3 = int(date3)

        now = datetime.datetime(date3, date2, date1)

        #template
        template = JINJA_ENVIRONMENT.get_template('templates/template.html')

        #verify mail is not taken
        mails = db.GqlQuery("SELECT * FROM User WHERE mail ='%s'" %(email,) )
        for res in mails:
            mail_taken = True
            print 'the mail exists'
            if res.active:
                print 'profile active' 
                res.active = True
                res.twitterUsername = twitterUsername
                res.lastName = lastName
                res.firstName = firstName
                res.timestamp=now
                res.put()
                templateVars = { "message" : "The account exists and the infos have been updated"}
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

        #if mail is not taken, create a new user
        if not mail_taken:
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
    ('/addUser', addUser)
], debug=True)
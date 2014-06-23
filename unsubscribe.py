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



class Unsubscribe(webapp2.RequestHandler):
    def get(self):
        from tweepy import API
        template = JINJA_ENVIRONMENT.get_template('templates/unsubscribe.html')
        self.response.write(template.render({}))

    def post(self):

        #Get variables from post
        twitterUsername = self.request.get('twitterUsername')

        found = False

        template = JINJA_ENVIRONMENT.get_template('templates/template.html')

        #get pseudo
        users = db.GqlQuery("SELECT * FROM User WHERE twitterUsername ='%s'" %(twitterUsername) )
        for res in users:
            found = True
            if not res.active:
                #already deactivated                   
                templateVars = { "message" : 'you account is already deactivated'}
                self.response.write(template.render(templateVars) )
            else:
                #now deactivated
                print 'correspondance'
                res.active=False                    
                res.put()
                templateVars = { "message" : 'you account has been deactivated'}
                self.response.write(template.render(templateVars) )
                sendMail(res.mail,res.twitterUsername,res.firstName)
        if not found:
            templateVars = { "message" : "there is no profile linked to this username"}
            self.response.write(template.render(templateVars) )


def sendMail(email,twitterUsername,firstName):
    message = mail.EmailMessage(sender="Admin <%s>"%(os.environ['admin_mail']), subject="Account unactivated")
    message.to = "%s <%s>"%(twitterUsername,email)
    message.body = """
        Hi %s

        Your account has been deactivated
    """%(firstName)
    message.send()



app = webapp2.WSGIApplication([
    ('/unsubscribe', Unsubscribe)
], debug=True)














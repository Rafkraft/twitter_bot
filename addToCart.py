import webapp2
import os
import urllib
import jinja2
import datetime
import sys
import json


from google.appengine.api import users
from google.appengine.api import urlfetch
from google.appengine.ext import db

if 'libs' not in sys.path:
    sys.path[0:0] = ['libs']

from icebergsdk.api import IcebergAPI


class addToCart(webapp2.RequestHandler):
    def add(self,id,email,first_name,last_name):
        import logging
        logging.basicConfig(level=logging.DEBUG)

        api_handler = IcebergAPI()
        #api_hander = IcebergAPI(username = "rafkraft", access_token = "593aab9b65cfbad5a34951cf1b94769f6fb7bfb3")
        #api_hander.sso(email = "connect@yahoo.fr", first_name="Florian", last_name="Poullin")
        api_handler.sso(email, first_name, last_name)

       
        user_cart = api_handler.Cart.mine()

        product = api_handler.ProductOffer.find(id)
       

        user_cart.addOffer(product)

        user_cart = api_handler.Cart.mine()
        print user_cart.__dict__


    def get(self):
        import logging
        logging.basicConfig(level=logging.DEBUG)

        api_handler = IcebergAPI()
        #api_hander = IcebergAPI(username = "rafkraft", access_token = "593aab9b65cfbad5a34951cf1b94769f6fb7bfb3")
        #api_hander.sso(email = "connect@yahoo.fr", first_name="Florian", last_name="Poullin")
        api_handler.sso("connect@yahoo.fr", "Florian", "Poullin")

        #print api_handler.get_me()

        user_cart = api_handler.Cart.mine()
        #print user_cart

        product = api_handler.ProductOffer.find(52)
        #print product.__dict__

        user_cart.addOffer(product)

        user_cart = api_handler.Cart.mine()
        print user_cart.__dict__


        #variables = dir()
        #happyHandler =  dir(variables[0])
        #print happyHandler



        


app = webapp2.WSGIApplication([
    ('/addToCart', addToCart)
], debug=True)




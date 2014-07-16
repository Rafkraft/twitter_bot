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

def add_to_cart(id,email,first_name,last_name):
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

app = webapp2.WSGIApplication([
    ('/CartHandler', add_to_cart)
], debug=True)




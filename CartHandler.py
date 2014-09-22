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

    print 'addToCart'

    api_handler = IcebergAPI()

    #Identification 
    api_handler.sso(email, first_name, last_name)
    print 'connected'

    #Get cart
    user_cart = api_handler.Cart.mine()

    #Find product
    product = api_handler.ProductOffer.find(id)

    print 'product'
    print product
   
    #Add product to cart
    user_cart.addOffer(product)

    user_cart = api_handler.Cart.mine()   

    print user_cart


app = webapp2.WSGIApplication([
    ('/CartHandler', add_to_cart)
], debug=True)




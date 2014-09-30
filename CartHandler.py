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

def add_to_cart(object_id, email,first_name,last_name,size):
    import logging
    logging.basicConfig(level=logging.DEBUG)

    print 'addToCart'

    api_handler = IcebergAPI()

    #Identification 
    api_handler.sso(email, first_name, last_name)
    print 'connected'

    #Get cart
    user_cart = api_handler.Cart.mine()
    

    print 'USER FETCHED :'
    print api_handler.get_my_cart()['total_amount']
    print api_handler.get_my_cart()['user']['id']
    print api_handler.get_my_cart()['user']['username']
    print api_handler.get_my_cart()['user']['last_name']
    print api_handler.get_my_cart()['user']['first_name']

    #Find product
    product = api_handler.Product.find(object_id)

    print ' product'
    #print product
    #print product.best_offer.to_JSON()

    def addOffer(offer):
        print "adding offer"
        user_cart.addOffer(offer)
        print "product %s added, no variation"%(offer.name)

    def addVariationOffer(variation, offer):
        print "adding variation offer"
        user_cart.addVariation(variation, offer)
        print "product %s added, variation %s"%(offer.name,variation.name)
        print api_handler.get_my_cart()['total_amount']

    if(len(product.best_offer.variations)>0):
        if(size):
            for variation in product.best_offer.variations:
                if(variation.name==size):
                    addVariationOffer(variation, product.best_offer)
                else:
                    addVariationOffer(product.best_offer.variations[0], product.best_offer)
        else:
            addVariationOffer(product.best_offer.variations[0], product.best_offer)
    else:
        addOffer(product.best_offer)






app = webapp2.WSGIApplication([
    ('/CartHandler', add_to_cart)
], debug=True)




# -*- coding: utf-8 -*-

from icebergsdk.resources.base import UpdateableIcebergObject

from icebergsdk.exceptions import IcebergNoHandlerError
from icebergsdk.resources.order import Order

class Cart(UpdateableIcebergObject):
    endpoint = 'cart'

    @classmethod
    def mine(cls):
        """
        Return current Cart for logged user
        """
        if not cls._handler:
            raise IcebergNoHandlerError()

        data = cls._handler.request("%s/mine/" % (cls.endpoint))
        return cls.findOrCreate(data)

    def form_data(self):
        """
        Return Payment Form data
        """
        return self.request("%s%s/" % (self.resource_uri, 'backend_form_data'))

    def items(self):
        """
        Return CartItems
        """
        return self.get_list('%sitems/' % self.resource_uri)
        

    def createOrder(self, params = None):
        """
        If Cart is valid, create an Order from it
        """
        params = params or {}

        data = self.request("%s%s/" % (self.resource_uri, 'createOrder'), method = "post", post_args = params)
        return Order.findOrCreate(data)

    def addOffer(self, product_offer):
        """
        Add an offer to the Cart
        """
        params = {
            'offer_id': product_offer.id,
            'quantity': 1
        }
        self.request("%s%s/" % (self.resource_uri, 'items'), post_args = params, method = "post")
        return self

    def addVariation(self, product_variation, product_offer):
        """
        product_offer is optional
        """
        params = {
            'variation_id': product_variation.id,
            'offer_id': product_offer.id,
            'quantity': 1
        }            

        self.request("%s%s/" % (self.resource_uri, 'items'), post_args = params, method = "post")
        return self



class CartItem(UpdateableIcebergObject):
    endpoint = 'cart_item'




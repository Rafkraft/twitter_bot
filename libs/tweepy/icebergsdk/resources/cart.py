# -*- coding: utf-8 -*-

from icebergsdk.resources.base import UpdateableIcebergObject

from icebergsdk.exceptions import IcebergNoHandlerError
from icebergsdk.resources.order import Order

class Cart(UpdateableIcebergObject):
    endpoint = 'cart'

    @classmethod
    def mine(cls):
        if not cls.handler:
            raise IcebergNoHandlerError()

        data = cls.handler.request("%s/mine/" % (cls.endpoint))
        return cls.findOrCreate(data)

    def form_data(self):
        """
        Return Payment Form data
        """
        return self.request("%s%s/" % (self.resource_uri, 'backend_form_data'))
        

    def createOrder(self, params = {}):
        data = self.request("%s%s/" % (self.resource_uri, 'createOrder'), method = "post", post_args = params)
        return Order.findOrCreate(data)

    def addOffer(self, product_offer):
        params = {
            'offer_id': product_offer.id,
            'quantity': 1
        }
        self.request("%s%s/" % (self.resource_uri, 'items'), post_args = params, method = "post")
        return self

    def addVariation(self, product_variation):
        raise NotImplementedError()


class CartItem(UpdateableIcebergObject):
    endpoint = 'cart_item'
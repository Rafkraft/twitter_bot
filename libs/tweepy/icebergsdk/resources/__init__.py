# -*- coding: utf-8 -*-

from icebergsdk.resources.application import Application
from icebergsdk.resources.order import Order
from icebergsdk.resources.cart import Cart
from icebergsdk.resources.product import Product, ProductOffer, ProductVariation
from icebergsdk.resources.store import Store
from icebergsdk.resources.user import User, Profile
from icebergsdk.resources.address import Address, Country
from icebergsdk.resources.payment import Payment

def get_class_from_resource_uri(resource_uri):
    types = {
        "product_offer": ProductOffer,
        "product": Product,
        "user": User,
        "address": Address,
        "profile": Profile,
        "payment": Payment
    }

    # Hack for now
    for resource, klass in types.iteritems():
        if resource in resource_uri:
            return klass

    raise NotImplementedError()


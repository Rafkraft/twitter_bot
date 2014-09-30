# -*- coding: utf-8 -*-

import logging

from icebergsdk.resources.application import Application
from icebergsdk.resources.order import Order, MerchantOrder, OrderItem
from icebergsdk.resources.cart import Cart, CartItem
from icebergsdk.resources.product import Product, ProductOffer, ProductVariation, ProductOfferImage, Category, Brand
from icebergsdk.resources.store import Store, MerchantImage, MerchantAddress
from icebergsdk.resources.user import User, Profile, UserShoppingPreference
from icebergsdk.resources.address import Address, Country
from icebergsdk.resources.payment import Payment
from icebergsdk.resources.message import Message
from icebergsdk.resources.review import Review, MerchantReview

logger = logging.getLogger('icebergsdk')

def get_class_from_resource_uri(resource_uri):
    types = {
        "application": Application,
        "product": Product,
        "productoffer": ProductOffer,
        "offer_image": ProductOfferImage,
        "product_variation": ProductVariation,
        "user": User,
        "address": Address,
        "country": Country,
        "brand": Brand,
        "profile": Profile,
        "user_shopping_prefs": UserShoppingPreference, 
        "payment": Payment,
        "merchant": Store,
        "merchant_address": MerchantAddress,
        "merchant_image": MerchantImage,
        "order": Order,
        "merchant_order": MerchantOrder,
        "message": Message,
        "cart": Cart,
        "cart_item": CartItem,
        "order_item": OrderItem,
        "review": Review,
        "merchant_review": MerchantReview,
        "category": Category
    }

    # Hack for now... Will be changed
    for resource, klass in types.iteritems():
        if "/%s/" % resource in resource_uri:
            return klass

    logger.error('cant find resource for %s' % resource_uri)
    raise NotImplementedError()


# -*- coding: utf-8 -*-


from icebergsdk.resources.base import UpdateableIcebergObject, IcebergObject

"""
Todo: Add addToCart method to ProductOffer and ProductVariation

"""

class Product(UpdateableIcebergObject):
    endpoint = 'product'

    def reviews(self):
        return self.get_list('review', args = {'product': self.id})

class ProductOffer(UpdateableIcebergObject):
    endpoint = 'productoffer'

class ProductVariation(UpdateableIcebergObject):
    endpoint = 'product_variation'

class ProductOfferImage(UpdateableIcebergObject):
    endpoint = 'offer_image'

class Category(IcebergObject):
    endpoint = 'category'

class Brand(IcebergObject):
    endpoint = 'brand'

# -*- coding: utf-8 -*-


from icebergsdk.resources.base import IcebergObject

class Product(IcebergObject):
    endpoint = 'product'
    api_type = "p"

class ProductOffer(IcebergObject):
    endpoint = 'productoffer'

class ProductVariation(IcebergObject):
    endpoint = 'product_variation'



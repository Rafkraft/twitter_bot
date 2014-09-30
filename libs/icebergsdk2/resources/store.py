# -*- coding: utf-8 -*-

from icebergsdk.resources.base import IcebergObject

class Store(IcebergObject):
    endpoint = 'merchant'

    def product_offers(self):
        return self.get_list('productoffer', args = {'merchant': self.id})
    

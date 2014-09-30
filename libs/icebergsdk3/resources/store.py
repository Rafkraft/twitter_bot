# -*- coding: utf-8 -*-

from icebergsdk.resources.base import IcebergObject, UpdateableIcebergObject

class Store(UpdateableIcebergObject):
    endpoint = 'merchant'
    
    def product_offers(self, params = None, limit = None, offset = 0):
        params = params or {}
        params.update({
            'merchant': self.id,
            'offset': offset
        })
        if limit:
            params['limit'] = limit
        return self.get_list('productoffer', args = params)

    def inbox(self):
        return self.get_list("%sinbox/" % self.resource_uri)

    def import_products(self, feed_url = None):
        """
        Return product from XML file
        Use for initial import
        """
        feed_url = feed_url or ("%sdownload_export/" % self.resource_uri)

        from icebergsdk.parser import XMLParser

        parser = XMLParser()

        res = []

        for element in parser.parse_feed(feed_url):
            if type(element) != dict:
                raise Exception("element from export feed invalid: %s" % element)
            res.append(UpdateableIcebergObject.findOrCreate(element))

        return res


class MerchantImage(IcebergObject):
    endpoint = 'merchant_image'

class MerchantAddress(IcebergObject):
    endpoint = 'merchant_address'



# -*- coding: utf-8 -*-

from icebergsdk.resources.base import UpdateableIcebergObject

class OrderItem(UpdateableIcebergObject):
    endpoint = 'order_item'

    def cancel(self):
        data = self.request("%s%s/" % (self.resource_uri, 'cancel'), method = "post")
        return self._load_attributes_from_response(**data)

    def confirm(self):
        data = self.request("%s%s/" % (self.resource_uri, 'confirm'), method = "post")
        return self._load_attributes_from_response(**data)

    def send(self):
        data = self.request("%s%s/" % (self.resource_uri, 'send'), method = "post")
        return self._load_attributes_from_response(**data)



class MerchantOrder(UpdateableIcebergObject):
    endpoint = 'merchant_order'

    def cancel(self):
        data = self.request("%s%s/" % (self.resource_uri, 'cancel'), method = "post")
        return self._load_attributes_from_response(**data)

    def confirm(self):
        data = self.request("%s%s/" % (self.resource_uri, 'confirm'), method = "post")
        return self._load_attributes_from_response(**data)

    def send(self):
        data = self.request("%s%s/" % (self.resource_uri, 'send'), method = "post")
        return self._load_attributes_from_response(**data)


class Order(UpdateableIcebergObject):
    endpoint = 'order'

    def authorizeOrder(self, params = None):
        params = params or {}
        data = self.request("%s%s/" % (self.resource_uri, 'authorizeOrder'), method = "post", post_args = params)
        return self._load_attributes_from_response(**data)

    def updateOrderPayment(self):
        data = self.request("%s%s/" % (self.resource_uri, 'updateOrderPayment'), method = "post")
        return self._load_attributes_from_response(**data)

    def cancel(self):
        raise NotImplementedError()

    # Seller Related
    def confirm(self):
        raise NotImplementedError()





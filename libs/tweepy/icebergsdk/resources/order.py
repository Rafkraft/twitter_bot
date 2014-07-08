# -*- coding: utf-8 -*-

from icebergsdk.resources.base import IcebergObject

class OrderItem(IcebergObject):
    endpoint = 'order_item'

    def cancel(self):
        raise NotImplementedError()
        return self

    def confirm(self):
        raise NotImplementedError()
        return self

    def send(self):
        raise NotImplementedError()
        return self



class MerchantOrder(IcebergObject):
    endpoint = 'merchant_order'

    def cancel(self):
        raise NotImplementedError()
        return self

    def confirm(self):
        raise NotImplementedError()
        return self

    def send(self):
        raise NotImplementedError()
        return self


class Order(IcebergObject):
    endpoint = 'order'

    def authorizeOrder(self, params = {}):
        data = self.request("%s%s/" % (self.resource_uri, 'authorizeOrder'), method = "post", post_args = params)
        return self._load_attributes_from_response(**data)

    def updateOrderPayment(self):
        data = self.request("%s%s/" % (self.resource_uri, 'updateOrderPayment'), method = "post")
        return self._load_attributes_from_response(**data)

    def cancel(self):
        raise NotImplementedError()
        return self

    # Seller Related
    def confirm(self):
        raise NotImplementedError()
        return self





# -*- coding: utf-8 -*-

from icebergsdk.resources.base import IcebergObject

class Message(IcebergObject):
    endpoint = 'message'

    def read(self):
        """
        Mark message as read
        """
        data = self.request("%s%s/" % (self.resource_uri, 'read'), method = "post")
        return self._load_attributes_from_response(**data)


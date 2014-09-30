# -*- coding: utf-8 -*-

from icebergsdk.resources.base import UpdateableIcebergObject

class Application(UpdateableIcebergObject):
    endpoint = 'application'

    def inbox(self):
        return self.get_list("%sinbox/" % self.resource_uri)

    def fetch_secret_key(self):
    	return self.request("%sfetchSecretKey/" % self.resource_uri)["secret_key"]

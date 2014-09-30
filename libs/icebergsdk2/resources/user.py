# -*- coding: utf-8 -*-

from icebergsdk.resources.base import IcebergObject, UpdateableIcebergObject

from icebergsdk.exceptions import IcebergNoHandlerError

class User(IcebergObject):
    endpoint = 'user'

    @classmethod
    def me(cls):
        if not cls.handler:
            raise IcebergNoHandlerError()

        data = cls.handler.request("%s/me/" % (cls.endpoint))
        return cls.findOrCreate(data)

    def addresses(self):
        return self.get_list('address', args = {'user': self.id})


    def profile(self):
        data = self.request('%sprofile/' % self.resource_uri) 
        return Profile.findOrCreate(data)

class Profile(UpdateableIcebergObject):
    endpoint = 'profile'




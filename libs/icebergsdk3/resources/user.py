# -*- coding: utf-8 -*-

from icebergsdk.resources.base import IcebergObject, UpdateableIcebergObject
from icebergsdk.exceptions import IcebergNoHandlerError

class User(IcebergObject):
    endpoint = 'user'

    @classmethod
    def me(cls):
        if not cls._handler:
            raise IcebergNoHandlerError()

        data = cls._handler.request("%s/me/" % (cls.endpoint))
        return cls.findOrCreate(data)

    def addresses(self):
        return self.get_list('address', args = {'user': self.id})

    def applications(self):
        return self.get_list('application', args = {'contact_user': self.id})

    def reviews(self):
        return self.get_list('review', args = {'user': self.id})

    def profile(self):
        data = self.request('%sprofile/' % self.resource_uri) 
        return Profile.findOrCreate(data)

    def inbox(self):
        return self.get_list("%sinbox/" % self.resource_uri)


class Profile(UpdateableIcebergObject):
    endpoint = 'profile'


class UserShoppingPreference(UpdateableIcebergObject):
    endpoint = 'user_shopping_prefs'



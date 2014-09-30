# -*- coding: utf-8 -*-

from icebergsdk.resources.base import IcebergObject, UpdateableIcebergObject


class Country(IcebergObject):
    endpoint = 'country'


class Address(UpdateableIcebergObject):
    endpoint = 'address'

    

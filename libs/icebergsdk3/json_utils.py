# -*- coding: utf-8 -*-

import json

from datetime import datetime, timedelta
from decimal import Decimal

class DateTimeAwareJSONEncoder(json.JSONEncoder):
    """ 
    Converts a python object, where datetime and timedelta objects are converted
    into objects that can be decoded using the DateTimeAwareJSONDecoder.
    """
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        elif isinstance(obj, Decimal):
            return obj.to_eng_string(),
        else:
            return json.JSONEncoder.default(self, obj)

class DateTimeAwareJSONDecoder(json.JSONDecoder):
    """ 
    Converts a json string, where datetime and timedelta objects were converted
    into objects using the DateTimeAwareJSONEncoder, back into a python object.
    """
    def __init__(self,*args,**kargs):
        json.JSONDecoder.__init__(self, object_hook=self.dict_to_object,*args,**kargs)

    def dict_to_object(self, d): 
        if '__type__' not in d:
            return d

        type = d.pop('__type__')
        if type == 'datetime':
            return datetime(**d)
        elif type == 'timedelta':
            return timedelta(**d)
        elif type == 'Decimal':
            return Decimal(d["value"])
        else:
            # Oops... better put this back together.
            d['__type__'] = type
            return d



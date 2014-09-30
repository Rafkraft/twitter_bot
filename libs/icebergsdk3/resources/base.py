# -*- coding: utf-8 -*-

import warnings, sys, json, logging
import weakref  # Means that if there is no other value, it will be removed

logger = logging.getLogger('icebergsdk.resource')

from icebergsdk.exceptions import IcebergNoHandlerError, IcebergReadOnlyError


"""
Work in progress...
Lot's of stuff to rewrite/remove/add
"""


class IcebergObject(dict):
    __objects_store = {} # Will store the object for relationship management

    def __init__(self, api_key=None, handler = None, **params):
        super(IcebergObject, self).__init__()

        self._unsaved_values = set()
        self._transient_values = set()

        self._retrieve_params = params
        self._previous_metadata = None

        object.__setattr__(self, '_handler', handler)

    def __setattr__(self, k, v):
        if k[0] == '_':
            return super(IcebergObject, self).__setattr__(k, v)

        if k in self.__dict__:
            self._init_unsaved()
            self._unsaved_values.add(k)

            return super(IcebergObject, self).__setattr__(k, v)
        else:
            self._init_unsaved()
            self._unsaved_values.add(k)
            self[k] = v

    def _init_unsaved(self):
        # Allows for unpickling in Python 3.x
        if not hasattr(self, '_unsaved_values'):
            self._unsaved_values = set()

    def __getattr__(self, k):
        if k[0] == '_':
            raise AttributeError(k)

        try:
            return self[k]
        except KeyError as err:
            raise AttributeError(*err.args)

    def __setitem__(self, k, v):
        if v == "":
            raise ValueError(
                "You cannot set %s to an empty string. "
                "We interpret empty strings as None in requests."
                "You may set %s.%s = None to delete the property" % (
                    k, str(self), k))

        super(IcebergObject, self).__setitem__(k, v)

        # Allows for unpickling in Python 3.x
        if not hasattr(self, '_unsaved_values'):
            self._unsaved_values = set()

        self._unsaved_values.add(k)

    def __getitem__(self, k):
        try:
            return super(IcebergObject, self).__getitem__(k)
        except KeyError as err:
            if k in self._transient_values:
                raise KeyError(
                    "%r.  HINT: The %r attribute was set in the past."
                    "It was then wiped when refreshing the object with "
                    "the result returned by Stripe's API, probably as a "
                    "result of a save().  The attributes currently "
                    "available on this object are: %s" %
                    (k, k, ', '.join(self.keys())))
            else:
                raise err

    def __delitem__(self, k):
        raise TypeError(
            "You cannot delete attributes on a IcebergObject. "
            "To unset a property, set it to None.")

    def request(self, *args, **kwargs):
        return self.__class__._handler.request(*args, **kwargs)

    def get_list(self, resource, **kwargs):
        """
        Return a list of Resource Objects
        """
        data = self.__class__._handler.get_list(resource, **kwargs)

        res = []
        for element in data:
            res.append(IcebergObject.findOrCreate(element))

        return res

    def to_JSON(self):
        return json.dumps(self.as_dict())

    def as_dict(self, max_depth=2):
        params = {}
        if max_depth <= 0:
            return {}
        for k in self.__dict__:
            if k.startswith('_'):
                continue

            v = getattr(self, k)

            if isinstance(v, IcebergObject):
                params[k] = v.as_dict(max_depth=max_depth-1)
            elif type(v) == list:
                res = []
                for u in v:
                    if isinstance(u, IcebergObject):
                        res.append(u.as_dict(max_depth=max_depth-1))
                    elif hasattr(u, 'as_dict'):
                        res.append(u.as_dict())
                    else:
                        res.append(u)
                params[k] = res
            else:
                params[k] = v if v is not None else ""
        return params

    def __repr__(self):        
        ident_parts = [type(self).__name__]

        if isinstance(self.get('object'), basestring):
            ident_parts.append(self.get('object'))

        if isinstance(self.get('id'), basestring):
            ident_parts.append('id=%s' % (self.get('id'),))

        unicode_repr = '<%s at %s> JSON: %s' % (
            ' '.join(ident_parts), hex(id(self)), str(self))

        if sys.version_info[0] < 3:
            return unicode_repr.encode('utf-8')
        else:
            return unicode_repr

    def __str__(self):
        return json.dumps(self, sort_keys=True, indent=2)

    @classmethod
    def set_handler(cls, handler):
        cls._handler = handler
        return cls

    def to_dict(self):
        warnings.warn(
            'The `to_dict` method is deprecated and will be removed in '
            'version 2.0 of the Stripe bindings. The StripeObject is '
            'itself now a subclass of `dict`.',
            DeprecationWarning)

        return dict(self)

    def iceberg_id(self):
        return self.id

    def is_new(self):
        return getattr(self, 'id', None) is None

    def has_changed(self):
        return len(self._unsaved_values) > 0

    @classmethod
    def build_resource_uri(cls, options):
        """
        Generate a resource URI from a class

        Should work like:
            build_resource_uri(Product, {id:2}) -> https://api.iceberg.technology/v1/product/2/
        """
        raise NotImplementedError()

    def get_resource_uri(self):
        if self.is_new():
            raise Exception('Missing id for resource %s' % self.endpoint)

        if not hasattr(self, 'resource_uri'):
            self.resource_uri = "/v1/%s/%s/" % (self.endpoint, self.id)
        return self.resource_uri

    def _load_attributes_from_response(self, **response):
        """
        Loads attributes
        If the data has a nested object with a resource_uri, try to math an existing object
        """
        for key, value in response.iteritems():
            if type(value) == list:
                res = []
                for elem in value:
                    if type(elem)==dict and 'resource_uri' in elem: # Try to match a relation
                        try:
                            from icebergsdk.resources import get_class_from_resource_uri
                            obj_cls = get_class_from_resource_uri(elem['resource_uri'])
                            res.append(obj_cls.findOrCreate(elem))
                        except Exception:
                            logger.exception('Cant parse resource')
                    else:
                        res.append(elem)
                        
                self.__dict__[key] = res

            elif type(value) == dict:
                if 'resource_uri' in value: # Try to match a relation
                    try:
                        from icebergsdk.resources import get_class_from_resource_uri
                        obj_cls = get_class_from_resource_uri(value['resource_uri'])
                        self.__dict__[key] = obj_cls.findOrCreate(value)
                    except:
                        pass
                elif 'id' in value: # Fall back
                    self.__dict__[key] = value['id']
            else:
                self.__dict__[key] = value
        return self


    @classmethod
    def findOrCreate(cls, data):
        """
        Take a dict and return an corresponding Iceberg resource object.

        Check in __objects_store for reuse of existing object

        Example:
            data: {
                "id": 1,
                "resource_uri": "/v1/user/1/"
                ...
            }

            Will return an User object
        """

        from icebergsdk.resources import get_class_from_resource_uri

        try:
            obj_cls = get_class_from_resource_uri(data['resource_uri'])
        except:
            obj = cls()
        else:
            data_type = obj_cls.endpoint

            if not data_type in cls.__objects_store: # New type collectore
                cls.__objects_store[data_type] = weakref.WeakValueDictionary()
                obj = obj_cls()
                cls.__objects_store[data_type][str(data['id'])] = obj
            else:
                if str(data['id']) in cls.__objects_store[data_type]:
                    obj = cls.__objects_store[data_type][str(data['id'])]
                else:
                    obj = obj_cls()
                    cls.__objects_store[data_type][str(data['id'])] = obj

        return obj._load_attributes_from_response(**data)

    @classmethod
    def find(cls, object_id):
        if not cls._handler:
            raise IcebergNoHandlerError()

        data = cls._handler.get_element(cls.endpoint, object_id)
        return cls.findOrCreate(data)


    @classmethod
    def search(cls, args = None):
        if not cls._handler:
            raise IcebergNoHandlerError()

        data = cls._handler.request("%s/" % cls.endpoint, args)
        res = []
        for element in data['objects']:
            res.append(cls.findOrCreate(element))

        return res, data["meta"]  # cls.findOrCreate(data)

    @classmethod
    def findWhere(cls, args):
        """
        Like search but return the first result
        """
        return cls.search(args)[0][0]

    @classmethod
    def all(cls):
        """
        Like search but return the first result
        """
        return cls.search()[0]


    def validate_format(self):
        """
        Check the data with the format structure sent by the API
        """
        raise NotImplementedError()


    def fetch(self):
        """
        Resets the model's state from the server
        """
        if not self.__class__._handler:
            raise IcebergNoHandlerError()

        data = self.__class__._handler.request(self.resource_uri)

        return self._load_attributes_from_response(**data)

    def delete(self):
        raise IcebergReadOnlyError()

    def save(self):
        raise IcebergReadOnlyError()
        


class UpdateableIcebergObject(IcebergObject):
    def serialize(self, obj):
        params = {}
        if obj._unsaved_values:
            for k in obj._unsaved_values:
                if k == 'id' or k == '_previous_metadata':
                    continue
                v = getattr(obj, k)

                if isinstance(v, IcebergObject):
                    params[k] = v.get_resource_uri()
                elif type(v) == list:

                    res = []
                    for elem in v:
                        if isinstance(elem, IcebergObject):
                            res.append(elem.get_resource_uri())
                        else:
                            res.append(elem)
                    params[k] = res
                else:
                    params[k] = v if v is not None else ""
        return params

    def save(self):
        if not self.__class__._handler:
            raise IcebergNoHandlerError()

        if self.is_new():
            method = "POST"
            path = "%s/" % self.endpoint
        else:
            method = "PUT"
            path = self.resource_uri

        res = self.__class__._handler.request(path, post_args = self.serialize(self), method = method)
        self._load_attributes_from_response(**res)

        # Clean
        self._unsaved_values = set()

        return self

    def delete(self, handler = None):
        if not handler:
            if not self.__class__._handler:
                raise IcebergNoHandlerError()

            handler = self.__class__._handler
                
        handler.request(self.resource_uri, post_args = {}, method = "DELETE")
        # Clean
        self.__dict__ = {}
        self._unsaved_values = set()



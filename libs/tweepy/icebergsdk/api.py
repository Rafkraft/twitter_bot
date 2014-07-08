# -*- coding: utf-8 -*-

import logging, requests, json, time, hashlib, hmac

from icebergsdk.exceptions import IcebergAPIError, IcebergServerError, IcebergClientError, IcebergMissingApplicationSettingsError
from icebergsdk.conf import Configuration
from icebergsdk import resources
from icebergsdk.json_utils import DateTimeAwareJSONEncoder

logger = logging.getLogger('icebergsdk')

class IcebergAPI(object):
    def __init__(self, username = None, access_token = None, lang = None, timeout = None, conf = None):
        # Conf
        self.conf = conf or Configuration
        self.username = username
        self.access_token = access_token
        self.timeout = timeout
        self.lang = lang or self.conf.ICEBERG_DEFAULT_LANG

        # Resources definition
        self.ProductVariation = resources.ProductVariation.set_handler(self)
        self.ProductOffer = resources.ProductOffer.set_handler(self)
        self.Product = resources.Product.set_handler(self)
        self.Order = resources.Order.set_handler(self)
        self.Application = resources.Application.set_handler(self)
        self.Store = resources.Store.set_handler(self)
        self.User = resources.User.set_handler(self)
        self.Profile = resources.Profile.set_handler(self)
        self.Cart = resources.Cart.set_handler(self)
        self.Country = resources.Country.set_handler(self)
        self.Address = resources.Address.set_handler(self)
        self.Payment = resources.Payment.set_handler(self)

        # Missing
        # Return
        # Reviews
        # Message
        # Invoices
        # Currencies


    def get_auth_token(self):
        return '%s %s:%s' % (self.conf.ICEBERG_AUTH_HEADER, self.username, self.access_token)

    def auth_user(self, username, email, first_name = '', last_name = '', is_staff = False, is_superuser = False):
        """
        Method for Iceberg Staff to get or create a user into the platform and get the access_token
        """
        timestamp = int(time.time())
        secret_key = self.conf.ICEBERG_API_PRIVATE_KEY

        to_compose = [username, email, first_name, last_name, is_staff, is_superuser, timestamp]
        hash_obj = hmac.new(secret_key, ";".join(str(x) for x in to_compose), digestmod = hashlib.sha1)
        message_auth = hash_obj.hexdigest()

        data = {
            'username': username,
            'email': email,
            'first_name': first_name,
            'last_name': last_name,
            'is_staff': is_staff,
            'is_superuser': is_superuser,
            'timestamp': timestamp,
            'message_auth': message_auth
        }

        self.access_token = self.request('user/auth/', args = data)['access_token']

        return self

    def sso(self, email, first_name, last_name):
        if not self.conf.ICEBERG_APPLICATION_NAMESPACE or not self.conf.ICEBERG_APPLICATION_SECRET_KEY:
            raise IcebergMissingApplicationSettingsError()

        timestamp = int(time.time())
        secret_key = self.conf.ICEBERG_APPLICATION_SECRET_KEY

        to_compose = [email, first_name, last_name, timestamp]
        hash_obj = hmac.new(secret_key, ";".join(str(x) for x in to_compose), digestmod = hashlib.sha1)
        message_auth = hash_obj.hexdigest()

        data = {
            'application': self.conf.ICEBERG_APPLICATION_NAMESPACE,
            'email': email,
            'first_name': first_name,
            'last_name': last_name,
            'timestamp': timestamp,
            'message_auth': message_auth
        }

        response = self.request('user/sso/', args = data)

        self.username = response['username']
        self.access_token = response['access_token']

        return response


    def request(self, path, args = None, post_args = None, files = None, method = None):
        args = args or {}
        method = method or "GET"

        headers = {
            'Content-Type': 'application/json',
            'Accept-Language': self.lang,
            'Authorization': self.get_auth_token()
        }
        # store = requests.get('http://api.local.iceberg-marketplace.com:8000/v1/merchant/', params = {'slug': store_slug}, headers = headers)

        if '//' not in path:
            url = "%s:%s/%s/" % (self.conf.ICEBERG_API_URL, self.conf.ICEBERG_API_PORT, self.conf.ICEBERG_API_VERSION)
        else:
            url = ""

        url += path

        logger.debug('REQUEST %s - %s - %s - GET PARAMS: %s - POST PARAMS: %s', method, url, headers, args, post_args)
        try:
            if post_args:
                post_args = json.dumps(post_args, cls=DateTimeAwareJSONEncoder, ensure_ascii=False)
            print post_args
            response = requests.request(method,
                                        url,
                                        timeout=self.timeout,
                                        params=args,
                                        data=post_args,
                                        files=files,
                                        headers=headers)
        except requests.HTTPError as e:
            response = json.loads(e.read())
            raise IcebergAPIError(response)

        logger.debug('RESPONSE - Status: %s - Response Time (s): %s - %s', response.status_code, response.elapsed.total_seconds(), response.text)

        if 400 <= response.status_code < 500:
            raise IcebergClientError(response)

        if 500 <= response.status_code <= 600:
            raise IcebergServerError(response)

        return response.json()

    def get_element(self, resource, object_id):
        return self.request("%s/%s/" % (resource, object_id))

    def get_list(self, resource, **kwargs):
        result = self.request("%s/" % resource, **kwargs)
        return result['objects']

    # User
    def get_me(self):
        return self.request("user/me/")

    def convert_to_register_user(self):
        raise NotImplementedError()

    # Cart
    def get_my_cart(self):
        return self.request("cart/mine/")


    # Merchants
    def get_my_merchants(self):
        return self.get_list('merchant')

    def get_merchant(self, object_id):
        return self.get_element('merchant', object_id)

    # Applications
    def get_my_applications(self):
        return self.get_list('application')

    def get_application(self, object_id):
        return self.get_element('application', object_id)




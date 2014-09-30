# -*- coding: utf-8 -*-

import os

class ConfigurationBase(object):
    ICEBERG_API_VERSION = "v1"
    ICEBERG_AUTH_HEADER = "IcebergAccessToken"
    ICEBERG_DEFAULT_LANG = "en"


class Configuration(ConfigurationBase):
    """
    Main Configuration. Use for Production
    """
    ICEBERG_API_URL = "https://api.iceberg.technology"
    ICEBERG_API_PORT = 443
    ICEBERG_CORS = "https://api.iceberg.technology:%s/cors/" % (ICEBERG_API_PORT)
    ICEBERG_API_URL_FULL = "%s:%s" % (ICEBERG_API_URL, ICEBERG_API_PORT)
    ICEBERG_ENV = "prod"

    # Keys
    ICEBERG_API_PRIVATE_KEY = os.getenv('ICEBERG_API_PRIVATE_KEY', None)
    ICEBERG_APPLICATION_NAMESPACE = os.getenv('ICEBERG_APPLICATION_NAMESPACE', None)
    ICEBERG_APPLICATION_SECRET_KEY = os.getenv('ICEBERG_APPLICATION_SECRET_KEY', None)


class ConfigurationSandbox(ConfigurationBase):
    """
    Sandbox Configuration. Isolated from Production.
    """
    ICEBERG_API_URL = "http://api.sandbox.iceberg.technology"
    ICEBERG_API_PORT = 80
    ICEBERG_CORS = "http://api.sandbox.iceberg.technology/cors/"
    ICEBERG_API_URL_FULL = "%s:%s" % (ICEBERG_API_URL, ICEBERG_API_PORT)
    ICEBERG_ENV = "sandbox"

    # Keys
    ICEBERG_API_PRIVATE_KEY = os.getenv('ICEBERG_API_PRIVATE_KEY_SANDBOX', None)
    ICEBERG_APPLICATION_NAMESPACE = os.getenv('ICEBERG_APPLICATION_NAMESPACE_SANDBOX', None)
    ICEBERG_APPLICATION_SECRET_KEY = os.getenv('ICEBERG_APPLICATION_SECRET_KEY_SANDBOX', None)



class ConfigurationStage(ConfigurationBase):
    """
    PreProd configuration. Share same database as Prod
    """
    ICEBERG_API_URL = "http://api.stage.iceberg.technology"
    ICEBERG_API_PORT = 80
    ICEBERG_CORS = "http://api.stage.iceberg.technology/cors/"
    ICEBERG_API_URL_FULL = "%s:%s" % (ICEBERG_API_URL, ICEBERG_API_PORT)
    ICEBERG_ENV = "stage"

    # Keys
    ICEBERG_API_PRIVATE_KEY = os.getenv('ICEBERG_API_PRIVATE_KEY_STAGE', None)
    ICEBERG_APPLICATION_NAMESPACE = os.getenv('ICEBERG_APPLICATION_NAMESPACE_STAGE', None)
    ICEBERG_APPLICATION_SECRET_KEY = os.getenv('ICEBERG_APPLICATION_SECRET_KEY_STAGE', None)



######
##  Development Configuration. Use for local development.
######
class ConfigurationDebug(ConfigurationBase):
    ICEBERG_API_URL = "http://api.local.iceberg.technology"
    ICEBERG_API_PORT = 8000
    ICEBERG_ENV = "prod"
    ICEBERG_CORS = "http://api.local.iceberg.technology:8000/cors/"
    ICEBERG_API_URL_FULL = "%s:%s" % (ICEBERG_API_URL, ICEBERG_API_PORT)

    ICEBERG_API_PRIVATE_KEY = os.getenv('ICEBERG_API_PRIVATE_KEY_DEBUG', None)
    ICEBERG_APPLICATION_NAMESPACE = os.getenv('ICEBERG_APPLICATION_NAMESPACE_DEBUG', None)
    ICEBERG_APPLICATION_SECRET_KEY = os.getenv('ICEBERG_APPLICATION_SECRET_KEY_DEBUG', None)



class ConfigurationDebugSandbox(ConfigurationBase):
    ICEBERG_API_URL = "http://api.sandbox.local.iceberg.technology"
    ICEBERG_API_PORT = 8000
    ICEBERG_API_URL_FULL = "%s:%s" % (ICEBERG_API_URL, ICEBERG_API_PORT)
    ICEBERG_CORS = "http://api.sandbox.local.iceberg.technology:8000/cors/"
    ICEBERG_ENV = "sandbox"

    ICEBERG_API_PRIVATE_KEY = os.getenv('ICEBERG_API_PRIVATE_KEY_DEBUG_SANDBOX', None)
    ICEBERG_APPLICATION_NAMESPACE = os.getenv('ICEBERG_APPLICATION_NAMESPACE_DEBUG_SANDBOX', None)
    ICEBERG_APPLICATION_SECRET_KEY = os.getenv('ICEBERG_APPLICATION_SECRET_KEY_DEBUG_SANDBOX', None)





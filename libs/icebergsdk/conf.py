# -*- coding: utf-8 -*-

import os

class Configuration:
    ICEBERG_API_URL = "https://api.iceberg.technology"
    ICEBERG_API_PORT = 443
    ICEBERG_API_PRIVATE_KEY = os.getenv('ICEBERG_API_PRIVATE_KEY', None)

    ICEBERG_API_SANDBOX_URL_FULL = "http://api.sandbox.iceberg.technology"

    ICEBERG_CORS = "https://api.iceberg.technology:%s/cors/" % (ICEBERG_API_PORT)
    ICEBERG_SANDBOX_CORS = "%s://api.sandbox.iceberg.technology:%s/cors/" % ("http", 80)

    ICEBERG_API_URL_FULL = "%s:%s" % (ICEBERG_API_URL, ICEBERG_API_PORT)
    ICEBERG_API_VERSION = "v1"
    ICEBERG_AUTH_HEADER = "IcebergAccessToken"
    ICEBERG_DEFAULT_LANG = "en"

    # Application
    ICEBERG_APPLICATION_NAMESPACE = os.getenv('ICEBERG_APPLICATION_NAMESPACE', 'raf_app')
    ICEBERG_APPLICATION_SECRET_KEY = os.getenv('ICEBERG_APPLICATION_SECRET_KEY', '19776da6-3c73-4dcd-aad7-75937d421eff')





# -*- coding: utf-8 -*-


class IcebergError(Exception):
    pass

class IcebergMissingApplicationSettingsError(IcebergError):
    pass

class IcebergNoHandlerError(IcebergError):
    pass

class IcebergConnectionError(IcebergError):
    pass

class IcebergAuthenticationError(IcebergError):
    pass

class IcebergBadRequestError(IcebergError):
    pass

class IcebergTransitionError(IcebergError):
    pass


class IcebergInternalServerError(IcebergError):
    pass

class IcebergRateLimitExceeded(IcebergError):
    pass

class IcebergNotAuthorized(IcebergError):
    pass

class IcebergReadOnlyError(IcebergError):
    pass

# API
class IcebergAPIError(IcebergError):
    def __init__(self, response):
        self.status_code = response.status_code
        self.error_codes = []
        self.message = ''

        try:
            self.data = response.json()
        except:
            self.data = response
        else:
            if 'errors' in self.data:
                for error in self.data['errors']:
                    self.error_codes.append(error['code'])
                    self.message += error['msg']
            if 'error' in self.data:
                self.message += self.data['error']['msg']

        Exception.__init__(self, self.message)
        
    def __str__(self):
        if len(self.message) > 0:
            message = self.message
        else:
            message = self.data
        return "Error! %s : %s: %s" % (self.status_code, self.error_codes, message)

class IcebergServerError(IcebergAPIError):
    pass

class IcebergClientError(IcebergAPIError):
    pass




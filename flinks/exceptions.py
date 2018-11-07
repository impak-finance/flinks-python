"""
    Flinks client exceptions
    ========================

    This module defines top-level exceptions that can be used by the Flinks client implementation.

"""


class FlinksError(Exception):
    """ Base exception for all exceptions that can be raised by the Flinks client. """

    def __init__(self, msg=None):
        self.msg = msg

    def __str__(self):
        return self.msg or super().__str__()


class TransportError(FlinksError):
    """ Raised when an error occurs related to the connection with the Flinks service. """

    def __init__(self, msg, response):
        super().__init__(msg)
        self.response = response


class ProtocolError(FlinksError):
    """ Raised when an error occurs related to the response processing. """

    def __init__(self, msg, response=None, data=None):
        super().__init__(msg)
        self.response = response
        self.data = data

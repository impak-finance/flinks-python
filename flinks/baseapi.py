"""
    Flinks base API abstraction
    ===========================

    This module defines the ``BaseApi`` class allowing to construct various endpoint paths.

"""

from itertools import chain


class BaseApi:
    """ Simple class to buid path for entities. """

    def __init__(self, client):
        """ Initializes the class using a Flinks client. """
        self._client = client
        self.endpoint = ''

    def _build_path(self, *args):
        """ Builds a path using the configured endpoint and path arguments. """
        return '/'.join(chain((self.endpoint, ), map(str, args)))

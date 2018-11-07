"""
    Flinks client
    =============

    This module defines the ``Client`` class allowing to interact with the Flinks API endpoints and
    methods.
    Documentation: https://sandbox.flinks.io/documentation/

"""

from urllib.parse import urljoin

import requests
from requests.adapters import HTTPAdapter
from requests.exceptions import HTTPError

from .exceptions import ProtocolError, TransportError


class Client:
    """ The Flinks API client class. """

    def __init__(self, customer_id, base_url=None, http_max_retries=None):
        """ Initializes the Flinks client.

        :param customer_id: authorization key required to interact with the API endpoints
        :param base_url: base URL of the API endpont (eg. "https://sandbox.flinks.io/v3/")
        :param http_max_retries: maximum number of retries each connection should attempt
        :type customer_id: str
        :type base_url: str
        :type http_max_retries: int
        :return: :class:`Client <Client>` object
        :rtype: flinks.client.Client

        """
        # Initializes attributes related to the client settings.
        self.api_endpoint = urljoin(base_url or 'https://sandbox.flinks.io/v3/', customer_id) + '/'
        self.session = requests.Session()
        self.session.mount(self.api_endpoint, HTTPAdapter(max_retries=http_max_retries or 3))

        # Set up entities attributes.
        self._banking_services = None

        ###################
        # FLINKS ENTITIES #
        ###################

    @property
    def banking_services(self):
        """ Allows to access the banking services entity.

        :return: :class:`BankingServices <BankingServices>` object
        :rtype: flinks.entities.banking_services.BankingServices

        """
        if self._banking_services is None:
            from .entities.banking_services import BankingServices
            self._banking_services = BankingServices(self)
        return self._banking_services

        ##################################
        # PRIVATE METHODS AND PROPERTIES #
        ##################################

    def _call(self, http_method, path, params=None, data=None):
        """ Calls the API endpoint. """
        # Prepares the headers and parameters that will be used to forge the request.
        headers = {'cache-control': 'no-cache', 'Content-Type': 'application/json'}
        params = params or {}

        # Calls the API endpoint!
        request = getattr(self.session, http_method.lower())
        try:
            response = request(
                urljoin(self.api_endpoint, path), headers=headers, params=params, json=data,
            )
            response.raise_for_status()
        except HTTPError:
            if response.status_code != 400:
                raise TransportError(
                    'Got unsuccessful response from server (status code: {})'.format(
                        response.status_code,
                    ),
                    response=response,
                )

        # Ensures the response body can be deserialized to JSON.
        try:
            response_data = response.json()
        except ValueError as e:
            raise ProtocolError(
                'Unable to deserialize response body: {}'.format(e), response=response,
            )

        # Properly handles potential errors.
        if response.status_code > 299 and response_data.get('FlinksCode'):
            raise ProtocolError(
                response_data.get('FlinksCode') or 'FLINKS_ERROR',
                response=response,
                data=response_data,
            )

        return response_data

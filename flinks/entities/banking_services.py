"""
    Flinks banking services entity
    ==============================

    This module defines the ``BankingServices`` entity allowing to interact with the underlying API
    methods.
    Documentation: https://sandbox.flinks.io/documentation/

"""

from ..baseapi import BaseApi


class BankingServices(BaseApi):
    """ Wraps the banking services-related API methods. """

    def __init__(self, client):
        super().__init__(client)
        self.endpoint = 'BankingServices'

    def authorize(
        self, most_recent_cached=False, request_id=None, login_id=None, institution=None,
        username=None, password=None, save=None, security_responses=None, tag=None,
    ):
        """ Exchanges credentials for a LoginId and RequestId.

        :param most_recent_cached:
            indicates whether to get cached data or not for the generated request ID
        :param request_id: generated request ID (if any)
        :param login_id: generated login ID (if applicable)
        :param institution: name of the considered financial institution
        :param username: bank account username
        :param password: bank account password
        :param save: whether or not to save user's credentials on the Flinks side
        :param security_responses: dictionary of security responses and answers
        :param tag: custom value to associate with the generated request ID
        :type most_recent_cached: bool
        :type request_id: str
        :type login_id: str
        :type institution: str
        :type username: str
        :type password: str
        :type save: bool
        :type security_responses: dict
        :type tag: str
        :return: dictionary containing the authorization response
        :rtype: dictionary

        """
        data = {'MostRecentCached': most_recent_cached, }
        if request_id is not None:
            data['RequestId'] = request_id
        if login_id is not None:
            data['LoginId'] = login_id
        if institution is not None:
            data['Institution'] = institution
        if username and password:
            data['Username'] = username
            data['Password'] = password
        if save is not None:
            data['Save'] = save
        if security_responses is not None:
            data['SecurityResponses'] = security_responses
        if tag is not None:
            data['Tag'] = tag
        return self._client._call('POST', self._build_path('Authorize'), data=data)

    def authorize_multiple(self, login_ids=None):
        """ Exchanges multiple credentials for pairs of LoginIds and RequestIds.

        :param login_ids: list of login IDs (list of string)
        :type most_recent_cached: list
        :return: dictionary containing the authorization response
        :rtype: dictionary

        """
        return self._client._call(
            'POST', self._build_path('AuthorizeMultiple'), data={'LoginIds': login_ids or [], },
        )

    def get_accounts_summary(self, request_id):
        """ Retrieves quick details about a specific user.

        :param request_id: valid request ID
        :type request_id: str
        :return: dictionary containing the quick details of the user
        :rtype: dictionary

        """
        return self._client._call(
            'POST', self._build_path('GetAccountsSummary'), data={'RequestId': request_id, },
        )

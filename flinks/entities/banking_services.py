"""
    Flinks banking services entity
    ==============================

    This module defines the ``BankingServices`` entity allowing to interact with the underlying API
    methods.
    Documentation: https://sandbox.flinks.io/documentation/

"""

import datetime as dt

from ..baseapi import BaseApi


class BankingServices(BaseApi):
    """ Wraps the banking services-related API methods. """

    def __init__(self, client):
        super().__init__(client)
        self.endpoint = 'BankingServices'

    def authorize(
        self, most_recent_cached=False, request_id=None, login_id=None, institution=None,
        username=None, password=None, save=None, security_responses=None, schedule_refresh=None,
        tag=None,
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
        :param schedule_refresh: indicates whether to automate refreshes of the user's data
        :param tag: custom value to associate with the generated request ID
        :type most_recent_cached: bool
        :type request_id: str
        :type login_id: str
        :type institution: str
        :type username: str
        :type password: str
        :type save: bool
        :type security_responses: dict
        :type schedule_refresh: bool
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
        if schedule_refresh is not None:
            data['ScheduleRefresh'] = schedule_refresh
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

    def get_accounts_detail(
        self, request_id, with_account_identity=False, with_transactions=False,
        days_of_transactions=None, date_from=None, date_to=None, refresh_delta=None,
        accounts_filter=None,
    ):
        """ Retrieves complete details about a specific user.

        :param request_id: valid request ID
        :param with_account_identity:
            whether to include information about the account in the response
        :param with_transactions: whether to include account transactions in the response
        :param days_of_transactions:
            identifier of the number of days of transactions needed (either 'Days90' or 'Days365')
        :param date_from: start date to use to retrieve transactions
        :param date_to: end date to use to retrieve transactions
        :param refresh_delta:
            list of dictionaries containing an 'AccountId' and 'TransactionId'; they will be used in
            order to return transactions that occured after the specified transactions only
        :param accounts_filter: list of user account IDs to target specificaly
        :type request_id: str
        :type with_account_identity: bool
        :type with_transactions: bool
        :type days_of_transactions: str
        :type date_from: datetime.datetime or datetime.date or str
        :type date_to: datetime.datetime or datetime.date or str
        :type refresh_delta: list
        :type accounts_filter: list
        :return: dictionary containing the complete details of the user
        :rtype: dictionary

        """
        def _prepare_date(date):
            date = date.date() if isinstance(date, dt.datetime) else date
            return date.isoformat() if isinstance(date, dt.date) else date

        data = {
            'RequestId': request_id,
            'WithAccountIdentity': with_account_identity,
            'WithTransactions': with_transactions,
        }
        if days_of_transactions:
            data['DaysOfTransactions'] = days_of_transactions
        if date_from:
            data['DateFrom'] = _prepare_date(date_from)
        if date_to:
            data['DateTo'] = _prepare_date(date_to)
        if refresh_delta:
            data['RefreshDelta'] = refresh_delta
        if accounts_filter:
            data['AccountsFilter'] = accounts_filter
        return self._client._call('POST', self._build_path('GetAccountsDetail'), data=data)

    def get_accounts_detail_async(self, request_id):
        """ Retrieves complete details about a specific user (async mode).

        :param request_id: valid request ID
        :type request_id: str
        :return: dictionary containing the result of the operation
        :rtype: dictionary

        """
        return self._client._call('GET', self._build_path('GetAccountsDetailAsync/' + request_id))

    def delete_card(self, login_id):
        """ Deletes all traces of information about a card on Flinks side.

        :param login_id: valid login ID
        :type login_id: str
        :return: dictionary containing the result of the deletion operation
        :rtype: dictionary

        """
        return self._client._call('DELETE', self._build_path('DeleteCard/' + login_id))

    def get_statements(self, request_id, number_of_statements=None, accounts_filter=None):
        """ Retrieves the Official PDF Bank statements of an account.

        :param request_id: valid request ID
        :param number_of_statements:
            a string identifying the number of statements to retrieve per account (eg. 'MostRecent',
            'Months3', 'Months12')
        :param accounts_filter: list of user account IDs to target specificaly
        :type request_id: str
        :type number_of_statements: str
        :type accounts_filter: list
        :return: dictionary containing the statements
        :rtype: dictionary

        """
        data = {'RequestId': request_id, }
        if number_of_statements:
            data['NumberOfStatements'] = number_of_statements
        if accounts_filter:
            data['AccountsFilter'] = accounts_filter
        return self._client._call('POST', self._build_path('GetStatements'), data=data)

    def get_statements_async(self, request_id):
        """ Retrieves the Official PDF Bank statements of an account (async mode).

        :param request_id: valid request ID
        :type request_id: str
        :return: dictionary containing the result of the operation
        :rtype: dictionary

        """
        return self._client._call('GET', self._build_path('GetStatementsAsync/' + request_id))

    def get_mfa_questions(self, login_id):
        """ Retrieves the user's security questions that could've been stored.

        :param login_id: valid login ID
        :type login_id: str
        :return: dictionary containing the result of the operation and the MFA questions if any
        :rtype: dictionary

        """
        return self._client._call('GET', self._build_path('GetMFAQuestions/' + login_id))

    def set_mfa_questions(self, login_id, questions):
        """ Saves security questions and answers for a specific user.

        :param login_id: valid login ID
        :param questions: list of dictionaries containing a 'Question' key and an 'Answer' key
        :type login_id: str
        :type questions: list
        :return: dictionary containing the result of the operation
        :rtype: dictionary

        """
        data = {'LoginId': login_id, 'Questions': questions, }
        return self._client._call('PATCH', self._build_path('AnswerMFAQuestions'), data=data)

    def set_scheduled_refresh(self, login_id, is_activated=True):
        """ Deactivates or activates automatic refresh of users' data.

        :param login_id: valid login ID
        :param is_activated: boolean indicating whether to activate refreshes or deactivate them
        :type login_id: str
        :type is_activated: bool
        :return: string containing the result of the operation
        :rtype: str

        """
        data = {'LoginId': login_id, 'IsActivated': is_activated, }
        return self._client._call('PATCH', self._build_path('SetScheduledRefresh'), data=data)

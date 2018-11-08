import datetime as dt
import unittest.mock

from flinks import Client


class TestBankingServices:
    @unittest.mock.patch('requests.Session.post')
    def test_can_perform_a_standard_authorize_request(self, mocked_post):
        mocked_response = unittest.mock.Mock(status_code=200, content='{}')
        mocked_response.json.return_value = {
            'RequestId': 'test-1234',
            'LoginId': 'test-5678',
        }
        mocked_post.return_value = mocked_response

        client = Client('foo-12345', 'https://username.flinks-custom.io')
        client.banking_services.authorize(
            institution='Test', username='foo', password='bar', save=True, most_recent_cached=False,
            tag='42',
        )

        assert (
            mocked_post.call_args[0][0] ==
            'https://username.flinks-custom.io/foo-12345/BankingServices/Authorize'
        )
        assert mocked_post.call_args[1]['json'] == {
            'Institution': 'Test',
            'MostRecentCached': False,
            'Password': 'bar',
            'Save': True,
            'Tag': '42',
            'Username': 'foo',
        }

    @unittest.mock.patch('requests.Session.post')
    def test_can_perform_a_standard_authorize_request_with_security_responses(self, mocked_post):
        mocked_response = unittest.mock.Mock(status_code=200, content='{}')
        mocked_response.json.return_value = {
            'RequestId': 'test-1234',
            'LoginId': 'test-5678',
        }
        mocked_post.return_value = mocked_response

        client = Client('foo-12345', 'https://username.flinks-custom.io')
        client.banking_services.authorize(
            request_id='test-1234', username='foo', password='bar',
            security_responses={'Who is the best?': 'ME', },
        )

        assert (
            mocked_post.call_args[0][0] ==
            'https://username.flinks-custom.io/foo-12345/BankingServices/Authorize'
        )
        assert mocked_post.call_args[1]['json'] == {
            'RequestId': 'test-1234',
            'Username': 'foo',
            'Password': 'bar',
            'SecurityResponses': {'Who is the best?': 'ME', },
            'MostRecentCached': False,
        }

    @unittest.mock.patch('requests.Session.post')
    def test_can_perform_an_authorize_request_with_scheduled_refreshes(self, mocked_post):
        mocked_response = unittest.mock.Mock(status_code=200, content='{}')
        mocked_response.json.return_value = {
            'RequestId': 'test-1234',
            'LoginId': 'test-5678',
        }
        mocked_post.return_value = mocked_response

        client = Client('foo-12345', 'https://username.flinks-custom.io')
        client.banking_services.authorize(
            institution='AwesomeBank', username='foobar', password='pwd', save=True,
            schedule_refresh=True,
        )

        assert (
            mocked_post.call_args[0][0] ==
            'https://username.flinks-custom.io/foo-12345/BankingServices/Authorize'
        )
        assert mocked_post.call_args[1]['json'] == {
            'Institution': 'AwesomeBank',
            'Username': 'foobar',
            'Password': 'pwd',
            'Save': True,
            'ScheduleRefresh': True,
            'MostRecentCached': False,
        }

    @unittest.mock.patch('requests.Session.post')
    def test_can_perform_an_authorize_multiple_request(self, mocked_post):
        mocked_response = unittest.mock.Mock(status_code=200, content='{}')
        mocked_response.json.return_value = {
            'ValidLoginIds': [
                {'LoginId': 'login-1234', 'RequestId': 'request-1234'},
            ],
            'InvalidLoginIds': [],
        }
        mocked_post.return_value = mocked_response

        client = Client('foo-12345', 'https://username.flinks-custom.io')
        client.banking_services.authorize_multiple(login_ids=['test-1234', ])

        assert (
            mocked_post.call_args[0][0] ==
            'https://username.flinks-custom.io/foo-12345/BankingServices/AuthorizeMultiple'
        )
        assert mocked_post.call_args[1]['json'] == {
            'LoginIds': ['test-1234', ],
        }

    @unittest.mock.patch('requests.Session.post')
    def test_can_return_accounts_summary_for_a_specific_user(self, mocked_post):
        mocked_response = unittest.mock.Mock(status_code=200, content='{}')
        mocked_response.json.return_value = {'Accounts': [], }
        mocked_post.return_value = mocked_response

        client = Client('foo-12345', 'https://username.flinks-custom.io')
        client.banking_services.get_accounts_summary('request-1234')

        assert (
            mocked_post.call_args[0][0] ==
            'https://username.flinks-custom.io/foo-12345/BankingServices/GetAccountsSummary'
        )
        assert mocked_post.call_args[1]['json'] == {
            'RequestId': 'request-1234',
        }

    @unittest.mock.patch('requests.Session.post')
    def test_can_return_accounts_details_for_a_specific_user(self, mocked_post):
        mocked_response = unittest.mock.Mock(status_code=200, content='{}')
        mocked_response.json.return_value = {'Accounts': [], }
        mocked_post.return_value = mocked_response

        client = Client('foo-12345', 'https://username.flinks-custom.io')
        client.banking_services.get_accounts_detail('request-1234')

        assert (
            mocked_post.call_args[0][0] ==
            'https://username.flinks-custom.io/foo-12345/BankingServices/GetAccountsDetail'
        )
        assert mocked_post.call_args[1]['json'] == {
            'RequestId': 'request-1234',
            'WithAccountIdentity': False,
            'WithTransactions': False,
        }

    @unittest.mock.patch('requests.Session.post')
    def test_can_return_accounts_details_for_a_specific_user_with_account_identity(
        self, mocked_post,
    ):
        mocked_response = unittest.mock.Mock(status_code=200, content='{}')
        mocked_response.json.return_value = {'Accounts': [], }
        mocked_post.return_value = mocked_response

        client = Client('foo-12345', 'https://username.flinks-custom.io')
        client.banking_services.get_accounts_detail('request-1234', with_account_identity=True)

        assert (
            mocked_post.call_args[0][0] ==
            'https://username.flinks-custom.io/foo-12345/BankingServices/GetAccountsDetail'
        )
        assert mocked_post.call_args[1]['json'] == {
            'RequestId': 'request-1234',
            'WithAccountIdentity': True,
            'WithTransactions': False,
        }

    @unittest.mock.patch('requests.Session.post')
    def test_can_return_accounts_details_for_a_specific_user_with_transactions(
        self, mocked_post,
    ):
        mocked_response = unittest.mock.Mock(status_code=200, content='{}')
        mocked_response.json.return_value = {'Accounts': [], }
        mocked_post.return_value = mocked_response

        client = Client('foo-12345', 'https://username.flinks-custom.io')
        client.banking_services.get_accounts_detail('request-1234', with_transactions=True)

        assert (
            mocked_post.call_args[0][0] ==
            'https://username.flinks-custom.io/foo-12345/BankingServices/GetAccountsDetail'
        )
        assert mocked_post.call_args[1]['json'] == {
            'RequestId': 'request-1234',
            'WithAccountIdentity': False,
            'WithTransactions': True,
        }

    @unittest.mock.patch('requests.Session.post')
    def test_can_return_accounts_details_for_a_specific_user_with_specific_days_of_transactions(
        self, mocked_post,
    ):
        mocked_response = unittest.mock.Mock(status_code=200, content='{}')
        mocked_response.json.return_value = {'Accounts': [], }
        mocked_post.return_value = mocked_response

        client = Client('foo-12345', 'https://username.flinks-custom.io')
        client.banking_services.get_accounts_detail(
            'request-1234', with_transactions=True, days_of_transactions='Days365',
        )

        assert (
            mocked_post.call_args[0][0] ==
            'https://username.flinks-custom.io/foo-12345/BankingServices/GetAccountsDetail'
        )
        assert mocked_post.call_args[1]['json'] == {
            'RequestId': 'request-1234',
            'WithAccountIdentity': False,
            'WithTransactions': True,
            'DaysOfTransactions': 'Days365',
        }

    @unittest.mock.patch('requests.Session.post')
    def test_can_return_accounts_details_for_a_specific_user_with_specific_transactions_date_range(
        self, mocked_post,
    ):
        mocked_response = unittest.mock.Mock(status_code=200, content='{}')
        mocked_response.json.return_value = {'Accounts': [], }
        mocked_post.return_value = mocked_response

        client = Client('foo-12345', 'https://username.flinks-custom.io')
        client.banking_services.get_accounts_detail(
            'request-1234', with_transactions=True, date_from=dt.date(2017, 1, 1),
            date_to=dt.datetime.now(),
        )

        assert (
            mocked_post.call_args[0][0] ==
            'https://username.flinks-custom.io/foo-12345/BankingServices/GetAccountsDetail'
        )
        assert mocked_post.call_args[1]['json'] == {
            'RequestId': 'request-1234',
            'WithAccountIdentity': False,
            'WithTransactions': True,
            'DateFrom': '2017-01-01',
            'DateTo': dt.datetime.now().date().isoformat(),
        }

    @unittest.mock.patch('requests.Session.post')
    def test_can_return_accounts_details_for_a_specific_user_with_specific_transactions_refresh_delta(  # noqa
        self, mocked_post,
    ):
        mocked_response = unittest.mock.Mock(status_code=200, content='{}')
        mocked_response.json.return_value = {'Accounts': [], }
        mocked_post.return_value = mocked_response

        client = Client('foo-12345', 'https://username.flinks-custom.io')
        client.banking_services.get_accounts_detail(
            'request-1234',
            with_transactions=True,
            refresh_delta=[
                {'AccountId': 'id-1234', 'TransactionId': 'tx-1234', },
            ],
        )

        assert (
            mocked_post.call_args[0][0] ==
            'https://username.flinks-custom.io/foo-12345/BankingServices/GetAccountsDetail'
        )
        assert mocked_post.call_args[1]['json'] == {
            'RequestId': 'request-1234',
            'WithAccountIdentity': False,
            'WithTransactions': True,
            'RefreshDelta': [
                {'AccountId': 'id-1234', 'TransactionId': 'tx-1234', },
            ],
        }

    @unittest.mock.patch('requests.Session.post')
    def test_can_return_accounts_details_for_a_specific_user_by_filtering_specific_accounts(
        self, mocked_post,
    ):
        mocked_response = unittest.mock.Mock(status_code=200, content='{}')
        mocked_response.json.return_value = {'Accounts': [], }
        mocked_post.return_value = mocked_response

        client = Client('foo-12345', 'https://username.flinks-custom.io')
        client.banking_services.get_accounts_detail(
            'request-1234',
            with_transactions=True,
            accounts_filter=['acc-1234', ],
        )

        assert (
            mocked_post.call_args[0][0] ==
            'https://username.flinks-custom.io/foo-12345/BankingServices/GetAccountsDetail'
        )
        assert mocked_post.call_args[1]['json'] == {
            'RequestId': 'request-1234',
            'WithAccountIdentity': False,
            'WithTransactions': True,
            'AccountsFilter': ['acc-1234', ],
        }

    @unittest.mock.patch('requests.Session.get')
    def test_can_initiate_account_detail_retrieval_in_async_mode(self, mocked_get):
        mocked_response = unittest.mock.Mock(status_code=200, content='{}')
        mocked_response.json.return_value = {'Result': '', }
        mocked_get.return_value = mocked_response

        client = Client('foo-12345', 'https://username.flinks-custom.io')
        client.banking_services.get_accounts_detail_async('request-1234')

        assert (
            mocked_get.call_args[0][0] ==
            (
                'https://username.flinks-custom.io/foo-12345/BankingServices/'
                'GetAccountsDetailAsync/request-1234'
            )
        )

    @unittest.mock.patch('requests.Session.delete')
    def test_can_delete_traces_associated_with_a_specific_login_id(self, mocked_delete):
        mocked_response = unittest.mock.Mock(status_code=200, content='{}')
        mocked_response.json.return_value = {'Result': '', }
        mocked_delete.return_value = mocked_response

        client = Client('foo-12345', 'https://username.flinks-custom.io')
        client.banking_services.delete_card('login-1234')

        assert (
            mocked_delete.call_args[0][0] ==
            'https://username.flinks-custom.io/foo-12345/BankingServices/DeleteCard/login-1234'
        )

    @unittest.mock.patch('requests.Session.post')
    def test_can_retrieve_account_statements(self, mocked_post):
        mocked_response = unittest.mock.Mock(status_code=200, content='{}')
        mocked_response.json.return_value = {'Statements': [], }
        mocked_post.return_value = mocked_response

        client = Client('foo-12345', 'https://username.flinks-custom.io')
        client.banking_services.get_statements('request-1234')

        assert (
            mocked_post.call_args[0][0] ==
            'https://username.flinks-custom.io/foo-12345/BankingServices/GetStatements'
        )
        assert mocked_post.call_args[1]['json'] == {
            'RequestId': 'request-1234',
        }

    @unittest.mock.patch('requests.Session.post')
    def test_can_retrieve_account_statements_with_a_specific_number_of_statements(
        self, mocked_post,
    ):
        mocked_response = unittest.mock.Mock(status_code=200, content='{}')
        mocked_response.json.return_value = {'Statements': [], }
        mocked_post.return_value = mocked_response

        client = Client('foo-12345', 'https://username.flinks-custom.io')
        client.banking_services.get_statements('request-1234', number_of_statements='Months3')

        assert (
            mocked_post.call_args[0][0] ==
            'https://username.flinks-custom.io/foo-12345/BankingServices/GetStatements'
        )
        assert mocked_post.call_args[1]['json'] == {
            'RequestId': 'request-1234',
            'NumberOfStatements': 'Months3',
        }

    @unittest.mock.patch('requests.Session.post')
    def test_can_retrieve_account_statements_with_account_filtering(
        self, mocked_post,
    ):
        mocked_response = unittest.mock.Mock(status_code=200, content='{}')
        mocked_response.json.return_value = {'Statements': [], }
        mocked_post.return_value = mocked_response

        client = Client('foo-12345', 'https://username.flinks-custom.io')
        client.banking_services.get_statements('request-1234', accounts_filter=['acc-1234', ])

        assert (
            mocked_post.call_args[0][0] ==
            'https://username.flinks-custom.io/foo-12345/BankingServices/GetStatements'
        )
        assert mocked_post.call_args[1]['json'] == {
            'RequestId': 'request-1234',
            'AccountsFilter': ['acc-1234', ],
        }

    @unittest.mock.patch('requests.Session.get')
    def test_can_retrieve_account_statements_in_async_mode(self, mocked_get):
        mocked_response = unittest.mock.Mock(status_code=200, content='{}')
        mocked_response.json.return_value = {'Result': '', }
        mocked_get.return_value = mocked_response

        client = Client('foo-12345', 'https://username.flinks-custom.io')
        client.banking_services.get_statements_async('request-1234')

        assert (
            mocked_get.call_args[0][0] ==
            (
                'https://username.flinks-custom.io/foo-12345/BankingServices/'
                'GetStatementsAsync/request-1234'
            )
        )

    @unittest.mock.patch('requests.Session.get')
    def test_can_retrieve_mfa_questions_for_a_specific_user(self, mocked_get):
        mocked_response = unittest.mock.Mock(status_code=200, content='{}')
        mocked_response.json.return_value = {'Questions': [], }
        mocked_get.return_value = mocked_response

        client = Client('foo-12345', 'https://username.flinks-custom.io')
        client.banking_services.get_mfa_questions('login-1234')

        assert (
            mocked_get.call_args[0][0] ==
            (
                'https://username.flinks-custom.io/foo-12345/BankingServices/'
                'GetMFAQuestions/login-1234'
            )
        )

    @unittest.mock.patch('requests.Session.patch')
    def test_can_set_new_security_questions_for_a_specific_user(self, mocked_patch):
        mocked_response = unittest.mock.Mock(status_code=200, content='{}')
        mocked_response.json.return_value = {'Result': '', }
        mocked_patch.return_value = mocked_response

        client = Client('foo-12345', 'https://username.flinks-custom.io')
        client.banking_services.set_mfa_questions(
            'login-1234',
            [{'Question': 'Who is the best?', 'Answer': 'ME', }, ],
        )

        assert (
            mocked_patch.call_args[0][0] ==
            'https://username.flinks-custom.io/foo-12345/BankingServices/AnswerMFAQuestions'
        )
        assert mocked_patch.call_args[1]['json'] == {
            'LoginId': 'login-1234',
            'Questions': [{'Question': 'Who is the best?', 'Answer': 'ME', }, ],
        }

    @unittest.mock.patch('requests.Session.patch')
    def test_can_activate_scheduled_refreshes(self, mocked_patch):
        mocked_response = unittest.mock.Mock(status_code=200, content='{}')
        mocked_response.json.return_value = 'ACTIVATED'
        mocked_patch.return_value = mocked_response

        client = Client('foo-12345', 'https://username.flinks-custom.io')
        client.banking_services.set_scheduled_refresh('login-1234', is_activated=True)

        assert (
            mocked_patch.call_args[0][0] ==
            'https://username.flinks-custom.io/foo-12345/BankingServices/SetScheduledRefresh'
        )
        assert mocked_patch.call_args[1]['json'] == {
            'LoginId': 'login-1234',
            'IsActivated': True,
        }

    @unittest.mock.patch('requests.Session.patch')
    def test_can_deactivate_scheduled_refreshes(self, mocked_patch):
        mocked_response = unittest.mock.Mock(status_code=200, content='{}')
        mocked_response.json.return_value = 'DEACTIVATED'
        mocked_patch.return_value = mocked_response

        client = Client('foo-12345', 'https://username.flinks-custom.io')
        client.banking_services.set_scheduled_refresh('login-1234', is_activated=False)

        assert (
            mocked_patch.call_args[0][0] ==
            'https://username.flinks-custom.io/foo-12345/BankingServices/SetScheduledRefresh'
        )
        assert mocked_patch.call_args[1]['json'] == {
            'LoginId': 'login-1234',
            'IsActivated': False,
        }

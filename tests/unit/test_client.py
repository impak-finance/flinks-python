import unittest.mock

import pytest
from requests.exceptions import HTTPError

from flinks import Client
from flinks.exceptions import ProtocolError, TransportError


class TestClient:
    @unittest.mock.patch('requests.Session.post')
    def test_raises_a_transport_error_if_an_unsuccessful_is_sent_back_from_the_service(
        self, mocked_post,
    ):
        mocked_response = unittest.mock.Mock(status_code=500, content='ERROR')
        mocked_response.raise_for_status.side_effect = HTTPError(response=mocked_response)
        mocked_post.return_value = mocked_response
        client = Client('foo-12345', 'https://username.flinks-custom.io')
        with pytest.raises(TransportError):
            client.banking_services.authorize(login_id='test')

    @unittest.mock.patch('requests.Session.post')
    def test_raises_a_protocol_error_if_a_response_cannot_be_deserialized(self, mocked_post):
        mocked_response = unittest.mock.Mock(status_code=200, content='BAD')
        mocked_response.json.side_effect = ValueError()
        mocked_post.return_value = mocked_response
        client = Client('foo-12345', 'https://username.flinks-custom.io')
        with pytest.raises(ProtocolError):
            client.banking_services.authorize(login_id='test')

    @unittest.mock.patch('requests.Session.post')
    def test_raises_a_protocol_error_if_an_error_is_present_in_the_response(self, mocked_post):
        mocked_response = unittest.mock.Mock(status_code=400, content='{}')
        mocked_response.json.return_value = {'FlinksCode': 'INVALID_LOGING'}
        mocked_post.return_value = mocked_response
        client = Client('foo-12345', 'https://username.flinks-custom.io')
        with pytest.raises(ProtocolError):
            client.banking_services.authorize(login_id='test')

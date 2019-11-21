"""
    Flinks attributes entity
    ==============================

    This module defines the ``Attribute`` entity allowing to get values of special parameters.
    Documentation: https://docs.flinks.io/docs/enrich-your-data

"""

from ..baseapi import BaseApi


class Attribute(BaseApi):
    """ Wraps attributes parameters for calling into Flinks API """

    def __init__(self, client):
        super().__init__(client)
        self.endpoint = 'insight/login'

    def get_attributes(self, login_id, request_id, attributes, filters=None):
        """ Retrieves dict with values of attributes

        :param login_id: valid login ID
        :param request_id: valid request ID, which you can get after success authorization
        :param attributes: dict of attributes broken-down by Attribute level
        :param filters: dict of filters broken-down by categories
        :type login_id: str
        :type request_id:: str
        :type attributes:: dict
        :type filters:: dict
        :return: dictionary containing the values of attributes
        :rtype: dictionary

        """
        data = {"Attributes": attributes}

        if filters is not None:
            data.update({"Filters": filters})

        return self._client._call('POST', self._build_path(
            login_id + '/attributes/' + request_id), data=data)

# coding: utf-8

"""
    AIoD - RAIL

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)

    The version of the OpenAPI document: 1.0.20240507-beta
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from aiod_rail_sdk.models.rail_user_response import RailUserResponse


class TestRailUserResponse(unittest.TestCase):
    """RailUserResponse unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> RailUserResponse:
        """Test RailUserResponse
        include_option is a boolean, when False only required
        params are included, when True both required and
        optional params are included"""
        # uncomment below to create an instance of `RailUserResponse`
        """
        model = RailUserResponse()
        if include_optional:
            return RailUserResponse(
                email = '',
                api_key = ''
            )
        else:
            return RailUserResponse(
                email = '',
        )
        """

    def testRailUserResponse(self):
        """Test RailUserResponse"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == "__main__":
    unittest.main()

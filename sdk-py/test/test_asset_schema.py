# coding: utf-8

"""
    AIoD - RAIL

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)

    The version of the OpenAPI document: 1.0.20240209-beta
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from aiod_rail_sdk.models.asset_schema import AssetSchema


class TestAssetSchema(unittest.TestCase):
    """AssetSchema unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> AssetSchema:
        """Test AssetSchema
        include_option is a boolean, when False only required
        params are included, when True both required and
        optional params are included"""
        # uncomment below to create an instance of `AssetSchema`
        """
        model = AssetSchema()
        if include_optional:
            return AssetSchema(
                cardinality = '0-N'
            )
        else:
            return AssetSchema(
                cardinality = '0-N',
        )
        """

    def testAssetSchema(self):
        """Test AssetSchema"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == "__main__":
    unittest.main()

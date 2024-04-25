# AssetSchema


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**cardinality** | [**AssetCardinality**](AssetCardinality.md) |  | 

## Example

```python
from aiod_rail_sdk.models.asset_schema import AssetSchema

# TODO update the JSON string below
json = "{}"
# create an instance of AssetSchema from a JSON string
asset_schema_instance = AssetSchema.from_json(json)
# print the JSON string representation of the object
print(AssetSchema.to_json())

# convert the object into a dict
asset_schema_dict = asset_schema_instance.to_dict()
# create an instance of AssetSchema from a dict
asset_schema_from_dict = AssetSchema.from_dict(asset_schema_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



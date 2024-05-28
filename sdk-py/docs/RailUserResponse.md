# RailUserResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**email** | **str** |  | 
**api_key** | **str** |  | [optional] [default to '']

## Example

```python
from aiod_rail_sdk.models.rail_user_response import RailUserResponse

# TODO update the JSON string below
json = "{}"
# create an instance of RailUserResponse from a JSON string
rail_user_response_instance = RailUserResponse.from_json(json)
# print the JSON string representation of the object
print(RailUserResponse.to_json())

# convert the object into a dict
rail_user_response_dict = rail_user_response_instance.to_dict()
# create an instance of RailUserResponse from a dict
rail_user_response_from_dict = RailUserResponse.from_dict(rail_user_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



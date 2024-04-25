# Platform


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | The name of the platform, such as huggingface, openml or zenodo. Preferably using snake_case. | 
**identifier** | **int** |  | 

## Example

```python
from aiod_rail_sdk.models.platform import Platform

# TODO update the JSON string below
json = "{}"
# create an instance of Platform from a JSON string
platform_instance = Platform.from_json(json)
# print the JSON string representation of the object
print(Platform.to_json())

# convert the object into a dict
platform_dict = platform_instance.to_dict()
# create an instance of Platform from a dict
platform_from_dict = Platform.from_dict(platform_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



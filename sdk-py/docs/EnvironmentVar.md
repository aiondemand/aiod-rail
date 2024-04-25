# EnvironmentVar


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**key** | **str** |  | 
**value** | **str** |  | 

## Example

```python
from aiod_rail_sdk.models.environment_var import EnvironmentVar

# TODO update the JSON string below
json = "{}"
# create an instance of EnvironmentVar from a JSON string
environment_var_instance = EnvironmentVar.from_json(json)
# print the JSON string representation of the object
print(EnvironmentVar.to_json())

# convert the object into a dict
environment_var_dict = environment_var_instance.to_dict()
# create an instance of EnvironmentVar from a dict
environment_var_from_dict = EnvironmentVar.from_dict(environment_var_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



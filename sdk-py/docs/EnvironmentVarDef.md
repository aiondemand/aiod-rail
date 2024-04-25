# EnvironmentVarDef


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** |  | 
**description** | **str** |  | 

## Example

```python
from aiod_rail_sdk.models.environment_var_def import EnvironmentVarDef

# TODO update the JSON string below
json = "{}"
# create an instance of EnvironmentVarDef from a JSON string
environment_var_def_instance = EnvironmentVarDef.from_json(json)
# print the JSON string representation of the object
print(EnvironmentVarDef.to_json())

# convert the object into a dict
environment_var_def_dict = environment_var_def_instance.to_dict()
# create an instance of EnvironmentVarDef from a dict
environment_var_def_from_dict = EnvironmentVarDef.from_dict(environment_var_def_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



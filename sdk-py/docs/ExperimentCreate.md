# ExperimentCreate


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** |  | 
**description** | **str** |  | 
**is_public** | **bool** |  | 
**experiment_template_id** | **str** |  | 
**dataset_ids** | **List[str]** |  | 
**model_ids** | **List[str]** |  | 
**publication_ids** | **List[str]** |  | [optional] [default to []]
**env_vars** | [**List[EnvironmentVar]**](EnvironmentVar.md) |  | 

## Example

```python
from aiod_rail_sdk.models.experiment_create import ExperimentCreate

# TODO update the JSON string below
json = "{}"
# create an instance of ExperimentCreate from a JSON string
experiment_create_instance = ExperimentCreate.from_json(json)
# print the JSON string representation of the object
print(ExperimentCreate.to_json())

# convert the object into a dict
experiment_create_dict = experiment_create_instance.to_dict()
# create an instance of ExperimentCreate from a dict
experiment_create_from_dict = ExperimentCreate.from_dict(experiment_create_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



# ExperimentRunResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | 
**experiment_id** | **str** |  | 
**created_at** | **datetime** |  | 
**updated_at** | **datetime** |  | 
**retry_count** | **int** |  | 
**state** | [**RunState**](RunState.md) |  | 
**metrics** | **Dict[str, float]** |  | 
**is_public** | **bool** |  | 
**is_archived** | **bool** |  | 
**is_mine** | **bool** |  | 

## Example

```python
from aiod_rail_sdk.models.experiment_run_response import ExperimentRunResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ExperimentRunResponse from a JSON string
experiment_run_response_instance = ExperimentRunResponse.from_json(json)
# print the JSON string representation of the object
print(ExperimentRunResponse.to_json())

# convert the object into a dict
experiment_run_response_dict = experiment_run_response_instance.to_dict()
# create an instance of ExperimentRunResponse from a dict
experiment_run_response_from_dict = ExperimentRunResponse.from_dict(experiment_run_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



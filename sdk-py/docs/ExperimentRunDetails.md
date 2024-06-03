# ExperimentRunDetails


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
**logs** | **str** |  | 

## Example

```python
from aiod_rail_sdk.models.experiment_run_details import ExperimentRunDetails

# TODO update the JSON string below
json = "{}"
# create an instance of ExperimentRunDetails from a JSON string
experiment_run_details_instance = ExperimentRunDetails.from_json(json)
# print the JSON string representation of the object
print(ExperimentRunDetails.to_json())

# convert the object into a dict
experiment_run_details_dict = experiment_run_details_instance.to_dict()
# create an instance of ExperimentRunDetails from a dict
experiment_run_details_from_dict = ExperimentRunDetails.from_dict(experiment_run_details_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



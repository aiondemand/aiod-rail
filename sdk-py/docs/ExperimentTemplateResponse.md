# ExperimentTemplateResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** |  | 
**description** | **str** |  | 
**task** | [**TaskType**](TaskType.md) |  | 
**datasets_schema** | [**AssetSchema**](AssetSchema.md) |  | 
**models_schema** | [**AssetSchema**](AssetSchema.md) |  | 
**envs_required** | [**List[EnvironmentVarDef]**](EnvironmentVarDef.md) |  | 
**envs_optional** | [**List[EnvironmentVarDef]**](EnvironmentVarDef.md) |  | 
**script** | **str** |  | 
**pip_requirements** | **str** |  | 
**is_public** | **bool** |  | 
**id** | **str** |  | 
**created_at** | **datetime** |  | 
**updated_at** | **datetime** |  | 
**state** | [**TemplateState**](TemplateState.md) |  | 
**dockerfile** | **str** |  | 
**is_archived** | **bool** |  | 
**is_approved** | **bool** |  | 
**is_mine** | **bool** |  | 

## Example

```python
from aiod_rail_sdk.models.experiment_template_response import ExperimentTemplateResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ExperimentTemplateResponse from a JSON string
experiment_template_response_instance = ExperimentTemplateResponse.from_json(json)
# print the JSON string representation of the object
print(ExperimentTemplateResponse.to_json())

# convert the object into a dict
experiment_template_response_dict = experiment_template_response_instance.to_dict()
# create an instance of ExperimentTemplateResponse from a dict
experiment_template_response_from_dict = ExperimentTemplateResponse.from_dict(experiment_template_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



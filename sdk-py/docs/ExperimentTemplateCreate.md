# ExperimentTemplateCreate


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
**base_image** | **str** |  | 

## Example

```python
from aiod_rail_sdk.models.experiment_template_create import ExperimentTemplateCreate

# TODO update the JSON string below
json = "{}"
# create an instance of ExperimentTemplateCreate from a JSON string
experiment_template_create_instance = ExperimentTemplateCreate.from_json(json)
# print the JSON string representation of the object
print(ExperimentTemplateCreate.to_json())

# convert the object into a dict
experiment_template_create_dict = experiment_template_create_instance.to_dict()
# create an instance of ExperimentTemplateCreate from a dict
experiment_template_create_from_dict = ExperimentTemplateCreate.from_dict(experiment_template_create_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



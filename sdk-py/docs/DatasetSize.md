# DatasetSize


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**unit** | **str** | Text indicating the unit of measurement. | [optional] 
**value** | **int** | The size. | [optional] 

## Example

```python
from aiod_rail_sdk.models.dataset_size import DatasetSize

# TODO update the JSON string below
json = "{}"
# create an instance of DatasetSize from a JSON string
dataset_size_instance = DatasetSize.from_json(json)
# print the JSON string representation of the object
print(DatasetSize.to_json())

# convert the object into a dict
dataset_size_dict = dataset_size_instance.to_dict()
# create an instance of DatasetSize from a dict
dataset_size_from_dict = DatasetSize.from_dict(dataset_size_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



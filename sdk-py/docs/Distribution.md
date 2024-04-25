# Distribution


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**platform** | **str** | The external platform from which this resource originates. Leave empty if this item originates from AIoD. If platform is not None, the platform_resource_identifier should be set as well. | [optional] 
**platform_resource_identifier** | **str** | A unique identifier issued by the external platform that&#39;s specified in &#39;platform&#39;. Leave empty if this item is not part of an external platform. For example, for HuggingFace, this should be the &lt;namespace&gt;/&lt;dataset_name&gt;, and for Openml, the OpenML identifier. | [optional] 
**checksum** | **str** | The value of a checksum algorithm ran on this content. | [optional] 
**checksum_algorithm** | **str** | The checksum algorithm. | [optional] 
**copyright** | **str** |  | [optional] 
**content_url** | **str** |  | 
**content_size_kb** | **int** |  | [optional] 
**date_published** | **datetime** | The datetime (utc) on which this Distribution was first published on an external platform.  | [optional] 
**description** | **str** |  | [optional] 
**encoding_format** | **str** | The mimetype of this file. | [optional] 
**name** | **str** |  | [optional] 
**technology_readiness_level** | **int** | The technology readiness level (TRL) of the distribution. TRL 1 is the lowest and stands for &#39;Basic principles observed&#39;, TRL 9 is the highest and stands for &#39;actual system proven in operational environment&#39;. | [optional] 

## Example

```python
from aiod_rail_sdk.models.distribution import Distribution

# TODO update the JSON string below
json = "{}"
# create an instance of Distribution from a JSON string
distribution_instance = Distribution.from_json(json)
# print the JSON string representation of the object
print(Distribution.to_json())

# convert the object into a dict
distribution_dict = distribution_instance.to_dict()
# create an instance of Distribution from a dict
distribution_from_dict = Distribution.from_dict(distribution_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



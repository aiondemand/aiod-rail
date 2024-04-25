# Dataset


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**platform** | **str** | The external platform from which this resource originates. Leave empty if this item originates from AIoD. If platform is not None, the platform_resource_identifier should be set as well. | [optional] 
**platform_resource_identifier** | **str** | A unique identifier issued by the external platform that&#39;s specified in &#39;platform&#39;. Leave empty if this item is not part of an external platform. For example, for HuggingFace, this should be the &lt;namespace&gt;/&lt;dataset_name&gt;, and for Openml, the OpenML identifier. | [optional] 
**name** | **str** |  | 
**date_published** | **datetime** | The datetime (utc) on which this resource was first published on an external platform. Note the difference between &#x60;.aiod_entry.date_created&#x60; and &#x60;.date_published&#x60;: the former is automatically set to the datetime the resource was created on AIoD, while the latter can optionally be set to an earlier datetime that the resource was published on an external platform. | [optional] 
**same_as** | **str** | Url of a reference Web page that unambiguously indicates this resource&#39;s identity. | [optional] 
**is_accessible_for_free** | **bool** | A flag to signal that this asset is accessible at no cost. | [optional] 
**version** | **str** | The version of this asset. | [optional] 
**issn** | **str** | The International Standard Serial Number, ISSN, an identifier for serial publications. | [optional] 
**measurement_technique** | **str** | The technique, technology, or methodology used in a dataset, corresponding to the method used for measuring the corresponding variable(s). | [optional] 
**temporal_coverage** | **str** | The temporalCoverage of a CreativeWork indicates the period that the content applies to, i.e. that it describes, a textual string indicating a time period in ISO 8601 time interval format. In the case of a Dataset it will typically indicate the relevant time period in a precise notation (e.g. for a 2011 census dataset, the year 2011 would be written &#39;2011/2012&#39;). | [optional] 
**ai_asset_identifier** | **int** |  | [optional] 
**ai_resource_identifier** | **int** | This resource can be identified by its own identifier, but also by the resource_identifier. | [optional] 
**aiod_entry** | [**AIoDEntryRead**](AIoDEntryRead.md) |  | [optional] 
**alternate_name** | **List[str]** | An alias for the item, commonly used for the resource instead of the name. | [optional] 
**application_area** | **List[str]** | The objective of this AI resource. | [optional] 
**citation** | **List[int]** | A bibliographic reference. | [optional] 
**contact** | **List[int]** | Contact information of persons/organisations that can be contacted about this resource. | [optional] 
**creator** | **List[int]** | Contact information of persons/organisations that created this resource. | [optional] 
**description** | [**Text**](Text.md) |  | [optional] 
**distribution** | [**List[Distribution]**](Distribution.md) |  | [optional] 
**funder** | **List[int]** | Links to identifiers of the agents (person or organization) that supports this dataset through some kind of financial contribution.  | [optional] 
**has_part** | **List[int]** |  | [optional] 
**industrial_sector** | **List[str]** | A business domain where a resource is or can be used. | [optional] 
**is_part_of** | **List[int]** |  | [optional] 
**keyword** | **List[str]** | Keywords or tags used to describe this resource, providing additional context. | [optional] 
**license** | **str** |  | [optional] 
**media** | [**List[Distribution]**](Distribution.md) | Images or videos depicting the resource or associated with it.  | [optional] 
**note** | [**List[Note]**](Note.md) | Notes on this AI resource. | [optional] 
**relevant_link** | **List[str]** | URLs of relevant resources. These resources should not be part of AIoD (use relevant_resource otherwise). This field should only be used if there is no more specific field. | [optional] 
**relevant_resource** | **List[int]** |  | [optional] 
**relevant_to** | **List[int]** |  | [optional] 
**research_area** | **List[str]** | The research area is similar to the scientific_domain, but more high-level. | [optional] 
**scientific_domain** | **List[str]** | The scientific domain is related to the methods with which an objective is reached. | [optional] 
**size** | [**DatasetSize**](DatasetSize.md) | The size of this dataset, for example the number of rows. The file size should not be included here, but in distribution.content_size_kb. | [optional] 
**spatial_coverage** | [**Location**](Location.md) | A location that describes the spatial aspect of this dataset. For example, a point where all the measurements were collected. | [optional] 
**identifier** | **int** |  | 

## Example

```python
from aiod_rail_sdk.models.dataset import Dataset

# TODO update the JSON string below
json = "{}"
# create an instance of Dataset from a JSON string
dataset_instance = Dataset.from_json(json)
# print the JSON string representation of the object
print(Dataset.to_json())

# convert the object into a dict
dataset_dict = dataset_instance.to_dict()
# create an instance of Dataset from a dict
dataset_from_dict = Dataset.from_dict(dataset_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



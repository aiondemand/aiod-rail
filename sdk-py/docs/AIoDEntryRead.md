# AIoDEntryRead


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**editor** | **List[int]** | Links to identifiers of persons responsible for maintaining the entry. | [optional] 
**status** | **str** | Status of the entry (published, draft, rejected) | [optional] [default to 'draft']
**date_modified** | **datetime** | The datetime on which the metadata was last updated in the AIoD platform,in UTC.  Note the difference between &#x60;.aiod_entry.date_created&#x60; and &#x60;.date_published&#x60;: the former is automatically set to the datetime the resource was created on AIoD, while the latter can optionally be set to an earlier datetime that the resource was published on an external platform. | [optional] 
**date_created** | **datetime** | The datetime on which the metadata was first published on the AIoD platform, in UTC. | [optional] 

## Example

```python
from aiod_rail_sdk.models.aio_d_entry_read import AIoDEntryRead

# TODO update the JSON string below
json = "{}"
# create an instance of AIoDEntryRead from a JSON string
aio_d_entry_read_instance = AIoDEntryRead.from_json(json)
# print the JSON string representation of the object
print(AIoDEntryRead.to_json())

# convert the object into a dict
aio_d_entry_read_dict = aio_d_entry_read_instance.to_dict()
# create an instance of AIoDEntryRead from a dict
aio_d_entry_read_from_dict = AIoDEntryRead.from_dict(aio_d_entry_read_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



# Address


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**region** | **str** | A subdivision of the country. Not necessary for most countries.  | [optional] 
**locality** | **str** | A city, town or village. | [optional] 
**street** | **str** | The street address. | [optional] 
**postal_code** | **str** | The postal code. | [optional] 
**address** | **str** | Free text, in case the separate parts such as the street, postal code and country cannot be confidently separated. | [optional] 
**country** | **str** | The country as ISO 3166-1 alpha-3 | [optional] 

## Example

```python
from aiod_rail_sdk.models.address import Address

# TODO update the JSON string below
json = "{}"
# create an instance of Address from a JSON string
address_instance = Address.from_json(json)
# print the JSON string representation of the object
print(Address.to_json())

# convert the object into a dict
address_dict = address_instance.to_dict()
# create an instance of Address from a dict
address_from_dict = Address.from_dict(address_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



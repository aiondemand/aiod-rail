# Geo


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**latitude** | **float** | The latitude of a location in degrees (WGS84) | [optional] 
**longitude** | **float** | The longitude of a location in degrees (WGS84) | [optional] 
**elevation_millimeters** | **int** | The elevation in millimeters with tespect to the WGS84 ellipsoid | [optional] 

## Example

```python
from aiod_rail_sdk.models.geo import Geo

# TODO update the JSON string below
json = "{}"
# create an instance of Geo from a JSON string
geo_instance = Geo.from_json(json)
# print the JSON string representation of the object
print(Geo.to_json())

# convert the object into a dict
geo_dict = geo_instance.to_dict()
# create an instance of Geo from a dict
geo_from_dict = Geo.from_dict(geo_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



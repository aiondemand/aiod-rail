# aiod_rail_sdk.UsersApi

All URIs are relative to *http://localhost/api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_or_change_user_api_key_v1_users_api_key_post**](UsersApi.md#create_or_change_user_api_key_v1_users_api_key_post) | **POST** /v1/users/api_key | Create Or Change User Api Key
[**get_user_api_key_v1_users_api_key_get**](UsersApi.md#get_user_api_key_v1_users_api_key_get) | **GET** /v1/users/api_key | Get User Api Key
[**get_user_profile_v1_users_profile_get**](UsersApi.md#get_user_profile_v1_users_profile_get) | **GET** /v1/users/profile | Get User Profile


# **create_or_change_user_api_key_v1_users_api_key_post**
> str create_or_change_user_api_key_v1_users_api_key_post()

Create Or Change User Api Key

### Example

* Api Key Authentication (APIKeyHeader):

```python
import aiod_rail_sdk
from aiod_rail_sdk.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost/api
# See configuration.py for a list of all supported configuration parameters.
configuration = aiod_rail_sdk.Configuration(
    host = "http://localhost/api"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: APIKeyHeader
configuration.api_key['APIKeyHeader'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['APIKeyHeader'] = 'Bearer'

# Enter a context with an instance of the API client
with aiod_rail_sdk.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = aiod_rail_sdk.UsersApi(api_client)

    try:
        # Create Or Change User Api Key
        api_response = api_instance.create_or_change_user_api_key_v1_users_api_key_post()
        print("The response of UsersApi->create_or_change_user_api_key_v1_users_api_key_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling UsersApi->create_or_change_user_api_key_v1_users_api_key_post: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

**str**

### Authorization

[APIKeyHeader](../README.md#APIKeyHeader), [OpenIdConnect](../README.md#OpenIdConnect)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_user_api_key_v1_users_api_key_get**
> str get_user_api_key_v1_users_api_key_get()

Get User Api Key

### Example

* Api Key Authentication (APIKeyHeader):

```python
import aiod_rail_sdk
from aiod_rail_sdk.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost/api
# See configuration.py for a list of all supported configuration parameters.
configuration = aiod_rail_sdk.Configuration(
    host = "http://localhost/api"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: APIKeyHeader
configuration.api_key['APIKeyHeader'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['APIKeyHeader'] = 'Bearer'

# Enter a context with an instance of the API client
with aiod_rail_sdk.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = aiod_rail_sdk.UsersApi(api_client)

    try:
        # Get User Api Key
        api_response = api_instance.get_user_api_key_v1_users_api_key_get()
        print("The response of UsersApi->get_user_api_key_v1_users_api_key_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling UsersApi->get_user_api_key_v1_users_api_key_get: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

**str**

### Authorization

[APIKeyHeader](../README.md#APIKeyHeader), [OpenIdConnect](../README.md#OpenIdConnect)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_user_profile_v1_users_profile_get**
> RailUserResponse get_user_profile_v1_users_profile_get()

Get User Profile

### Example

* Api Key Authentication (APIKeyHeader):

```python
import aiod_rail_sdk
from aiod_rail_sdk.models.rail_user_response import RailUserResponse
from aiod_rail_sdk.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost/api
# See configuration.py for a list of all supported configuration parameters.
configuration = aiod_rail_sdk.Configuration(
    host = "http://localhost/api"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: APIKeyHeader
configuration.api_key['APIKeyHeader'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['APIKeyHeader'] = 'Bearer'

# Enter a context with an instance of the API client
with aiod_rail_sdk.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = aiod_rail_sdk.UsersApi(api_client)

    try:
        # Get User Profile
        api_response = api_instance.get_user_profile_v1_users_profile_get()
        print("The response of UsersApi->get_user_profile_v1_users_profile_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling UsersApi->get_user_profile_v1_users_profile_get: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**RailUserResponse**](RailUserResponse.md)

### Authorization

[APIKeyHeader](../README.md#APIKeyHeader), [OpenIdConnect](../README.md#OpenIdConnect)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


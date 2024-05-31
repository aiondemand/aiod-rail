# aiod_rail_sdk.ExperimentTemplatesApi

All URIs are relative to *http://localhost/api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**archive_experiment_template_v1_experiment_templates_id_archive_patch**](ExperimentTemplatesApi.md#archive_experiment_template_v1_experiment_templates_id_archive_patch) | **PATCH** /v1/experiment-templates/{id}/archive | Archive Experiment Template
[**create_experiment_template_v1_experiment_templates_post**](ExperimentTemplatesApi.md#create_experiment_template_v1_experiment_templates_post) | **POST** /v1/experiment-templates | Create Experiment Template
[**get_experiment_template_v1_experiment_templates_id_get**](ExperimentTemplatesApi.md#get_experiment_template_v1_experiment_templates_id_get) | **GET** /v1/experiment-templates/{id} | Get Experiment Template
[**get_experiment_templates_count_v1_count_experiment_templates_get**](ExperimentTemplatesApi.md#get_experiment_templates_count_v1_count_experiment_templates_get) | **GET** /v1/count/experiment-templates | Get Experiment Templates Count
[**get_experiment_templates_v1_experiment_templates_get**](ExperimentTemplatesApi.md#get_experiment_templates_v1_experiment_templates_get) | **GET** /v1/experiment-templates | Get Experiment Templates
[**get_experiments_of_template_count_v1_count_experiment_templates_id_experiments_get**](ExperimentTemplatesApi.md#get_experiments_of_template_count_v1_count_experiment_templates_id_experiments_get) | **GET** /v1/count/experiment-templates/{id}/experiments | Get Experiments Of Template Count
[**remove_experiment_template_v1_experiment_templates_id_delete**](ExperimentTemplatesApi.md#remove_experiment_template_v1_experiment_templates_id_delete) | **DELETE** /v1/experiment-templates/{id} | Remove Experiment Template
[**update_experiment_template_v1_experiment_templates_id_put**](ExperimentTemplatesApi.md#update_experiment_template_v1_experiment_templates_id_put) | **PUT** /v1/experiment-templates/{id} | Update Experiment Template


# **archive_experiment_template_v1_experiment_templates_id_archive_patch**
> object archive_experiment_template_v1_experiment_templates_id_archive_patch(id, archive=archive)

Archive Experiment Template

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
    api_instance = aiod_rail_sdk.ExperimentTemplatesApi(api_client)
    id = 'id_example' # str | 
    archive = False # bool |  (optional) (default to False)

    try:
        # Archive Experiment Template
        api_response = api_instance.archive_experiment_template_v1_experiment_templates_id_archive_patch(id, archive=archive)
        print("The response of ExperimentTemplatesApi->archive_experiment_template_v1_experiment_templates_id_archive_patch:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ExperimentTemplatesApi->archive_experiment_template_v1_experiment_templates_id_archive_patch: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 
 **archive** | **bool**|  | [optional] [default to False]

### Return type

**object**

### Authorization

[APIKeyHeader](../README.md#APIKeyHeader), [OpenIdConnect](../README.md#OpenIdConnect)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_experiment_template_v1_experiment_templates_post**
> ExperimentTemplateResponse create_experiment_template_v1_experiment_templates_post(experiment_template_create)

Create Experiment Template

### Example

* Api Key Authentication (APIKeyHeader):

```python
import aiod_rail_sdk
from aiod_rail_sdk.models.experiment_template_create import ExperimentTemplateCreate
from aiod_rail_sdk.models.experiment_template_response import ExperimentTemplateResponse
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
    api_instance = aiod_rail_sdk.ExperimentTemplatesApi(api_client)
    experiment_template_create = aiod_rail_sdk.ExperimentTemplateCreate() # ExperimentTemplateCreate | 

    try:
        # Create Experiment Template
        api_response = api_instance.create_experiment_template_v1_experiment_templates_post(experiment_template_create)
        print("The response of ExperimentTemplatesApi->create_experiment_template_v1_experiment_templates_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ExperimentTemplatesApi->create_experiment_template_v1_experiment_templates_post: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **experiment_template_create** | [**ExperimentTemplateCreate**](ExperimentTemplateCreate.md)|  | 

### Return type

[**ExperimentTemplateResponse**](ExperimentTemplateResponse.md)

### Authorization

[APIKeyHeader](../README.md#APIKeyHeader), [OpenIdConnect](../README.md#OpenIdConnect)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_experiment_template_v1_experiment_templates_id_get**
> ExperimentTemplateResponse get_experiment_template_v1_experiment_templates_id_get(id)

Get Experiment Template

### Example

* Api Key Authentication (APIKeyHeader):

```python
import aiod_rail_sdk
from aiod_rail_sdk.models.experiment_template_response import ExperimentTemplateResponse
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
    api_instance = aiod_rail_sdk.ExperimentTemplatesApi(api_client)
    id = 'id_example' # str | 

    try:
        # Get Experiment Template
        api_response = api_instance.get_experiment_template_v1_experiment_templates_id_get(id)
        print("The response of ExperimentTemplatesApi->get_experiment_template_v1_experiment_templates_id_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ExperimentTemplatesApi->get_experiment_template_v1_experiment_templates_id_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 

### Return type

[**ExperimentTemplateResponse**](ExperimentTemplateResponse.md)

### Authorization

[APIKeyHeader](../README.md#APIKeyHeader), [OpenIdConnect](../README.md#OpenIdConnect)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_experiment_templates_count_v1_count_experiment_templates_get**
> int get_experiment_templates_count_v1_count_experiment_templates_get(query=query, mine=mine, archived=archived, public=public, finalized=finalized, approved=approved)

Get Experiment Templates Count

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
    api_instance = aiod_rail_sdk.ExperimentTemplatesApi(api_client)
    query = '' # str |  (optional) (default to '')
    mine = True # bool |  (optional)
    archived = True # bool |  (optional)
    public = True # bool |  (optional)
    finalized = True # bool |  (optional)
    approved = True # bool |  (optional)

    try:
        # Get Experiment Templates Count
        api_response = api_instance.get_experiment_templates_count_v1_count_experiment_templates_get(query=query, mine=mine, archived=archived, public=public, finalized=finalized, approved=approved)
        print("The response of ExperimentTemplatesApi->get_experiment_templates_count_v1_count_experiment_templates_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ExperimentTemplatesApi->get_experiment_templates_count_v1_count_experiment_templates_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **query** | **str**|  | [optional] [default to &#39;&#39;]
 **mine** | **bool**|  | [optional] 
 **archived** | **bool**|  | [optional] 
 **public** | **bool**|  | [optional] 
 **finalized** | **bool**|  | [optional] 
 **approved** | **bool**|  | [optional] 

### Return type

**int**

### Authorization

[APIKeyHeader](../README.md#APIKeyHeader), [OpenIdConnect](../README.md#OpenIdConnect)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_experiment_templates_v1_experiment_templates_get**
> List[ExperimentTemplateResponse] get_experiment_templates_v1_experiment_templates_get(query=query, offset=offset, limit=limit, mine=mine, archived=archived, public=public, finalized=finalized, approved=approved)

Get Experiment Templates

### Example

* Api Key Authentication (APIKeyHeader):

```python
import aiod_rail_sdk
from aiod_rail_sdk.models.experiment_template_response import ExperimentTemplateResponse
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
    api_instance = aiod_rail_sdk.ExperimentTemplatesApi(api_client)
    query = '' # str |  (optional) (default to '')
    offset = 0 # int |  (optional) (default to 0)
    limit = 100 # int |  (optional) (default to 100)
    mine = True # bool |  (optional)
    archived = True # bool |  (optional)
    public = True # bool |  (optional)
    finalized = True # bool |  (optional)
    approved = True # bool |  (optional)

    try:
        # Get Experiment Templates
        api_response = api_instance.get_experiment_templates_v1_experiment_templates_get(query=query, offset=offset, limit=limit, mine=mine, archived=archived, public=public, finalized=finalized, approved=approved)
        print("The response of ExperimentTemplatesApi->get_experiment_templates_v1_experiment_templates_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ExperimentTemplatesApi->get_experiment_templates_v1_experiment_templates_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **query** | **str**|  | [optional] [default to &#39;&#39;]
 **offset** | **int**|  | [optional] [default to 0]
 **limit** | **int**|  | [optional] [default to 100]
 **mine** | **bool**|  | [optional] 
 **archived** | **bool**|  | [optional] 
 **public** | **bool**|  | [optional] 
 **finalized** | **bool**|  | [optional] 
 **approved** | **bool**|  | [optional] 

### Return type

[**List[ExperimentTemplateResponse]**](ExperimentTemplateResponse.md)

### Authorization

[APIKeyHeader](../README.md#APIKeyHeader), [OpenIdConnect](../README.md#OpenIdConnect)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_experiments_of_template_count_v1_count_experiment_templates_id_experiments_get**
> int get_experiments_of_template_count_v1_count_experiment_templates_id_experiments_get(id, only_mine=only_mine)

Get Experiments Of Template Count

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
    api_instance = aiod_rail_sdk.ExperimentTemplatesApi(api_client)
    id = 'id_example' # str | 
    only_mine = False # bool |  (optional) (default to False)

    try:
        # Get Experiments Of Template Count
        api_response = api_instance.get_experiments_of_template_count_v1_count_experiment_templates_id_experiments_get(id, only_mine=only_mine)
        print("The response of ExperimentTemplatesApi->get_experiments_of_template_count_v1_count_experiment_templates_id_experiments_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ExperimentTemplatesApi->get_experiments_of_template_count_v1_count_experiment_templates_id_experiments_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 
 **only_mine** | **bool**|  | [optional] [default to False]

### Return type

**int**

### Authorization

[APIKeyHeader](../README.md#APIKeyHeader), [OpenIdConnect](../README.md#OpenIdConnect)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **remove_experiment_template_v1_experiment_templates_id_delete**
> object remove_experiment_template_v1_experiment_templates_id_delete(id)

Remove Experiment Template

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
    api_instance = aiod_rail_sdk.ExperimentTemplatesApi(api_client)
    id = 'id_example' # str | 

    try:
        # Remove Experiment Template
        api_response = api_instance.remove_experiment_template_v1_experiment_templates_id_delete(id)
        print("The response of ExperimentTemplatesApi->remove_experiment_template_v1_experiment_templates_id_delete:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ExperimentTemplatesApi->remove_experiment_template_v1_experiment_templates_id_delete: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 

### Return type

**object**

### Authorization

[APIKeyHeader](../README.md#APIKeyHeader), [OpenIdConnect](../README.md#OpenIdConnect)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_experiment_template_v1_experiment_templates_id_put**
> ExperimentTemplateResponse update_experiment_template_v1_experiment_templates_id_put(id, experiment_template_create)

Update Experiment Template

### Example

* Api Key Authentication (APIKeyHeader):

```python
import aiod_rail_sdk
from aiod_rail_sdk.models.experiment_template_create import ExperimentTemplateCreate
from aiod_rail_sdk.models.experiment_template_response import ExperimentTemplateResponse
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
    api_instance = aiod_rail_sdk.ExperimentTemplatesApi(api_client)
    id = 'id_example' # str | 
    experiment_template_create = aiod_rail_sdk.ExperimentTemplateCreate() # ExperimentTemplateCreate | 

    try:
        # Update Experiment Template
        api_response = api_instance.update_experiment_template_v1_experiment_templates_id_put(id, experiment_template_create)
        print("The response of ExperimentTemplatesApi->update_experiment_template_v1_experiment_templates_id_put:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ExperimentTemplatesApi->update_experiment_template_v1_experiment_templates_id_put: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 
 **experiment_template_create** | [**ExperimentTemplateCreate**](ExperimentTemplateCreate.md)|  | 

### Return type

[**ExperimentTemplateResponse**](ExperimentTemplateResponse.md)

### Authorization

[APIKeyHeader](../README.md#APIKeyHeader), [OpenIdConnect](../README.md#OpenIdConnect)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


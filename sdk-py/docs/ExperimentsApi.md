# aiod_rail_sdk.ExperimentsApi

All URIs are relative to *http://localhost/api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**archive_experiment_v1_experiments_id_archive_patch**](ExperimentsApi.md#archive_experiment_v1_experiments_id_archive_patch) | **PATCH** /v1/experiments/{id}/archive | Archive Experiment
[**create_experiment_v1_experiments_post**](ExperimentsApi.md#create_experiment_v1_experiments_post) | **POST** /v1/experiments | Create Experiment
[**delete_experiment_v1_experiments_id_delete**](ExperimentsApi.md#delete_experiment_v1_experiments_id_delete) | **DELETE** /v1/experiments/{id} | Delete Experiment
[**execute_experiment_run_v1_experiments_id_execute_get**](ExperimentsApi.md#execute_experiment_run_v1_experiments_id_execute_get) | **GET** /v1/experiments/{id}/execute | Execute Experiment Run
[**get_experiment_runs_of_experiment_count_v1_count_experiments_id_runs_get**](ExperimentsApi.md#get_experiment_runs_of_experiment_count_v1_count_experiments_id_runs_get) | **GET** /v1/count/experiments/{id}/runs | Get Experiment Runs Of Experiment Count
[**get_experiment_runs_of_experiment_v1_experiments_id_runs_get**](ExperimentsApi.md#get_experiment_runs_of_experiment_v1_experiments_id_runs_get) | **GET** /v1/experiments/{id}/runs | Get Experiment Runs Of Experiment
[**get_experiment_v1_experiments_id_get**](ExperimentsApi.md#get_experiment_v1_experiments_id_get) | **GET** /v1/experiments/{id} | Get Experiment
[**get_experiments_count_v1_count_experiments_get**](ExperimentsApi.md#get_experiments_count_v1_count_experiments_get) | **GET** /v1/count/experiments | Get Experiments Count
[**get_experiments_v1_experiments_get**](ExperimentsApi.md#get_experiments_v1_experiments_get) | **GET** /v1/experiments | Get Experiments
[**update_experiment_v1_experiments_id_put**](ExperimentsApi.md#update_experiment_v1_experiments_id_put) | **PUT** /v1/experiments/{id} | Update Experiment


# **archive_experiment_v1_experiments_id_archive_patch**
> object archive_experiment_v1_experiments_id_archive_patch(id, archive=archive)

Archive Experiment

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
    api_instance = aiod_rail_sdk.ExperimentsApi(api_client)
    id = 'id_example' # str | 
    archive = False # bool |  (optional) (default to False)

    try:
        # Archive Experiment
        api_response = api_instance.archive_experiment_v1_experiments_id_archive_patch(id, archive=archive)
        print("The response of ExperimentsApi->archive_experiment_v1_experiments_id_archive_patch:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ExperimentsApi->archive_experiment_v1_experiments_id_archive_patch: %s\n" % e)
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

# **create_experiment_v1_experiments_post**
> ExperimentResponse create_experiment_v1_experiments_post(experiment_create)

Create Experiment

### Example

* Api Key Authentication (APIKeyHeader):

```python
import aiod_rail_sdk
from aiod_rail_sdk.models.experiment_create import ExperimentCreate
from aiod_rail_sdk.models.experiment_response import ExperimentResponse
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
    api_instance = aiod_rail_sdk.ExperimentsApi(api_client)
    experiment_create = aiod_rail_sdk.ExperimentCreate() # ExperimentCreate | 

    try:
        # Create Experiment
        api_response = api_instance.create_experiment_v1_experiments_post(experiment_create)
        print("The response of ExperimentsApi->create_experiment_v1_experiments_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ExperimentsApi->create_experiment_v1_experiments_post: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **experiment_create** | [**ExperimentCreate**](ExperimentCreate.md)|  | 

### Return type

[**ExperimentResponse**](ExperimentResponse.md)

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

# **delete_experiment_v1_experiments_id_delete**
> object delete_experiment_v1_experiments_id_delete(id)

Delete Experiment

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
    api_instance = aiod_rail_sdk.ExperimentsApi(api_client)
    id = 'id_example' # str | 

    try:
        # Delete Experiment
        api_response = api_instance.delete_experiment_v1_experiments_id_delete(id)
        print("The response of ExperimentsApi->delete_experiment_v1_experiments_id_delete:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ExperimentsApi->delete_experiment_v1_experiments_id_delete: %s\n" % e)
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

# **execute_experiment_run_v1_experiments_id_execute_get**
> ExperimentRunResponse execute_experiment_run_v1_experiments_id_execute_get(id)

Execute Experiment Run

### Example

* Api Key Authentication (APIKeyHeader):

```python
import aiod_rail_sdk
from aiod_rail_sdk.models.experiment_run_response import ExperimentRunResponse
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
    api_instance = aiod_rail_sdk.ExperimentsApi(api_client)
    id = 'id_example' # str | 

    try:
        # Execute Experiment Run
        api_response = api_instance.execute_experiment_run_v1_experiments_id_execute_get(id)
        print("The response of ExperimentsApi->execute_experiment_run_v1_experiments_id_execute_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ExperimentsApi->execute_experiment_run_v1_experiments_id_execute_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 

### Return type

[**ExperimentRunResponse**](ExperimentRunResponse.md)

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

# **get_experiment_runs_of_experiment_count_v1_count_experiments_id_runs_get**
> int get_experiment_runs_of_experiment_count_v1_count_experiments_id_runs_get(id)

Get Experiment Runs Of Experiment Count

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
    api_instance = aiod_rail_sdk.ExperimentsApi(api_client)
    id = 'id_example' # str | 

    try:
        # Get Experiment Runs Of Experiment Count
        api_response = api_instance.get_experiment_runs_of_experiment_count_v1_count_experiments_id_runs_get(id)
        print("The response of ExperimentsApi->get_experiment_runs_of_experiment_count_v1_count_experiments_id_runs_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ExperimentsApi->get_experiment_runs_of_experiment_count_v1_count_experiments_id_runs_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 

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

# **get_experiment_runs_of_experiment_v1_experiments_id_runs_get**
> List[ExperimentRunResponse] get_experiment_runs_of_experiment_v1_experiments_id_runs_get(id, offset=offset, limit=limit)

Get Experiment Runs Of Experiment

### Example

* Api Key Authentication (APIKeyHeader):

```python
import aiod_rail_sdk
from aiod_rail_sdk.models.experiment_run_response import ExperimentRunResponse
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
    api_instance = aiod_rail_sdk.ExperimentsApi(api_client)
    id = 'id_example' # str | 
    offset = 0 # int |  (optional) (default to 0)
    limit = 100 # int |  (optional) (default to 100)

    try:
        # Get Experiment Runs Of Experiment
        api_response = api_instance.get_experiment_runs_of_experiment_v1_experiments_id_runs_get(id, offset=offset, limit=limit)
        print("The response of ExperimentsApi->get_experiment_runs_of_experiment_v1_experiments_id_runs_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ExperimentsApi->get_experiment_runs_of_experiment_v1_experiments_id_runs_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 
 **offset** | **int**|  | [optional] [default to 0]
 **limit** | **int**|  | [optional] [default to 100]

### Return type

[**List[ExperimentRunResponse]**](ExperimentRunResponse.md)

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

# **get_experiment_v1_experiments_id_get**
> ExperimentResponse get_experiment_v1_experiments_id_get(id)

Get Experiment

### Example

* Api Key Authentication (APIKeyHeader):

```python
import aiod_rail_sdk
from aiod_rail_sdk.models.experiment_response import ExperimentResponse
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
    api_instance = aiod_rail_sdk.ExperimentsApi(api_client)
    id = 'id_example' # str | 

    try:
        # Get Experiment
        api_response = api_instance.get_experiment_v1_experiments_id_get(id)
        print("The response of ExperimentsApi->get_experiment_v1_experiments_id_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ExperimentsApi->get_experiment_v1_experiments_id_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 

### Return type

[**ExperimentResponse**](ExperimentResponse.md)

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

# **get_experiments_count_v1_count_experiments_get**
> int get_experiments_count_v1_count_experiments_get(query=query, mine=mine, archived=archived, public=public)

Get Experiments Count

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
    api_instance = aiod_rail_sdk.ExperimentsApi(api_client)
    query = '' # str |  (optional) (default to '')
    mine = True # bool |  (optional)
    archived = True # bool |  (optional)
    public = True # bool |  (optional)

    try:
        # Get Experiments Count
        api_response = api_instance.get_experiments_count_v1_count_experiments_get(query=query, mine=mine, archived=archived, public=public)
        print("The response of ExperimentsApi->get_experiments_count_v1_count_experiments_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ExperimentsApi->get_experiments_count_v1_count_experiments_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **query** | **str**|  | [optional] [default to &#39;&#39;]
 **mine** | **bool**|  | [optional] 
 **archived** | **bool**|  | [optional] 
 **public** | **bool**|  | [optional] 

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

# **get_experiments_v1_experiments_get**
> List[ExperimentResponse] get_experiments_v1_experiments_get(query=query, offset=offset, limit=limit, mine=mine, archived=archived, public=public)

Get Experiments

### Example

* Api Key Authentication (APIKeyHeader):

```python
import aiod_rail_sdk
from aiod_rail_sdk.models.experiment_response import ExperimentResponse
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
    api_instance = aiod_rail_sdk.ExperimentsApi(api_client)
    query = '' # str |  (optional) (default to '')
    offset = 0 # int |  (optional) (default to 0)
    limit = 100 # int |  (optional) (default to 100)
    mine = True # bool |  (optional)
    archived = True # bool |  (optional)
    public = True # bool |  (optional)

    try:
        # Get Experiments
        api_response = api_instance.get_experiments_v1_experiments_get(query=query, offset=offset, limit=limit, mine=mine, archived=archived, public=public)
        print("The response of ExperimentsApi->get_experiments_v1_experiments_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ExperimentsApi->get_experiments_v1_experiments_get: %s\n" % e)
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

### Return type

[**List[ExperimentResponse]**](ExperimentResponse.md)

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

# **update_experiment_v1_experiments_id_put**
> ExperimentResponse update_experiment_v1_experiments_id_put(id, experiment_create)

Update Experiment

### Example

* Api Key Authentication (APIKeyHeader):

```python
import aiod_rail_sdk
from aiod_rail_sdk.models.experiment_create import ExperimentCreate
from aiod_rail_sdk.models.experiment_response import ExperimentResponse
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
    api_instance = aiod_rail_sdk.ExperimentsApi(api_client)
    id = 'id_example' # str | 
    experiment_create = aiod_rail_sdk.ExperimentCreate() # ExperimentCreate | 

    try:
        # Update Experiment
        api_response = api_instance.update_experiment_v1_experiments_id_put(id, experiment_create)
        print("The response of ExperimentsApi->update_experiment_v1_experiments_id_put:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ExperimentsApi->update_experiment_v1_experiments_id_put: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 
 **experiment_create** | [**ExperimentCreate**](ExperimentCreate.md)|  | 

### Return type

[**ExperimentResponse**](ExperimentResponse.md)

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


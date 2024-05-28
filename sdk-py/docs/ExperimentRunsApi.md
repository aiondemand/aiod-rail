# aiod_rail_sdk.ExperimentRunsApi

All URIs are relative to *http://localhost/api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**delete_experiment_run_v1_experiment_runs_id_delete**](ExperimentRunsApi.md#delete_experiment_run_v1_experiment_runs_id_delete) | **DELETE** /v1/experiment-runs/{id} | Delete Experiment Run
[**download_file_from_experiment_run_v1_experiment_runs_id_files_download_get**](ExperimentRunsApi.md#download_file_from_experiment_run_v1_experiment_runs_id_files_download_get) | **GET** /v1/experiment-runs/{id}/files/download | Download File From Experiment Run
[**get_experiment_run_logs_v1_experiment_runs_id_logs_get**](ExperimentRunsApi.md#get_experiment_run_logs_v1_experiment_runs_id_logs_get) | **GET** /v1/experiment-runs/{id}/logs | Get Experiment Run Logs
[**get_experiment_run_v1_experiment_runs_id_get**](ExperimentRunsApi.md#get_experiment_run_v1_experiment_runs_id_get) | **GET** /v1/experiment-runs/{id} | Get Experiment Run
[**list_files_of_experiment_run_v1_experiment_runs_id_files_list_get**](ExperimentRunsApi.md#list_files_of_experiment_run_v1_experiment_runs_id_files_list_get) | **GET** /v1/experiment-runs/{id}/files/list | List Files Of Experiment Run


# **delete_experiment_run_v1_experiment_runs_id_delete**
> object delete_experiment_run_v1_experiment_runs_id_delete(id)

Delete Experiment Run

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
    api_instance = aiod_rail_sdk.ExperimentRunsApi(api_client)
    id = 'id_example' # str | 

    try:
        # Delete Experiment Run
        api_response = api_instance.delete_experiment_run_v1_experiment_runs_id_delete(id)
        print("The response of ExperimentRunsApi->delete_experiment_run_v1_experiment_runs_id_delete:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ExperimentRunsApi->delete_experiment_run_v1_experiment_runs_id_delete: %s\n" % e)
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

# **download_file_from_experiment_run_v1_experiment_runs_id_files_download_get**
> download_file_from_experiment_run_v1_experiment_runs_id_files_download_get(id, filepath)

Download File From Experiment Run

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
    api_instance = aiod_rail_sdk.ExperimentRunsApi(api_client)
    id = 'id_example' # str | 
    filepath = 'filepath_example' # str | 

    try:
        # Download File From Experiment Run
        api_instance.download_file_from_experiment_run_v1_experiment_runs_id_files_download_get(id, filepath)
    except Exception as e:
        print("Exception when calling ExperimentRunsApi->download_file_from_experiment_run_v1_experiment_runs_id_files_download_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 
 **filepath** | **str**|  | 

### Return type

void (empty response body)

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

# **get_experiment_run_logs_v1_experiment_runs_id_logs_get**
> str get_experiment_run_logs_v1_experiment_runs_id_logs_get(id)

Get Experiment Run Logs

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
    api_instance = aiod_rail_sdk.ExperimentRunsApi(api_client)
    id = 'id_example' # str | 

    try:
        # Get Experiment Run Logs
        api_response = api_instance.get_experiment_run_logs_v1_experiment_runs_id_logs_get(id)
        print("The response of ExperimentRunsApi->get_experiment_run_logs_v1_experiment_runs_id_logs_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ExperimentRunsApi->get_experiment_run_logs_v1_experiment_runs_id_logs_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 

### Return type

**str**

### Authorization

[APIKeyHeader](../README.md#APIKeyHeader), [OpenIdConnect](../README.md#OpenIdConnect)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_experiment_run_v1_experiment_runs_id_get**
> ExperimentRunDetails get_experiment_run_v1_experiment_runs_id_get(id)

Get Experiment Run

### Example

* Api Key Authentication (APIKeyHeader):

```python
import aiod_rail_sdk
from aiod_rail_sdk.models.experiment_run_details import ExperimentRunDetails
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
    api_instance = aiod_rail_sdk.ExperimentRunsApi(api_client)
    id = 'id_example' # str | 

    try:
        # Get Experiment Run
        api_response = api_instance.get_experiment_run_v1_experiment_runs_id_get(id)
        print("The response of ExperimentRunsApi->get_experiment_run_v1_experiment_runs_id_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ExperimentRunsApi->get_experiment_run_v1_experiment_runs_id_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 

### Return type

[**ExperimentRunDetails**](ExperimentRunDetails.md)

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

# **list_files_of_experiment_run_v1_experiment_runs_id_files_list_get**
> List[FileDetail] list_files_of_experiment_run_v1_experiment_runs_id_files_list_get(id)

List Files Of Experiment Run

### Example

* Api Key Authentication (APIKeyHeader):

```python
import aiod_rail_sdk
from aiod_rail_sdk.models.file_detail import FileDetail
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
    api_instance = aiod_rail_sdk.ExperimentRunsApi(api_client)
    id = 'id_example' # str | 

    try:
        # List Files Of Experiment Run
        api_response = api_instance.list_files_of_experiment_run_v1_experiment_runs_id_files_list_get(id)
        print("The response of ExperimentRunsApi->list_files_of_experiment_run_v1_experiment_runs_id_files_list_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ExperimentRunsApi->list_files_of_experiment_run_v1_experiment_runs_id_files_list_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 

### Return type

[**List[FileDetail]**](FileDetail.md)

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


# aiod_rail_sdk.ExperimentsApi

All URIs are relative to *http://localhost/api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_experiment_v1_experiments_post**](ExperimentsApi.md#create_experiment_v1_experiments_post) | **POST** /v1/experiments | Create Experiment
[**execute_experiment_run_v1_experiments_id_execute_get**](ExperimentsApi.md#execute_experiment_run_v1_experiments_id_execute_get) | **GET** /v1/experiments/{id}/execute | Execute Experiment Run
[**get_all_experiment_runs_v1_experiment_runs_get**](ExperimentsApi.md#get_all_experiment_runs_v1_experiment_runs_get) | **GET** /v1/experiment-runs | Get All Experiment Runs
[**get_experiment_run_logs_v1_experiment_runs_id_logs_get**](ExperimentsApi.md#get_experiment_run_logs_v1_experiment_runs_id_logs_get) | **GET** /v1/experiment-runs/{id}/logs | Get Experiment Run Logs
[**get_experiment_run_v1_experiment_runs_id_get**](ExperimentsApi.md#get_experiment_run_v1_experiment_runs_id_get) | **GET** /v1/experiment-runs/{id} | Get Experiment Run
[**get_experiment_runs_count_v1_count_experiments_id_runs_get**](ExperimentsApi.md#get_experiment_runs_count_v1_count_experiments_id_runs_get) | **GET** /v1/count/experiments/{id}/runs | Get Experiment Runs Count
[**get_experiment_runs_v1_experiments_id_runs_get**](ExperimentsApi.md#get_experiment_runs_v1_experiments_id_runs_get) | **GET** /v1/experiments/{id}/runs | Get Experiment Runs
[**get_experiment_v1_experiments_id_get**](ExperimentsApi.md#get_experiment_v1_experiments_id_get) | **GET** /v1/experiments/{id} | Get Experiment
[**get_experiments_count_v1_count_experiments_get**](ExperimentsApi.md#get_experiments_count_v1_count_experiments_get) | **GET** /v1/count/experiments | Get Experiments Count
[**get_experiments_v1_experiments_get**](ExperimentsApi.md#get_experiments_v1_experiments_get) | **GET** /v1/experiments | Get Experiments


# **create_experiment_v1_experiments_post**
> ExperimentResponse create_experiment_v1_experiments_post(experiment_create)

Create Experiment

### Example


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

[OpenIdConnect](../README.md#OpenIdConnect)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **execute_experiment_run_v1_experiments_id_execute_get**
> ExperimentRunResponse execute_experiment_run_v1_experiments_id_execute_get(id)

Execute Experiment Run

### Example


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

[OpenIdConnect](../README.md#OpenIdConnect)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_all_experiment_runs_v1_experiment_runs_get**
> List[ExperimentRunResponse] get_all_experiment_runs_v1_experiment_runs_get(offset=offset, limit=limit)

Get All Experiment Runs

### Example


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


# Enter a context with an instance of the API client
with aiod_rail_sdk.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = aiod_rail_sdk.ExperimentsApi(api_client)
    offset = 0 # int |  (optional) (default to 0)
    limit = 100 # int |  (optional) (default to 100)

    try:
        # Get All Experiment Runs
        api_response = api_instance.get_all_experiment_runs_v1_experiment_runs_get(offset=offset, limit=limit)
        print("The response of ExperimentsApi->get_all_experiment_runs_v1_experiment_runs_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ExperimentsApi->get_all_experiment_runs_v1_experiment_runs_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **offset** | **int**|  | [optional] [default to 0]
 **limit** | **int**|  | [optional] [default to 100]

### Return type

[**List[ExperimentRunResponse]**](ExperimentRunResponse.md)

### Authorization

No authorization required

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


```python
import aiod_rail_sdk
from aiod_rail_sdk.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost/api
# See configuration.py for a list of all supported configuration parameters.
configuration = aiod_rail_sdk.Configuration(
    host = "http://localhost/api"
)


# Enter a context with an instance of the API client
with aiod_rail_sdk.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = aiod_rail_sdk.ExperimentsApi(api_client)
    id = 'id_example' # str | 

    try:
        # Get Experiment Run Logs
        api_response = api_instance.get_experiment_run_logs_v1_experiment_runs_id_logs_get(id)
        print("The response of ExperimentsApi->get_experiment_run_logs_v1_experiment_runs_id_logs_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ExperimentsApi->get_experiment_run_logs_v1_experiment_runs_id_logs_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 

### Return type

**str**

### Authorization

No authorization required

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


# Enter a context with an instance of the API client
with aiod_rail_sdk.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = aiod_rail_sdk.ExperimentsApi(api_client)
    id = 'id_example' # str | 

    try:
        # Get Experiment Run
        api_response = api_instance.get_experiment_run_v1_experiment_runs_id_get(id)
        print("The response of ExperimentsApi->get_experiment_run_v1_experiment_runs_id_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ExperimentsApi->get_experiment_run_v1_experiment_runs_id_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 

### Return type

[**ExperimentRunDetails**](ExperimentRunDetails.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_experiment_runs_count_v1_count_experiments_id_runs_get**
> int get_experiment_runs_count_v1_count_experiments_id_runs_get(id)

Get Experiment Runs Count

### Example


```python
import aiod_rail_sdk
from aiod_rail_sdk.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost/api
# See configuration.py for a list of all supported configuration parameters.
configuration = aiod_rail_sdk.Configuration(
    host = "http://localhost/api"
)


# Enter a context with an instance of the API client
with aiod_rail_sdk.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = aiod_rail_sdk.ExperimentsApi(api_client)
    id = 'id_example' # str | 

    try:
        # Get Experiment Runs Count
        api_response = api_instance.get_experiment_runs_count_v1_count_experiments_id_runs_get(id)
        print("The response of ExperimentsApi->get_experiment_runs_count_v1_count_experiments_id_runs_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ExperimentsApi->get_experiment_runs_count_v1_count_experiments_id_runs_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 

### Return type

**int**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_experiment_runs_v1_experiments_id_runs_get**
> List[ExperimentRunResponse] get_experiment_runs_v1_experiments_id_runs_get(id, offset=offset, limit=limit)

Get Experiment Runs

### Example


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


# Enter a context with an instance of the API client
with aiod_rail_sdk.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = aiod_rail_sdk.ExperimentsApi(api_client)
    id = 'id_example' # str | 
    offset = 0 # int |  (optional) (default to 0)
    limit = 100 # int |  (optional) (default to 100)

    try:
        # Get Experiment Runs
        api_response = api_instance.get_experiment_runs_v1_experiments_id_runs_get(id, offset=offset, limit=limit)
        print("The response of ExperimentsApi->get_experiment_runs_v1_experiments_id_runs_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ExperimentsApi->get_experiment_runs_v1_experiments_id_runs_get: %s\n" % e)
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

No authorization required

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

No authorization required

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
> int get_experiments_count_v1_count_experiments_get(include_mine=include_mine, query_operator=query_operator)

Get Experiments Count

### Example


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

# Enter a context with an instance of the API client
with aiod_rail_sdk.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = aiod_rail_sdk.ExperimentsApi(api_client)
    include_mine = False # bool |  (optional) (default to False)
    query_operator = aiod_rail_sdk.QueryOperator() # QueryOperator |  (optional)

    try:
        # Get Experiments Count
        api_response = api_instance.get_experiments_count_v1_count_experiments_get(include_mine=include_mine, query_operator=query_operator)
        print("The response of ExperimentsApi->get_experiments_count_v1_count_experiments_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ExperimentsApi->get_experiments_count_v1_count_experiments_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **include_mine** | **bool**|  | [optional] [default to False]
 **query_operator** | [**QueryOperator**](.md)|  | [optional] 

### Return type

**int**

### Authorization

[OpenIdConnect](../README.md#OpenIdConnect)

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
> List[ExperimentResponse] get_experiments_v1_experiments_get(include_mine=include_mine, query_operator=query_operator, offset=offset, limit=limit)

Get Experiments

### Example


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

# Enter a context with an instance of the API client
with aiod_rail_sdk.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = aiod_rail_sdk.ExperimentsApi(api_client)
    include_mine = False # bool |  (optional) (default to False)
    query_operator = aiod_rail_sdk.QueryOperator() # QueryOperator |  (optional)
    offset = 0 # int |  (optional) (default to 0)
    limit = 100 # int |  (optional) (default to 100)

    try:
        # Get Experiments
        api_response = api_instance.get_experiments_v1_experiments_get(include_mine=include_mine, query_operator=query_operator, offset=offset, limit=limit)
        print("The response of ExperimentsApi->get_experiments_v1_experiments_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ExperimentsApi->get_experiments_v1_experiments_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **include_mine** | **bool**|  | [optional] [default to False]
 **query_operator** | [**QueryOperator**](.md)|  | [optional] 
 **offset** | **int**|  | [optional] [default to 0]
 **limit** | **int**|  | [optional] [default to 100]

### Return type

[**List[ExperimentResponse]**](ExperimentResponse.md)

### Authorization

[OpenIdConnect](../README.md#OpenIdConnect)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


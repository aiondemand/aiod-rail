# aiod_rail_sdk.ExperimentTemplatesApi

All URIs are relative to *http://localhost/api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**approve_experiment_template_v1_experiment_templates_id_approve_patch**](ExperimentTemplatesApi.md#approve_experiment_template_v1_experiment_templates_id_approve_patch) | **PATCH** /v1/experiment-templates/{id}/approve | Approve Experiment Template
[**create_experiment_template_v1_experiment_templates_post**](ExperimentTemplatesApi.md#create_experiment_template_v1_experiment_templates_post) | **POST** /v1/experiment-templates | Create Experiment Template
[**get_experiment_template_v1_experiment_templates_id_get**](ExperimentTemplatesApi.md#get_experiment_template_v1_experiment_templates_id_get) | **GET** /v1/experiment-templates/{id} | Get Experiment Template
[**get_experiment_templates_count_v1_count_experiment_templates_get**](ExperimentTemplatesApi.md#get_experiment_templates_count_v1_count_experiment_templates_get) | **GET** /v1/count/experiment-templates | Get Experiment Templates Count
[**get_experiment_templates_v1_experiment_templates_get**](ExperimentTemplatesApi.md#get_experiment_templates_v1_experiment_templates_get) | **GET** /v1/experiment-templates | Get Experiment Templates


# **approve_experiment_template_v1_experiment_templates_id_approve_patch**
> object approve_experiment_template_v1_experiment_templates_id_approve_patch(id, password, approve_value=approve_value)

Approve Experiment Template

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
    api_instance = aiod_rail_sdk.ExperimentTemplatesApi(api_client)
    id = 'id_example' # str | 
    password = 'password_example' # str | 
    approve_value = True # bool |  (optional) (default to True)

    try:
        # Approve Experiment Template
        api_response = api_instance.approve_experiment_template_v1_experiment_templates_id_approve_patch(id, password, approve_value=approve_value)
        print("The response of ExperimentTemplatesApi->approve_experiment_template_v1_experiment_templates_id_approve_patch:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ExperimentTemplatesApi->approve_experiment_template_v1_experiment_templates_id_approve_patch: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 
 **password** | **str**|  | 
 **approve_value** | **bool**|  | [optional] [default to True]

### Return type

**object**

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

# **create_experiment_template_v1_experiment_templates_post**
> ExperimentTemplateResponse create_experiment_template_v1_experiment_templates_post(experiment_template_create)

Create Experiment Template

### Example


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

# **get_experiment_template_v1_experiment_templates_id_get**
> ExperimentTemplateResponse get_experiment_template_v1_experiment_templates_id_get(id)

Get Experiment Template

### Example


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

# **get_experiment_templates_count_v1_count_experiment_templates_get**
> int get_experiment_templates_count_v1_count_experiment_templates_get(include_mine=include_mine, include_approved=include_approved, query_operator=query_operator)

Get Experiment Templates Count

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
    api_instance = aiod_rail_sdk.ExperimentTemplatesApi(api_client)
    include_mine = False # bool |  (optional) (default to False)
    include_approved = False # bool |  (optional) (default to False)
    query_operator = aiod_rail_sdk.QueryOperator() # QueryOperator |  (optional)

    try:
        # Get Experiment Templates Count
        api_response = api_instance.get_experiment_templates_count_v1_count_experiment_templates_get(include_mine=include_mine, include_approved=include_approved, query_operator=query_operator)
        print("The response of ExperimentTemplatesApi->get_experiment_templates_count_v1_count_experiment_templates_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ExperimentTemplatesApi->get_experiment_templates_count_v1_count_experiment_templates_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **include_mine** | **bool**|  | [optional] [default to False]
 **include_approved** | **bool**|  | [optional] [default to False]
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

# **get_experiment_templates_v1_experiment_templates_get**
> List[ExperimentTemplateResponse] get_experiment_templates_v1_experiment_templates_get(include_mine=include_mine, include_approved=include_approved, query_operator=query_operator, offset=offset, limit=limit)

Get Experiment Templates

### Example


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

# Enter a context with an instance of the API client
with aiod_rail_sdk.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = aiod_rail_sdk.ExperimentTemplatesApi(api_client)
    include_mine = False # bool |  (optional) (default to False)
    include_approved = False # bool |  (optional) (default to False)
    query_operator = aiod_rail_sdk.QueryOperator() # QueryOperator |  (optional)
    offset = 0 # int |  (optional) (default to 0)
    limit = 100 # int |  (optional) (default to 100)

    try:
        # Get Experiment Templates
        api_response = api_instance.get_experiment_templates_v1_experiment_templates_get(include_mine=include_mine, include_approved=include_approved, query_operator=query_operator, offset=offset, limit=limit)
        print("The response of ExperimentTemplatesApi->get_experiment_templates_v1_experiment_templates_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ExperimentTemplatesApi->get_experiment_templates_v1_experiment_templates_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **include_mine** | **bool**|  | [optional] [default to False]
 **include_approved** | **bool**|  | [optional] [default to False]
 **query_operator** | [**QueryOperator**](.md)|  | [optional] 
 **offset** | **int**|  | [optional] [default to 0]
 **limit** | **int**|  | [optional] [default to 100]

### Return type

[**List[ExperimentTemplateResponse]**](ExperimentTemplateResponse.md)

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


# aiod_rail_sdk.AssetsApi

All URIs are relative to *http://localhost/api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_dataset_v1_assets_datasets_post**](AssetsApi.md#create_dataset_v1_assets_datasets_post) | **POST** /v1/assets/datasets | Create Dataset
[**dataset_upload_file_to_huggingface_v1_assets_datasets_id_upload_file_to_huggingface_post**](AssetsApi.md#dataset_upload_file_to_huggingface_v1_assets_datasets_id_upload_file_to_huggingface_post) | **POST** /v1/assets/datasets/{id}/upload-file-to-huggingface | Dataset Upload File To Huggingface
[**delete_dataset_v1_assets_datasets_id_delete**](AssetsApi.md#delete_dataset_v1_assets_datasets_id_delete) | **DELETE** /v1/assets/datasets/{id} | Delete Dataset
[**get_dataset_v1_assets_datasets_id_get**](AssetsApi.md#get_dataset_v1_assets_datasets_id_get) | **GET** /v1/assets/datasets/{id} | Get Dataset
[**get_datasets_count_v1_assets_counts_datasets_get**](AssetsApi.md#get_datasets_count_v1_assets_counts_datasets_get) | **GET** /v1/assets/counts/datasets | Get Datasets Count
[**get_datasets_v1_assets_datasets_get**](AssetsApi.md#get_datasets_v1_assets_datasets_get) | **GET** /v1/assets/datasets | Get Datasets
[**get_filtered_datasets_count_v1_assets_counts_datasets_search_query_get**](AssetsApi.md#get_filtered_datasets_count_v1_assets_counts_datasets_search_query_get) | **GET** /v1/assets/counts/datasets/search/{query} | Get Filtered Datasets Count
[**get_filtered_models_count_v1_assets_counts_models_search_query_get**](AssetsApi.md#get_filtered_models_count_v1_assets_counts_models_search_query_get) | **GET** /v1/assets/counts/models/search/{query} | Get Filtered Models Count
[**get_filtered_publications_count_v1_assets_counts_publications_search_query_get**](AssetsApi.md#get_filtered_publications_count_v1_assets_counts_publications_search_query_get) | **GET** /v1/assets/counts/publications/search/{query} | Get Filtered Publications Count
[**get_model_v1_assets_models_id_get**](AssetsApi.md#get_model_v1_assets_models_id_get) | **GET** /v1/assets/models/{id} | Get Model
[**get_models_count_v1_assets_counts_models_get**](AssetsApi.md#get_models_count_v1_assets_counts_models_get) | **GET** /v1/assets/counts/models | Get Models Count
[**get_models_v1_assets_models_get**](AssetsApi.md#get_models_v1_assets_models_get) | **GET** /v1/assets/models | Get Models
[**get_my_datasets_count_v1_assets_counts_datasets_my_get**](AssetsApi.md#get_my_datasets_count_v1_assets_counts_datasets_my_get) | **GET** /v1/assets/counts/datasets/my | Get My Datasets Count
[**get_my_datasets_v1_assets_datasets_my_get**](AssetsApi.md#get_my_datasets_v1_assets_datasets_my_get) | **GET** /v1/assets/datasets/my | Get My Datasets
[**get_my_models_count_v1_assets_counts_models_my_get**](AssetsApi.md#get_my_models_count_v1_assets_counts_models_my_get) | **GET** /v1/assets/counts/models/my | Get My Models Count
[**get_my_models_v1_assets_models_my_get**](AssetsApi.md#get_my_models_v1_assets_models_my_get) | **GET** /v1/assets/models/my | Get My Models
[**get_platforms_v1_assets_platforms_get**](AssetsApi.md#get_platforms_v1_assets_platforms_get) | **GET** /v1/assets/platforms | Get Platforms
[**get_publication_v1_assets_publications_id_get**](AssetsApi.md#get_publication_v1_assets_publications_id_get) | **GET** /v1/assets/publications/{id} | Get Publication
[**get_publications_count_v1_assets_counts_publications_get**](AssetsApi.md#get_publications_count_v1_assets_counts_publications_get) | **GET** /v1/assets/counts/publications | Get Publications Count
[**get_publications_v1_assets_publications_get**](AssetsApi.md#get_publications_v1_assets_publications_get) | **GET** /v1/assets/publications | Get Publications
[**search_datasets_v1_assets_datasets_search_query_get**](AssetsApi.md#search_datasets_v1_assets_datasets_search_query_get) | **GET** /v1/assets/datasets/search/{query} | Search Datasets
[**search_models_v1_assets_models_search_query_get**](AssetsApi.md#search_models_v1_assets_models_search_query_get) | **GET** /v1/assets/models/search/{query} | Search Models
[**search_publications_v1_assets_publications_search_query_get**](AssetsApi.md#search_publications_v1_assets_publications_search_query_get) | **GET** /v1/assets/publications/search/{query} | Search Publications


# **create_dataset_v1_assets_datasets_post**
> Dataset create_dataset_v1_assets_datasets_post(dataset)

Create Dataset

### Example

* Api Key Authentication (APIKeyHeader):

```python
import aiod_rail_sdk
from aiod_rail_sdk.models.dataset import Dataset
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
    api_instance = aiod_rail_sdk.AssetsApi(api_client)
    dataset = aiod_rail_sdk.Dataset() # Dataset | 

    try:
        # Create Dataset
        api_response = api_instance.create_dataset_v1_assets_datasets_post(dataset)
        print("The response of AssetsApi->create_dataset_v1_assets_datasets_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AssetsApi->create_dataset_v1_assets_datasets_post: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **dataset** | [**Dataset**](Dataset.md)|  | 

### Return type

[**Dataset**](Dataset.md)

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

# **dataset_upload_file_to_huggingface_v1_assets_datasets_id_upload_file_to_huggingface_post**
> Dataset dataset_upload_file_to_huggingface_v1_assets_datasets_id_upload_file_to_huggingface_post(id, huggingface_name, huggingface_token, file)

Dataset Upload File To Huggingface

### Example


```python
import aiod_rail_sdk
from aiod_rail_sdk.models.dataset import Dataset
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
    api_instance = aiod_rail_sdk.AssetsApi(api_client)
    id = 56 # int | 
    huggingface_name = 'huggingface_name_example' # str | 
    huggingface_token = 'huggingface_token_example' # str | 
    file = None # bytearray | 

    try:
        # Dataset Upload File To Huggingface
        api_response = api_instance.dataset_upload_file_to_huggingface_v1_assets_datasets_id_upload_file_to_huggingface_post(id, huggingface_name, huggingface_token, file)
        print("The response of AssetsApi->dataset_upload_file_to_huggingface_v1_assets_datasets_id_upload_file_to_huggingface_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AssetsApi->dataset_upload_file_to_huggingface_v1_assets_datasets_id_upload_file_to_huggingface_post: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **int**|  | 
 **huggingface_name** | **str**|  | 
 **huggingface_token** | **str**|  | 
 **file** | **bytearray**|  | 

### Return type

[**Dataset**](Dataset.md)

### Authorization

[OpenIdConnect](../README.md#OpenIdConnect)

### HTTP request headers

 - **Content-Type**: multipart/form-data
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_dataset_v1_assets_datasets_id_delete**
> bool delete_dataset_v1_assets_datasets_id_delete(id)

Delete Dataset

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
    api_instance = aiod_rail_sdk.AssetsApi(api_client)
    id = 56 # int | 

    try:
        # Delete Dataset
        api_response = api_instance.delete_dataset_v1_assets_datasets_id_delete(id)
        print("The response of AssetsApi->delete_dataset_v1_assets_datasets_id_delete:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AssetsApi->delete_dataset_v1_assets_datasets_id_delete: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **int**|  | 

### Return type

**bool**

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

# **get_dataset_v1_assets_datasets_id_get**
> Dataset get_dataset_v1_assets_datasets_id_get(id)

Get Dataset

### Example


```python
import aiod_rail_sdk
from aiod_rail_sdk.models.dataset import Dataset
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
    api_instance = aiod_rail_sdk.AssetsApi(api_client)
    id = 56 # int | 

    try:
        # Get Dataset
        api_response = api_instance.get_dataset_v1_assets_datasets_id_get(id)
        print("The response of AssetsApi->get_dataset_v1_assets_datasets_id_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AssetsApi->get_dataset_v1_assets_datasets_id_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **int**|  | 

### Return type

[**Dataset**](Dataset.md)

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

# **get_datasets_count_v1_assets_counts_datasets_get**
> int get_datasets_count_v1_assets_counts_datasets_get()

Get Datasets Count

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
    api_instance = aiod_rail_sdk.AssetsApi(api_client)

    try:
        # Get Datasets Count
        api_response = api_instance.get_datasets_count_v1_assets_counts_datasets_get()
        print("The response of AssetsApi->get_datasets_count_v1_assets_counts_datasets_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AssetsApi->get_datasets_count_v1_assets_counts_datasets_get: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

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

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_datasets_v1_assets_datasets_get**
> List[Dataset] get_datasets_v1_assets_datasets_get(offset=offset, limit=limit)

Get Datasets

### Example


```python
import aiod_rail_sdk
from aiod_rail_sdk.models.dataset import Dataset
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
    api_instance = aiod_rail_sdk.AssetsApi(api_client)
    offset = 0 # int |  (optional) (default to 0)
    limit = 100 # int |  (optional) (default to 100)

    try:
        # Get Datasets
        api_response = api_instance.get_datasets_v1_assets_datasets_get(offset=offset, limit=limit)
        print("The response of AssetsApi->get_datasets_v1_assets_datasets_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AssetsApi->get_datasets_v1_assets_datasets_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **offset** | **int**|  | [optional] [default to 0]
 **limit** | **int**|  | [optional] [default to 100]

### Return type

[**List[Dataset]**](Dataset.md)

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

# **get_filtered_datasets_count_v1_assets_counts_datasets_search_query_get**
> int get_filtered_datasets_count_v1_assets_counts_datasets_search_query_get(query)

Get Filtered Datasets Count

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
    api_instance = aiod_rail_sdk.AssetsApi(api_client)
    query = 'query_example' # str | 

    try:
        # Get Filtered Datasets Count
        api_response = api_instance.get_filtered_datasets_count_v1_assets_counts_datasets_search_query_get(query)
        print("The response of AssetsApi->get_filtered_datasets_count_v1_assets_counts_datasets_search_query_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AssetsApi->get_filtered_datasets_count_v1_assets_counts_datasets_search_query_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **query** | **str**|  | 

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

# **get_filtered_models_count_v1_assets_counts_models_search_query_get**
> int get_filtered_models_count_v1_assets_counts_models_search_query_get(query)

Get Filtered Models Count

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
    api_instance = aiod_rail_sdk.AssetsApi(api_client)
    query = 'query_example' # str | 

    try:
        # Get Filtered Models Count
        api_response = api_instance.get_filtered_models_count_v1_assets_counts_models_search_query_get(query)
        print("The response of AssetsApi->get_filtered_models_count_v1_assets_counts_models_search_query_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AssetsApi->get_filtered_models_count_v1_assets_counts_models_search_query_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **query** | **str**|  | 

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

# **get_filtered_publications_count_v1_assets_counts_publications_search_query_get**
> int get_filtered_publications_count_v1_assets_counts_publications_search_query_get(query)

Get Filtered Publications Count

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
    api_instance = aiod_rail_sdk.AssetsApi(api_client)
    query = 'query_example' # str | 

    try:
        # Get Filtered Publications Count
        api_response = api_instance.get_filtered_publications_count_v1_assets_counts_publications_search_query_get(query)
        print("The response of AssetsApi->get_filtered_publications_count_v1_assets_counts_publications_search_query_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AssetsApi->get_filtered_publications_count_v1_assets_counts_publications_search_query_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **query** | **str**|  | 

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

# **get_model_v1_assets_models_id_get**
> MLModel get_model_v1_assets_models_id_get(id)

Get Model

### Example


```python
import aiod_rail_sdk
from aiod_rail_sdk.models.ml_model import MLModel
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
    api_instance = aiod_rail_sdk.AssetsApi(api_client)
    id = 56 # int | 

    try:
        # Get Model
        api_response = api_instance.get_model_v1_assets_models_id_get(id)
        print("The response of AssetsApi->get_model_v1_assets_models_id_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AssetsApi->get_model_v1_assets_models_id_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **int**|  | 

### Return type

[**MLModel**](MLModel.md)

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

# **get_models_count_v1_assets_counts_models_get**
> int get_models_count_v1_assets_counts_models_get()

Get Models Count

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
    api_instance = aiod_rail_sdk.AssetsApi(api_client)

    try:
        # Get Models Count
        api_response = api_instance.get_models_count_v1_assets_counts_models_get()
        print("The response of AssetsApi->get_models_count_v1_assets_counts_models_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AssetsApi->get_models_count_v1_assets_counts_models_get: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

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

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_models_v1_assets_models_get**
> List[MLModel] get_models_v1_assets_models_get(offset=offset, limit=limit)

Get Models

### Example


```python
import aiod_rail_sdk
from aiod_rail_sdk.models.ml_model import MLModel
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
    api_instance = aiod_rail_sdk.AssetsApi(api_client)
    offset = 0 # int |  (optional) (default to 0)
    limit = 100 # int |  (optional) (default to 100)

    try:
        # Get Models
        api_response = api_instance.get_models_v1_assets_models_get(offset=offset, limit=limit)
        print("The response of AssetsApi->get_models_v1_assets_models_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AssetsApi->get_models_v1_assets_models_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **offset** | **int**|  | [optional] [default to 0]
 **limit** | **int**|  | [optional] [default to 100]

### Return type

[**List[MLModel]**](MLModel.md)

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

# **get_my_datasets_count_v1_assets_counts_datasets_my_get**
> int get_my_datasets_count_v1_assets_counts_datasets_my_get()

Get My Datasets Count

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
    api_instance = aiod_rail_sdk.AssetsApi(api_client)

    try:
        # Get My Datasets Count
        api_response = api_instance.get_my_datasets_count_v1_assets_counts_datasets_my_get()
        print("The response of AssetsApi->get_my_datasets_count_v1_assets_counts_datasets_my_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AssetsApi->get_my_datasets_count_v1_assets_counts_datasets_my_get: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

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

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_my_datasets_v1_assets_datasets_my_get**
> List[Dataset] get_my_datasets_v1_assets_datasets_my_get(offset=offset, limit=limit)

Get My Datasets

### Example


```python
import aiod_rail_sdk
from aiod_rail_sdk.models.dataset import Dataset
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
    api_instance = aiod_rail_sdk.AssetsApi(api_client)
    offset = 0 # int |  (optional) (default to 0)
    limit = 100 # int |  (optional) (default to 100)

    try:
        # Get My Datasets
        api_response = api_instance.get_my_datasets_v1_assets_datasets_my_get(offset=offset, limit=limit)
        print("The response of AssetsApi->get_my_datasets_v1_assets_datasets_my_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AssetsApi->get_my_datasets_v1_assets_datasets_my_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **offset** | **int**|  | [optional] [default to 0]
 **limit** | **int**|  | [optional] [default to 100]

### Return type

[**List[Dataset]**](Dataset.md)

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

# **get_my_models_count_v1_assets_counts_models_my_get**
> int get_my_models_count_v1_assets_counts_models_my_get()

Get My Models Count

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
    api_instance = aiod_rail_sdk.AssetsApi(api_client)

    try:
        # Get My Models Count
        api_response = api_instance.get_my_models_count_v1_assets_counts_models_my_get()
        print("The response of AssetsApi->get_my_models_count_v1_assets_counts_models_my_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AssetsApi->get_my_models_count_v1_assets_counts_models_my_get: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

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

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_my_models_v1_assets_models_my_get**
> List[MLModel] get_my_models_v1_assets_models_my_get(offset=offset, limit=limit)

Get My Models

### Example


```python
import aiod_rail_sdk
from aiod_rail_sdk.models.ml_model import MLModel
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
    api_instance = aiod_rail_sdk.AssetsApi(api_client)
    offset = 0 # int |  (optional) (default to 0)
    limit = 100 # int |  (optional) (default to 100)

    try:
        # Get My Models
        api_response = api_instance.get_my_models_v1_assets_models_my_get(offset=offset, limit=limit)
        print("The response of AssetsApi->get_my_models_v1_assets_models_my_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AssetsApi->get_my_models_v1_assets_models_my_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **offset** | **int**|  | [optional] [default to 0]
 **limit** | **int**|  | [optional] [default to 100]

### Return type

[**List[MLModel]**](MLModel.md)

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

# **get_platforms_v1_assets_platforms_get**
> List[Platform] get_platforms_v1_assets_platforms_get(offset=offset, limit=limit)

Get Platforms

### Example


```python
import aiod_rail_sdk
from aiod_rail_sdk.models.platform import Platform
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
    api_instance = aiod_rail_sdk.AssetsApi(api_client)
    offset = 0 # int |  (optional) (default to 0)
    limit = 100 # int |  (optional) (default to 100)

    try:
        # Get Platforms
        api_response = api_instance.get_platforms_v1_assets_platforms_get(offset=offset, limit=limit)
        print("The response of AssetsApi->get_platforms_v1_assets_platforms_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AssetsApi->get_platforms_v1_assets_platforms_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **offset** | **int**|  | [optional] [default to 0]
 **limit** | **int**|  | [optional] [default to 100]

### Return type

[**List[Platform]**](Platform.md)

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

# **get_publication_v1_assets_publications_id_get**
> Publication get_publication_v1_assets_publications_id_get(id)

Get Publication

### Example


```python
import aiod_rail_sdk
from aiod_rail_sdk.models.publication import Publication
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
    api_instance = aiod_rail_sdk.AssetsApi(api_client)
    id = 56 # int | 

    try:
        # Get Publication
        api_response = api_instance.get_publication_v1_assets_publications_id_get(id)
        print("The response of AssetsApi->get_publication_v1_assets_publications_id_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AssetsApi->get_publication_v1_assets_publications_id_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **int**|  | 

### Return type

[**Publication**](Publication.md)

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

# **get_publications_count_v1_assets_counts_publications_get**
> int get_publications_count_v1_assets_counts_publications_get()

Get Publications Count

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
    api_instance = aiod_rail_sdk.AssetsApi(api_client)

    try:
        # Get Publications Count
        api_response = api_instance.get_publications_count_v1_assets_counts_publications_get()
        print("The response of AssetsApi->get_publications_count_v1_assets_counts_publications_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AssetsApi->get_publications_count_v1_assets_counts_publications_get: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

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

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_publications_v1_assets_publications_get**
> List[Publication] get_publications_v1_assets_publications_get(offset=offset, limit=limit)

Get Publications

### Example


```python
import aiod_rail_sdk
from aiod_rail_sdk.models.publication import Publication
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
    api_instance = aiod_rail_sdk.AssetsApi(api_client)
    offset = 0 # int |  (optional) (default to 0)
    limit = 100 # int |  (optional) (default to 100)

    try:
        # Get Publications
        api_response = api_instance.get_publications_v1_assets_publications_get(offset=offset, limit=limit)
        print("The response of AssetsApi->get_publications_v1_assets_publications_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AssetsApi->get_publications_v1_assets_publications_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **offset** | **int**|  | [optional] [default to 0]
 **limit** | **int**|  | [optional] [default to 100]

### Return type

[**List[Publication]**](Publication.md)

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

# **search_datasets_v1_assets_datasets_search_query_get**
> List[Dataset] search_datasets_v1_assets_datasets_search_query_get(query, offset=offset, limit=limit)

Search Datasets

### Example


```python
import aiod_rail_sdk
from aiod_rail_sdk.models.dataset import Dataset
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
    api_instance = aiod_rail_sdk.AssetsApi(api_client)
    query = 'query_example' # str | 
    offset = 0 # int |  (optional) (default to 0)
    limit = 100 # int |  (optional) (default to 100)

    try:
        # Search Datasets
        api_response = api_instance.search_datasets_v1_assets_datasets_search_query_get(query, offset=offset, limit=limit)
        print("The response of AssetsApi->search_datasets_v1_assets_datasets_search_query_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AssetsApi->search_datasets_v1_assets_datasets_search_query_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **query** | **str**|  | 
 **offset** | **int**|  | [optional] [default to 0]
 **limit** | **int**|  | [optional] [default to 100]

### Return type

[**List[Dataset]**](Dataset.md)

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

# **search_models_v1_assets_models_search_query_get**
> List[MLModel] search_models_v1_assets_models_search_query_get(query, offset=offset, limit=limit)

Search Models

### Example


```python
import aiod_rail_sdk
from aiod_rail_sdk.models.ml_model import MLModel
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
    api_instance = aiod_rail_sdk.AssetsApi(api_client)
    query = 'query_example' # str | 
    offset = 0 # int |  (optional) (default to 0)
    limit = 100 # int |  (optional) (default to 100)

    try:
        # Search Models
        api_response = api_instance.search_models_v1_assets_models_search_query_get(query, offset=offset, limit=limit)
        print("The response of AssetsApi->search_models_v1_assets_models_search_query_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AssetsApi->search_models_v1_assets_models_search_query_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **query** | **str**|  | 
 **offset** | **int**|  | [optional] [default to 0]
 **limit** | **int**|  | [optional] [default to 100]

### Return type

[**List[MLModel]**](MLModel.md)

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

# **search_publications_v1_assets_publications_search_query_get**
> List[Publication] search_publications_v1_assets_publications_search_query_get(query, offset=offset, limit=limit)

Search Publications

### Example


```python
import aiod_rail_sdk
from aiod_rail_sdk.models.publication import Publication
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
    api_instance = aiod_rail_sdk.AssetsApi(api_client)
    query = 'query_example' # str | 
    offset = 0 # int |  (optional) (default to 0)
    limit = 100 # int |  (optional) (default to 100)

    try:
        # Search Publications
        api_response = api_instance.search_publications_v1_assets_publications_search_query_get(query, offset=offset, limit=limit)
        print("The response of AssetsApi->search_publications_v1_assets_publications_search_query_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AssetsApi->search_publications_v1_assets_publications_search_query_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **query** | **str**|  | 
 **offset** | **int**|  | [optional] [default to 0]
 **limit** | **int**|  | [optional] [default to 100]

### Return type

[**List[Publication]**](Publication.md)

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


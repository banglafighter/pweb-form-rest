from functools import wraps
from pweb_form_rest.common.pweb_fr_config import PWebFRConfig
from pweb_form_rest.common.pweb_fr_constant import SwaggerDefinitionType, HTTPContentType, SwaggerCommon, HTTPMethod, \
    SwaggerDataType
from pweb_form_rest.swagger.pweb_swagger_param_def import SwaggerParamDef


def add_swagger_endpoint(
        request_obj=None, request_list=None, response_obj=None,
        response_list=None, query_params: list = None,
        url_params: list = None, tag: str = None, method: str = None,
        def_type: str = SwaggerDefinitionType.NONE, http_response_code: int = 200,
        response_content_type: str = HTTPContentType.APPLICATION_JSON,
        request_content_type: str = HTTPContentType.APPLICATION_JSON,
        pweb_message_response: bool = False, pweb_error_details_response: bool = False):
    def decorator(function):
        function.__pweb_swagger__ = SwaggerCommon.PWEB_SWAGGER

        @wraps(function)
        def pweb_swagger_def(*args, **kwargs):
            if 'pass_definition' in kwargs and kwargs['pass_definition']:
                definition = SwaggerParamDef()
                definition.request_obj = request_obj
                definition.request_list = request_list
                definition.response_obj = response_obj
                definition.response_list = response_list
                definition.query_params = query_params
                definition.url_params = url_params
                definition.http_response_code = http_response_code
                definition.response_content_type = response_content_type
                definition.request_content_type = request_content_type
                definition.pweb_error_details_response = pweb_error_details_response
                definition.tag = tag
                definition.method = method
                definition.def_type = def_type
                definition.pweb_message_response = pweb_message_response
                return definition
            return function(*args, **kwargs)

        return pweb_swagger_def

    return decorator


def pweb_endpoint(
        request_obj=None, request_list=None, response_obj=None, method: str = None, response_list=None,
        query_params: list = None, url_params: list = None, tag: str = None, def_type: str = SwaggerDefinitionType.NONE,
        http_response_code: int = 200, response_content_type: str = HTTPContentType.APPLICATION_JSON,
        request_content_type: str = HTTPContentType.APPLICATION_JSON, pweb_message_response: bool = False,
        pweb_error_details_response: bool = False):
    return add_swagger_endpoint(
        request_obj=request_obj, request_list=request_list, response_obj=response_obj, response_list=response_list,
        method=method, query_params=query_params, url_params=url_params, def_type=def_type,
        tag=tag, pweb_message_response=pweb_message_response, pweb_error_details_response=pweb_error_details_response,
        http_response_code=http_response_code, response_content_type=response_content_type,
        request_content_type=request_content_type
    )


def pweb_upload_endpoint(
        request_obj=None, request_list=None, response_obj=None,
        response_list=None, query_params: list = None,
        url_params: list = None, tag: str = None,
        http_response_code: int = 200, response_content_type: str = HTTPContentType.APPLICATION_JSON,
        pweb_message_response: bool = False, pweb_error_details_response: bool = False):
    return add_swagger_endpoint(
        def_type=SwaggerDefinitionType.FILE_UPLOAD,
        request_obj=request_obj, request_list=request_list, response_obj=response_obj, response_list=response_list,
        method=HTTPMethod.POST, query_params=query_params, url_params=url_params,
        tag=tag, pweb_message_response=pweb_message_response,
        http_response_code=http_response_code, response_content_type=response_content_type,
        request_content_type=HTTPContentType.MULTIPART_FORM_DATA,
        pweb_error_details_response=pweb_error_details_response
    )


def pweb_paginate_endpoint(
        response_obj=None, query_params: list = None,
        url_params: list = None, tag: str = None, method: str = HTTPMethod.GET,
        pagination: bool = True, sorting: bool = True, search: bool = True,
        http_response_code: int = 200, response_content_type: str = HTTPContentType.APPLICATION_JSON,
        pweb_message_response: bool = False):
    if not query_params:
        query_params = []

    if pagination:
        query_params.append((PWebFRConfig.PAGE_PARAM_NAME, SwaggerDataType.integer))
        query_params.append((PWebFRConfig.ITEM_PER_PAGE_PARAM_NAME, SwaggerDataType.integer))

    if sorting:
        query_params.append((PWebFRConfig.SORT_FIELD_PARAM_NAME, SwaggerDataType.string))
        query_params.append((PWebFRConfig.SORT_ORDER_PARAM_NAME, SwaggerDataType.string))

    if search:
        query_params.append((PWebFRConfig.SEARCH_FIELD_PARAM_NAME, SwaggerDataType.string))

    return add_swagger_endpoint(
        method=method, query_params=query_params, url_params=url_params,
        tag=tag, pweb_message_response=pweb_message_response, response_list=response_obj,
        http_response_code=http_response_code, response_content_type=response_content_type
    )

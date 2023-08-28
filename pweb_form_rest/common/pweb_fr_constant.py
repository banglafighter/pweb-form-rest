class SwaggerDefinitionType(object):
    NONE = None
    PAGINATION = "PAGINATION"
    FILE_UPLOAD = "FILE_UPLOAD"


class SwaggerCommon(object):
    PWEB_SWAGGER = "PWEB_SWAGGER"


class SwaggerDataType(object):
    integer = "integer"
    number = "number"
    string = "string"


class HTTPContentType(object):
    APPLICATION_JSON = "application/json"
    MULTIPART_FORM_DATA = "multipart/form-data"
    FORM_DATA = "application/x-www-form-urlencoded"


class HTTPMethod(object):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"

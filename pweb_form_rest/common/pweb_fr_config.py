class PWebFRConfig:
    # API Config
    PAGE_PARAM_NAME: str = "page"
    ITEM_PER_PAGE_PARAM_NAME: str = "per-page"
    SORT_FIELD_PARAM_NAME: str = "sort-field"
    SORT_ORDER_PARAM_NAME: str = "sort-order"
    SEARCH_FIELD_PARAM_NAME: str = "search"
    SORT_DEFAULT_ORDER_NAME: str = "desc"
    SORT_DEFAULT_FIELD_NAME: str = "id"
    TOTAL_ITEM_PER_PAGE: int = 25

    # Swagger UI Config
    ENABLE_SWAGGER_UI: bool = True
    ENABLE_SWAGGER_AUTH: bool = False
    SWAGGER_AUTH_USERNAME: str = "pweb"
    SWAGGER_AUTH_PASSWORD: str = "pweb12"
    SWAGGER_JSON_URL: str = "/pweb-swagger-json"
    SWAGGER_UI_URL: str = "/pweb-swagger-ui"
    SWAGGER_UI_ASSETS_URL: str = "/swagger-assets"
    SWAGGER_DEFAULT_TAG_NAME: str = "Common"
    SWAGGER_TITLE: str = "PWeb Swagger"
    SWAGGER_APP_VERSION: str = "1.0.0"

    ENABLED_JWT_AUTH: bool = True

    # Messages
    INVALID_REQUEST_DATA: str = "Invalid Request Data"
    VALIDATION_ERROR: str = "Validation Error!"
    UNKNOWN_ERROR: str = "Unknown Error Occurred!"

    # File Upload
    FILE_SIZE_NOT_MATCH: str = "File size is bigger than allowed"
    INVALID_FILE_EXTENSION: str = "Invalid uploaded file"
    INVALID_FILE_UPLOAD_PATH: str = "Invalid upload path"

    # Form Helper
    SSR_UI_HELPER: "PWebSSRUIHelper" = None

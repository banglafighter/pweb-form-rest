class PWebFRConfig:
    # API Config
    PAGE_PARAM_NAME: str = "page"
    ITEM_PER_PAGE_PARAM_NAME: str = "per-page"
    SORT_FIELD_PARAM_NAME: str = "sort-field"
    SORT_ORDER_PARAM_NAME: str = "sort-order"
    SEARCH_FIELD_PARAM_NAME: str = "search"
    SORT_DEFAULT_ORDER_NAME: str = "desc"
    SORT_DEFAULT_FIELD_NAME: str = "id"

    # Swagger UI Config
    ENABLE_SWAGGER_UI: bool = True
    ENABLE_SWAGGER_AUTH: bool = False
    SWAGGER_AUTH_USERNAME: str = "pweb"
    SWAGGER_AUTH_PASSWORD: str = "pweb12"
    SWAGGER_JSON_URL = "/pweb-swagger-json"
    SWAGGER_UI_URL = "/pweb-swagger-ui"
    SWAGGER_DEFAULT_TAG_NAME: str = "Common"

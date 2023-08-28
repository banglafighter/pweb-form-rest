from pweb_form_rest.schema.pweb_rest_schema import APIBase, APIMessageResponse, APIErrorResponse, APIDataResponse, \
    APIDataListResponse, APIPaginateResponse


class PWebBaseResponse:
    status: str = None
    code: str = None
    httpCode: int = None
    message: str = None

    def make_dict(self, data, api_base: APIBase, many=False):
        return api_base.dumps(data, many=many)


class PWebMessageResponse(PWebBaseResponse):
    message: str = None

    def to_dict(self):
        return self.make_dict(self, APIMessageResponse())


class PWebErrorResponse(PWebMessageResponse):
    error: dict = None

    def to_dict(self):
        return self.make_dict(self, APIErrorResponse())


class PWebDataResponse(PWebBaseResponse):
    _schema = APIDataResponse()
    data: any

    def __init__(self):
        self.data = None

    def add_data(self, model, schema: APIBase, many=False):
        if many:
            self._schema = APIDataListResponse()
        else:
            self._schema = APIDataResponse()

        if model and schema:
            self.add_only_data(model, schema, many)

    def add_only_data(self, model, schema: APIBase, many=False):
        if model:
            self.data = schema.dump(model, many=many)

    def to_dict(self):
        return self.make_dict(self, self._schema)


class PWebPagination(object):
    page: int = None
    itemPerPage: int = None
    total: int = None
    totalPage: int = None


class PWebPaginateResponse(PWebDataResponse):
    _schema = APIPaginateResponse()
    pagination: PWebPagination = None

    def to_dict(self):
        return self.make_dict(self, self._schema)

from marshmallow import Schema, fields


class APIBase(Schema):
    class Meta:
        ordered = True


class APIBaseResponse(APIBase):
    class Meta:
        ordered = True

    status = fields.String()
    code = fields.String()


class APIMessageResponse(APIBaseResponse):
    message = fields.String()


class APIErrorResponse(APIBaseResponse):
    error = fields.Dict(keys=fields.String(), values=fields.String())


class APIDataResponse(APIBaseResponse):
    message = fields.String()
    data = fields.Dict()


class APIDataListResponse(APIBaseResponse):
    data = fields.List(fields.Dict)


class Pagination(APIBase):
    page = fields.Integer()
    itemPerPage = fields.Integer()
    total = fields.Integer()
    totalPage = fields.Integer()


class APIPaginateResponse(APIDataListResponse):
    pagination = fields.Nested(Pagination())

from pweb_form_rest.crud.pweb_crud import PWebCRUD
from pweb_form_rest.crud.pweb_response_maker import ResponseMaker
from pweb_form_rest.schema.pweb_rest_schema import PWebDataDTO
from pweb_orm import PWebBaseModel


class PWebCRUDCommon:
    model: PWebBaseModel = None
    pweb_crud: PWebCRUD = PWebCRUD()
    response_maker: ResponseMaker = ResponseMaker()

    def message_or_data_response(self, model, response_dto: PWebDataDTO = None, response_message: str = None):
        if not response_dto:
            return self.response_maker.success_message(response_message)
        return self.response_maker.data_response(model, response_dto)

    def get_json_data(self, data_dto: PWebDataDTO, is_validate=True, load_only=False):
        return self.pweb_crud.get_json_data(data_dto=data_dto, is_validate=is_validate, load_only=load_only)

    def get_form_data(self, data_dto: PWebDataDTO, is_validate=True, load_only=False, is_populate_model=False):
        return self.pweb_crud.get_form_data(data_dto=data_dto, is_validate=is_validate, is_populate_model=is_populate_model, load_only=load_only)

    def check_unique(self, field: str, value, model_id=None, exception: bool = True, message: str = "Already used", query=None):
        self.pweb_crud.check_unique(self.model, field=field, value=value, exception=exception, message=message, query=query, model_id=model_id)

    def get_by_id(self, model_id, exception=True, message: str = "Entry Not Found!", query=None):
        return self.pweb_crud.get_by_id(self.model, id=model_id, exception=exception, message=message, query=query)

    def read_all(self, query=None, search_fields: list = None, sort_field=None, sort_order=None, item_per_page=None, enable_pagination=True):
        return self.pweb_crud.list(model=self.model, query=query, search_fields=search_fields, sort_field=sort_field, sort_order=sort_order, item_per_page=item_per_page, enable_pagination=enable_pagination)

    def save(self, data: dict, request_dto: PWebDataDTO, existing_model=None):
        model = self.pweb_crud.populate_model(data, request_dto, instance=existing_model)
        model.save()
        return model

    def edit(self, model_id, data: dict, request_dto: PWebDataDTO, existing_model=None, query=None):
        if not existing_model:
            existing_model = self.get_by_id(model_id, query=query, exception=True)
        return self.save(data=data, request_dto=request_dto, existing_model=existing_model)

    def soft_remove(self, model_id: int, query=None, exception=True):
        existing_model = self.get_by_id(model_id, exception=exception, query=query)
        if existing_model and hasattr(existing_model, "isDeleted"):
            existing_model.isDeleted = True
            existing_model.save()
            return True
        return False

    def remove(self, model_id: int, query=None):
        existing_model = self.get_by_id(model_id, exception=True, query=query)
        existing_model.delete()

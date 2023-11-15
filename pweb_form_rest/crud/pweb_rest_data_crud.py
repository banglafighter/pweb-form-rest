from pweb_form_rest.common.pweb_com_fr_message import ComFRMessage
from pweb_form_rest.crud.pweb_crud_common import PWebCRUDCommon
from pweb_form_rest.schema.pweb_rest_schema import PWebDataDTO
from pweb_form_rest.crud.pweb_file_data_crud import FileDataCRUD
from pweb_orm import PWebBaseModel


class RESTDataCRUD(PWebCRUDCommon):
    file_data_crud = None

    def __init__(self, model: PWebBaseModel):
        self.model = model
        self.file_data_crud = FileDataCRUD(model=model)

    def update_and_get_model(self, request_dto: PWebDataDTO, data: dict = None, existing_model=None, query=None):
        if not data:
            data = self.get_json_data(request_dto)
        return self.edit(model_id=data['id'], data=data, request_dto=request_dto, existing_model=existing_model, query=query)

    def create_and_get_model(self, request_dto: PWebDataDTO, data: dict = None):
        if not data:
            data = self.get_json_data(request_dto)
        return self.save(data=data, request_dto=request_dto)

    def create(self, request_dto: PWebDataDTO, response_dto: PWebDataDTO = None, response_message: str = ComFRMessage.create_success, data: dict = None):
        model = self.create_and_get_model(data=data, request_dto=request_dto)
        return self.message_or_data_response(model, response_dto, response_message)

    def details(self, model_id: int, response_dto: PWebDataDTO, query=None):
        existing_model = self.get_by_id(model_id, exception=True, query=query)
        return self.response_maker.data_response(existing_model, response_dto)

    def update(self, request_dto: PWebDataDTO, response_dto: PWebDataDTO = None, response_message: str = ComFRMessage.update_success, existing_model=None, data: dict = None, query=None):
        model = self.update_and_get_model(request_dto=request_dto, existing_model=existing_model, query=query, data=data)
        return self.message_or_data_response(model, response_dto, response_message)

    def delete(self, model_id: int, response_message: str = ComFRMessage.delete_success, query=None):
        self.soft_remove(model_id=model_id, query=query)
        return self.response_maker.success_message(response_message)

    def hard_delete(self, model_id: int, response_message: str = ComFRMessage.delete_success, query=None):
        self.remove(model_id, query=query)
        return self.response_maker.success_message(response_message)

    def paginated_list(self, response_dto: PWebDataDTO, query=None, search_fields: list = None, sort_field=None, sort_order=None, item_per_page=None):
        data_list = self.read_all(query=query, search_fields=search_fields, sort_field=sort_field, sort_order=sort_order, item_per_page=item_per_page)
        return self.response_maker.paginate_response(data_list, response_dto)

    def list(self, response_dto: PWebDataDTO, query=None, search_fields: list = None, sort_field=None, sort_order=None):
        data_list = self.read_all(query=query, search_fields=search_fields, sort_field=sort_field, sort_order=sort_order, enable_pagination=False)
        return self.response_maker.list_data_type_response(data_list, response_dto=response_dto)

    def upload_file_data(self, request_dto: PWebDataDTO, upload_path, response_dto: PWebDataDTO = None, override_names: dict = None, response_message: str = ComFRMessage.create_success, form_data=None):
        return self.file_data_crud.upload_file_data(request_dto=request_dto, upload_path=upload_path, response_dto=response_dto, override_names=override_names, response_message=response_message, form_data=form_data)

    def update_upload_file_data(self, request_dto: PWebDataDTO, upload_path, response_dto: PWebDataDTO = None, override_names: dict = None, response_message: str = ComFRMessage.update_success, existing_model=None, form_data: dict = None, query=None):
        return self.file_data_crud.update_upload_file_data(request_dto=request_dto, upload_path=upload_path, response_dto=response_dto, override_names=override_names, response_message=response_message, existing_model=existing_model, form_data=form_data, query=query)

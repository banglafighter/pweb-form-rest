from marshmallow import ValidationError
from pweb_form_rest.common.pweb_fr_exception import FormRESTException
from pweb_form_rest.crud.pweb_crud import PWebCRUD
from pweb_form_rest.crud.pweb_request_data import RequestData
from pweb_form_rest.form.pweb_form_definition import FormDefinition
from pweb_form_rest.schema.pweb_rest_schema import PWebOrmDTO


class PWebFormData:
    request_data: RequestData = RequestData()
    pweb_crud: PWebCRUD = PWebCRUD()

    def is_post_data(self) -> bool:
        return self.request_data.is_post()

    def is_valid_data(self, form: PWebOrmDTO, definition: FormDefinition, form_data=None) -> bool:
        try:
            if not form_data:
                form_data = definition.get_request_data()

            if form_data:
                definition.set_field_value(field_and_value=form_data)

            self.pweb_crud.get_form_data(data_dto=form, form_data=form_data)
            return True
        except ValidationError as e:
            errors = {}
            if e and e.messages_dict and isinstance(e.messages_dict, dict):
                for name, error in e.messages_dict.items():
                    errors[name] = ', '.join(error)
            definition.set_field_errors(errors)
        except FormRESTException as e:
            if e.messageResponse and e.messageResponse.error:
                definition.set_field_errors(e.messageResponse.error)
        return False

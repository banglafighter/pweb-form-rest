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

    def is_get_data(self) -> bool:
        return self.request_data.is_get()

    def handle_validation_exception(self, exception, definition: FormDefinition):
        errors = {}
        if exception and exception.messages_dict and isinstance(exception.messages_dict, dict):
            for name, error in exception.messages_dict.items():
                errors[name] = ', '.join(error)
        definition.set_field_errors(errors)

    def handle_form_rest_exception(self, exception, definition: FormDefinition):
        if exception.messageResponse and hasattr(exception.messageResponse, "error") and exception.messageResponse.error:
            definition.set_field_errors(exception.messageResponse.error)

    def is_valid_data(self, form: PWebOrmDTO, definition: FormDefinition, form_data=None) -> bool:
        try:
            if not form_data:
                form_data = definition.get_request_data()

            if form_data:
                definition.set_field_value(field_and_value=form_data)

            if definition.is_validation_error:
                return False

            self.pweb_crud.get_form_data(data_dto=form, form_data=form_data)
            return True
        except ValidationError as e:
            self.handle_validation_exception(exception=e, definition=definition)
        except FormRESTException as e:
            self.handle_form_rest_exception(exception=e, definition=definition)
        return False

from pweb_form_rest.form.pweb_form_data import PWebFormData
from pweb_form_rest.form.pweb_form_definition import FormDefinition
from pweb_form_rest.schema.pweb_rest_schema import PWebRestDTO


class PWebBaseForm:
    pass


class PWebForm(PWebBaseForm, PWebRestDTO):
    definition: FormDefinition = None
    pweb_form_data: PWebFormData = PWebFormData()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.definition = FormDefinition()
        self.definition.init(self.declared_fields)

    def set_select_option(self, field_name, select_options: dict):
        return self.definition.set_select_option(field_name=field_name, select_options=select_options)

    def process_and_set_option(self, field_name, options: list, key_name: str, value_name: str):
        return self.definition.process_and_set_option(field_name=field_name, options=options, key_name=key_name, value_name=value_name)

    def is_post_data(self) -> bool:
        return self.pweb_form_data.is_post_data()

    def is_get_data(self) -> bool:
        return self.pweb_form_data.is_get_data()

    def is_valid_data_submit(self, form_data=None):
        if self.is_post_data() and self.is_valid_data(form_data=form_data):
            return True
        return False

    def is_valid_data(self, form_data=None) -> bool:
        return self.pweb_form_data.is_valid_data(form=self, form_data=form_data, definition=self.definition)

    def get_request_data(self, form_data=None):
        return self.definition.get_request_data(all_data=form_data)

    def set_value(self, field_name, value):
        return self.definition.set_value(field_name=field_name, value=value)

    def set_dict_value(self, name_value: dict):
        return self.definition.set_dict_value(name_value=name_value)

    def set_model_value(self, model):
        return self.definition.set_model_value(model=model)

    def set_field_error(self, field_name, error):
        if self.definition:
            self.definition.set_field_errors({field_name: error})

from pweb_form_rest.form.pweb_form_definition import FormDefinition
from pweb_form_rest.schema.pweb_rest_schema import PWebRestDTO


class PWebBaseForm:
    pass


class PWebForm(PWebBaseForm, PWebRestDTO):
    definition: FormDefinition = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.definition = FormDefinition()
        self.definition.init(self.declared_fields)

    def set_select_option(self, field_name, select_options: dict):
        return self.definition.set_select_option(field_name=field_name, select_options=select_options)

    def process_and_set_option(self, field_name, options: list, key_name: str, value_name: str):
        return self.definition.process_and_set_option(field_name=field_name, options=options, key_name=key_name, value_name=value_name)

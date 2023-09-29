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

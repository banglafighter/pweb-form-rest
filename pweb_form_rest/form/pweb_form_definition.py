from pweb_form_rest.form.pweb_form_field import FormField
from pweb_form_rest.form.pweb_process_form_field import ProcessFormFiled


class FormDefinition:
    process_form_filed = ProcessFormFiled()

    def init(self, declared_fields: dict = None):
        self._process_form_field(declared_fields)

    def _process_form_field(self, declared_fields: dict, existing_form_definition=None):
        for field_name in declared_fields:
            declared_field_definition = declared_fields[field_name]
            if declared_field_definition and not declared_field_definition.dump_only:
                form_field: FormField = self._convert_declared_field_to_form_field(declared_field_definition, existing_form_definition)
                setattr(self, form_field.name, form_field)

    def _convert_declared_field_to_form_field(self, declared_field_definition, existing_form_definition=None):
        form_field: FormField = FormField()
        if existing_form_definition and hasattr(existing_form_definition, declared_field_definition.name):
            form_field = getattr(existing_form_definition, declared_field_definition.name)
        form_field = self.process_form_filed.start(declared_field_definition, form_field=form_field)
        return form_field

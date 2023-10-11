from ppy_file_text import StringUtil
from pweb_form_rest.form.pweb_form_field import FormField


class ProcessFormFiled:

    def start(self, declared_field_definition, form_field: FormField):
        form_field = self._set_basic_information(declared_field_definition, form_field=form_field)
        form_field = self._set_field_default_value(declared_field_definition, form_field=form_field)
        form_field = self._process_metadata(declared_field_definition, form_field=form_field)
        form_field = self._process_enum_to_select_option(declared_field_definition, form_field=form_field)
        form_field = self._set_required_error_text(declared_field_definition, form_field=form_field)
        form_field = self._set_label(form_field=form_field)
        form_field = self._set_input_type(form_field=form_field)
        return form_field

    def _set_input_type(self, form_field: FormField):
        if not form_field.inputType and form_field.dataType:
            data_type = form_field.dataType
            if data_type == "Integer" or data_type == "Float" or data_type == "Decimal":
                form_field.inputType = "number"
            elif data_type == "Email":
                form_field.inputType = "email"
            elif data_type == "EnumField":
                form_field.inputType = "select"
            elif data_type == "Date":
                form_field.inputType = "date"
            elif data_type == "FileField":
                form_field.inputType = "file"
            else:
                form_field.inputType = "text"
        return form_field

    def _get_field_data(self, declared_field_definition, name, default=None):
        if hasattr(declared_field_definition, name):
            return getattr(declared_field_definition, name)
        return default

    def _set_required_error_text(self, declared_field_definition, form_field: FormField):
        if declared_field_definition.required and hasattr(declared_field_definition, "error_messages") and "required" in declared_field_definition.error_messages:
            form_field.errorText = declared_field_definition.error_messages["required"]
        return form_field

    def _set_basic_information(self, declared_field_definition, form_field: FormField):
        form_field.name = self._get_field_data(declared_field_definition, "name", default=form_field.required)
        form_field.required = self._get_field_data(declared_field_definition, "required", default=form_field.required)
        form_field.dataType = declared_field_definition.__class__.__name__
        return form_field

    def _set_field_default_value(self, declared_field_definition, form_field: FormField):
        default_value = self._get_field_data(declared_field_definition, "defaultValue", form_field.defaultValue)
        if not form_field.value and default_value:
            form_field.value = default_value
        return form_field

    def process_attributes(self, declared_attributes: dict, form_field: FormField, ignore: list = None):
        if not declared_attributes or not isinstance(declared_attributes, dict):
            return form_field

        if not form_field.allAttributes:
            form_field.allAttributes = {}

        for attribute_name in declared_attributes:
            if ignore and attribute_name in ignore:
                continue

            if attribute_name not in form_field.allAttributes:
                form_field.allAttributes[attribute_name] = declared_attributes[attribute_name]
            elif attribute_name in form_field.allAttributes:
                form_field.allAttributes[attribute_name] += f" {declared_attributes[attribute_name]}"

        return form_field

    def _process_metadata(self, declared_field_definition, form_field: FormField):
        metadata: dict = declared_field_definition.metadata
        for name in metadata:
            if hasattr(form_field, name):
                setattr(form_field, name, metadata[name])
            elif name == "type":
                form_field.inputType = metadata[name]
            elif name == "attributes":
                form_field = self.process_attributes(metadata[name], form_field)
        return form_field

    def _set_label(self, form_field: FormField):
        if not form_field.label and form_field.name and form_field.isLabel:
            form_field.label = StringUtil.human_readable(form_field.name)
        return form_field

    def _process_enum_to_select_option(self, declared_field_definition, form_field: FormField):
        if not form_field.selectOptions and hasattr(declared_field_definition, "enumType"):
            form_field.selectOptions = {}
            for enumItem in declared_field_definition.enumType:
                form_field.selectOptions[enumItem.name] = enumItem.value
        return form_field

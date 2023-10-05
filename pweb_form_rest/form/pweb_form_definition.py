from pweb_form_rest.crud.pweb_request_data import RequestData
from pweb_form_rest.form.pweb_form_field import FormField
from pweb_form_rest.form.pweb_process_form_field import ProcessFormFiled


class FormDefinition:
    is_validation_error: bool = False
    process_form_filed = ProcessFormFiled()
    request_data: RequestData = RequestData()
    _record_form_fields: list = []
    _record_check_uncheck_fields: list = []

    def init(self, declared_fields: dict = None):
        self.is_validation_error = False
        self._process_form_field(declared_fields)

    def _process_form_field(self, declared_fields: dict, existing_form_definition=None):
        for field_name in declared_fields:
            declared_field_definition = declared_fields[field_name]
            if declared_field_definition and not declared_field_definition.dump_only:
                if field_name not in self._record_form_fields:
                    self._record_form_fields.append(field_name)
                form_field: FormField = self._convert_declared_field_to_form_field(declared_field_definition, existing_form_definition)
                if form_field.inputType == "radio" or form_field.inputType == "checkbox":
                    self._record_check_uncheck_fields.append(field_name)
                setattr(self, form_field.name, form_field)

    def _convert_declared_field_to_form_field(self, declared_field_definition, existing_form_definition=None):
        form_field: FormField = FormField()
        if existing_form_definition and hasattr(existing_form_definition, declared_field_definition.name):
            form_field = getattr(existing_form_definition, declared_field_definition.name)
        form_field = self.process_form_filed.start(declared_field_definition, form_field=form_field)
        return form_field

    def get_form_field(self, field_name):
        if hasattr(self, field_name):
            return getattr(self, field_name)
        return None

    def set_select_option(self, field_name, select_options: dict):
        form_field = self.get_form_field(field_name=field_name)
        if not form_field or not select_options or not isinstance(select_options, dict):
            return False
        form_field.selectOptions = select_options
        return True

    def process_and_set_option(self, field_name, options: list, key_name: str, value_name: str):
        select_options = {}
        for option in options:
            if key_name in option and value_name in option:
                select_options[option[key_name]] = option[value_name]
        return self.set_select_option(field_name=field_name, select_options=select_options)

    def set_field_errors(self, errors: dict):
        self.is_validation_error = True
        for field_name in errors:
            if hasattr(self, field_name):
                form_field: FormField = getattr(self, field_name)
                form_field.errorText = errors[field_name]
                form_field.isError = True

    def set_field_value(self, field_and_value: dict):
        for field_name in field_and_value:
            if hasattr(self, field_name) and field_and_value[field_name] != None:
                form_field: FormField = getattr(self, field_name)
                form_field.value = field_and_value[field_name]

    def set_dict_value(self, name_value: dict):
        if name_value and isinstance(name_value, dict):
            self.set_field_value(name_value)
            return True
        return False

    def set_value(self, field_name, value):
        if field_name and value:
            self.set_field_value({field_name: value})
            return True
        return False

    def set_model_value(self, model):
        for field_name in self._record_form_fields:
            if hasattr(self, field_name) and hasattr(model, field_name):
                value = getattr(model, field_name)
                self.set_value(field_name, value)

    def get_request_data(self, all_data=None):
        if not all_data:
            all_data = self.request_data.form_and_file_data()

        for field_name in list(all_data.keys()):
            if hasattr(self, field_name):
                form_field: FormField = getattr(self, field_name)
                if form_field.dataType in ["Integer", "Float", "DateTime", "Date", "EnumField", "FileField", "Boolean"] and all_data[field_name] == "":
                    all_data[field_name] = None
                if form_field.required and (all_data[field_name] == "" or all_data[field_name] is None):
                    del all_data[field_name]

        if self._record_check_uncheck_fields:
            for check_uncheck_input in self._record_check_uncheck_fields:
                if check_uncheck_input not in all_data and hasattr(self, check_uncheck_input):
                    form_field: FormField = getattr(self, check_uncheck_input)
                    all_data[check_uncheck_input] = form_field.unchecked

        return all_data

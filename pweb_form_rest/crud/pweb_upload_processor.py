from werkzeug.datastructures import FileStorage
from ppy_file_text import FileUtil
from pweb_form_rest import FileField
from pweb_form_rest.common.pweb_fr_config import PWebFRConfig
from pweb_form_rest.common.pweb_fr_exception import form_rest_exception
from pweb_form_rest.common.pweb_web_file_util import PWebWebFileUtil
from pweb_form_rest.schema.pweb_rest_schema import PWebDataDTO


class PWebUploadProcessor:

    def validate_file_size(self, file_storage: FileStorage, field: FileField):
        if field.max_size_kb and not PWebWebFileUtil.is_valid_file_size(file_storage, field.max_size_kb):
            raise form_rest_exception.error_message_exception(PWebFRConfig.FILE_SIZE_NOT_MATCH)
        return True

    def validate_file_extension(self, file_storage: FileStorage, field: FileField):
        if field.allowed_extensions and not PWebWebFileUtil.allowed_file(file_storage.filename, field.allowed_extensions):
            raise form_rest_exception.error_message_exception(PWebFRConfig.INVALID_FILE_EXTENSION)
        return True

    def upload_file(self, input_name, file_storage: FileStorage, upload_path, override_name: dict = None, override: bool = True):
        filename = file_storage.filename.lower()
        filename = PWebWebFileUtil.process_file_name(filename)
        if override_name and input_name in override_name:
            filename = override_name[input_name] + "." + PWebWebFileUtil.get_file_extension(filename)
        if filename:
            filename = filename.lower()
        FileUtil.create_directories(upload_path)
        file_upload_path = FileUtil.join_path(upload_path, filename)
        if override:
            FileUtil.delete(file_upload_path)
            file_storage.save(file_upload_path)
        return filename

    def delete_file(self, upload_path, filename):
        file_upload_path = FileUtil.join_path(upload_path, filename)
        FileUtil.delete(file_upload_path)

    def validate_and_upload_multiple(self, form_data: dict, request_dto: PWebDataDTO, upload_path, override_name: dict = None, override: bool = True):
        response_file_name_dict = {}

        for input_name in form_data:
            file_list = form_data[input_name]

            if not isinstance(file_list, list):
                file_list = [file_list]

            override_name_index = 0
            uploaded_file_names = []
            file_name = self._get_upload_file_override_name(input_name, override_name, override_name_index)
            if file_name:
                uploaded_file_names = {}

            for file in file_list:
                file_name = self._get_upload_file_override_name(input_name, override_name, override_name_index)
                override_name_index += 1
                _override_name = None

                if file_name:
                    _override_name = {input_name: file_name}
                response = self.validate_and_upload(
                    files={input_name: file},
                    request_dto=request_dto,
                    upload_path=upload_path,
                    override_name=_override_name,
                    override=override)

                if isinstance(uploaded_file_names, list):
                    uploaded_file_names.append(response[input_name])
                elif isinstance(uploaded_file_names, dict) and file_name:
                    uploaded_file_names[file_name] = response[input_name]

            response_file_name_dict.update({input_name: uploaded_file_names})
        return response_file_name_dict

    def validate_and_upload(self, files: dict, request_dto: PWebDataDTO, upload_path, override_name: dict = None, override: bool = True):
        errors = {}
        if not upload_path:
            raise form_rest_exception.error_details_exception(PWebFRConfig.INVALID_FILE_UPLOAD_PATH, errors)

        for input_name in files:
            try:
                field: FileField = self._get_file_input(input_name, request_dto)
                if field and isinstance(files[input_name], FileStorage):
                    file_storage: FileStorage = files[input_name]
                    self.validate_file_size(file_storage, field)
                    self.validate_file_extension(file_storage, field)
                    files[input_name] = self.upload_file(input_name, file_storage, upload_path, override_name, override)
            except Exception as e:
                errors[input_name] = str(e)
        if errors:
            raise form_rest_exception.error_details_exception(PWebFRConfig.VALIDATION_ERROR, errors)
        return files

    def get_file_override_names(self, uuid, request_dto: PWebDataDTO, override_names: dict = None):
        if not override_names:
            override_names = {}
        for field_name in request_dto.fields:
            field = request_dto.fields[field_name]
            if isinstance(field, FileField) and field.name not in override_names:
                prefix = ""
                if field.save_prefix:
                    prefix = field.save_prefix + "-"
                override_names[field.name] = (prefix + uuid).lower()
        return override_names

    def delete_orphan_files(self, override_names: dict, form_data, model, upload_path):
        for name in override_names:
            if "deletedItem" in form_data and name in form_data["deletedItem"]:
                if hasattr(model, name) and (name not in form_data or not isinstance(form_data[name], FileStorage)):
                    file_path = FileUtil.join_path(upload_path, getattr(model, name))
                    setattr(model, name, None)
                    FileUtil.delete(file_path)
        return model

    def _get_upload_file_override_name(self, input_name, override_name: dict, index=0):
        if not override_name:
            return None
        file_name = None
        if input_name in override_name:
            if isinstance(override_name[input_name], list):
                file_name = self._get_file_name_from_list(index, override_name[input_name])
            else:
                file_name = override_name[input_name]
        return file_name

    def _get_file_name_from_list(self, index, list_data: list, default_name: str = "file"):
        try:
            if not list_data:
                return None
            return list_data[index]
        except IndexError:
            return default_name + str(index)

    def _get_file_input(self, name: str, request_dto: PWebDataDTO):
        if name in request_dto.fields:
            field = request_dto.fields[name]
            if isinstance(field, FileField):
                return field
        return None

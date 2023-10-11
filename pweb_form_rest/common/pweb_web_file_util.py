import os
from werkzeug.datastructures import FileStorage
from ppy_file_text import StringUtil


class PWebWebFileUtil:

    @staticmethod
    def get_file_size(file_object: FileStorage, default=0):
        if file_object.content_length:
            return file_object.content_length

        try:
            current_position = file_object.tell()
            file_object.seek(0, 2)
            size = file_object.tell()
            file_object.seek(current_position)
            return size
        except (AttributeError, IOError):
            pass

        return default

    @staticmethod
    def is_valid_file_size(file_object: FileStorage, max_size_kb):
        size = PWebWebFileUtil.get_file_size(file_object)
        size_in_kb = round(size / 1024, 4)
        if size_in_kb <= max_size_kb:
            return True
        return False

    @staticmethod
    def allowed_file(filename, file_extensions: list):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in file_extensions

    @staticmethod
    def process_file_name(file_name: str):
        if file_name:
            for sep in os.path.sep, os.path.altsep:
                if sep:
                    file_name = file_name.replace(sep, " ")

            file_name = StringUtil.camelcase_to(file_name, "-")
            file_name = StringUtil.find_and_replace_with(file_name, "_", "-")
            file_name = StringUtil.replace_space_with(file_name, "-")
            file_name = file_name.lower()
        return file_name

    @staticmethod
    def get_file_extension(filename):
        if '.' in filename:
            return filename.rsplit('.', 1)[1].lower()

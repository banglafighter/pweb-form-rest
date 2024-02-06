import os
from pathlib import Path

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
            file_name_only = PWebWebFileUtil.get_file_name_only(file_name)
            file_name_only = StringUtil.remove_special_character(file_name_only)
            file_name_only = StringUtil.replace_multiple_occurrence_to_single_with(text=file_name_only, to="-")
            file_name_only = file_name_only.strip("-")
            file_name_only = file_name_only.rstrip("-")
            file_extension = PWebWebFileUtil.get_file_extension(file_name)
            file_name = f"{file_name_only}.{file_extension}"
            file_name = file_name.lower()
        return file_name

    @staticmethod
    def get_file_extension(filename):
        if '.' in filename:
            return filename.rsplit('.', 1)[1].lower()

    @staticmethod
    def get_file_name_only(filename):
        if filename:
            path = Path(filename)
            return path.stem
        return filename

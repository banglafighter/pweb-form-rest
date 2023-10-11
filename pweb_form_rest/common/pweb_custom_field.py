import enum
from marshmallow import fields, ValidationError
import typing
from werkzeug.datastructures import FileStorage


class FileField(fields.String):
    max_size_kb: int = None
    allowed_extensions: list = None
    is_multiple: bool = False
    is_string_name: bool = False
    save_prefix: str = None

    default_error_messages = {
        "invalid": "Not a valid file."
    }

    def set_max_size_kb(self, size: int) -> "FileField":
        self.max_size_kb = size
        return self

    def set_allowed_extension(self, extension: list) -> "FileField":
        self.allowed_extensions = extension
        return self

    def allow_multiple(self) -> "FileField":
        self.is_multiple = True
        return self

    def allow_string_name(self) -> "FileField":
        self.is_string_name = True
        return self

    def set_save_prefix(self, prefix: str) -> "FileField":
        self.save_prefix = prefix
        return self

    def _deserialize(self, value, attr, data, **kwargs) -> typing.Any:
        if self.is_multiple and isinstance(value, list):
            for file in value:
                if not isinstance(file, FileStorage) and not self.is_string_name:
                    raise self.make_error("invalid")
            return value

        if not isinstance(value, FileStorage) and not self.is_string_name:
            raise self.make_error("invalid")
        return value


class CustomNestedField(fields.Nested):

    def _deserialize(self, value, attr, data, partial=None, **kwargs):
        return value


class BaseEnum(enum.Enum):

    @classmethod
    def values(cls) -> list:
        return list(map(lambda c: c.value, cls))

    @classmethod
    def keys(cls) -> list:
        return list(map(lambda c: c.name, cls))

    @classmethod
    def to_map(cls) -> dict:
        data = {}
        for enum_type in cls:
            data[enum_type.name] = enum_type.value
        return data

    @classmethod
    def value_to_key(cls, value):
        for enum_type in cls:
            if enum_type.value == value:
                return enum_type.name
        return None

    def __str__(self):
        return self.value

    def is_pf_enum(self):
        return True


def validate_enum_value(values: list, value: str, key: str, message: str = "Value should be any of "):
    if value not in values:
        message += '(' + ', '.join(values) + ')'
        raise ValidationError(message, key)


class EnumField(fields.String):
    enumType: BaseEnum

    def __init__(self, enumType, *args, **kwargs):
        self.enumType = enumType
        super(EnumField, self).__init__(*args, **kwargs)

    def _serialize(self, value, attr, obj, **kwargs):
        if isinstance(value, enum.Enum):
            return value.value
        return value

    def _deserialize(self, value, attr, data, **kwargs):
        if hasattr(self.enumType, 'is_pf_enum'):
            validate_enum_value(self.enumType.values(), data[attr], attr)
        name = self.enumType.value_to_key(data[attr])
        return self.enumType[name]

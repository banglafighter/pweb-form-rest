from dataclasses import dataclass
from ppy_common import DataUtil
from pweb_form_rest import PWebDataDTO


@dataclass(kw_only=True)
class DTODefinitionData:
    name: str
    isRequired: bool = False
    exlImport: bool = False


class RestSchemaUtil:

    @staticmethod
    def get_dto_definition(dto: PWebDataDTO) -> dict[str, DTODefinitionData]:
        response: dict = {}
        if dto and dto.declared_fields:

            for field in dto.declared_fields:
                field_data = DataUtil.get_dict_value(data=dto.declared_fields, key=field)
                if not field_data:
                    continue
                definition = DTODefinitionData(name=field)
                definition.isRequired = field_data.required
                metadata = field_data.metadata
                if metadata:
                    definition.exlImport = DataUtil.get_dict_value(data=metadata, key="exlImport", default=False)
                response[field] = definition

        return response

from pweb_form_rest.crud.pweb_crud_common import PWebCRUDCommon
from pweb_form_rest.form.pweb_form import PWebForm
from pweb_form_rest.ui.pweb_ui_helper import PWebSSRUIHelper, ssr_ui_render
from pweb_orm import PWebBaseModel


class FormDataCRUD(PWebCRUDCommon):
    ssr_ui_helper: PWebSSRUIHelper = None

    def __init__(self, model: PWebBaseModel, ssr_ui_helper: PWebSSRUIHelper = None):
        self.model = model
        self.ssr_ui_helper = ssr_ui_helper

    def render(self, view_name, params: dict = None, form: PWebForm = None):
        return ssr_ui_render(view_name=view_name, params=params, form=form, ssr_ui_helper=self.ssr_ui_helper)

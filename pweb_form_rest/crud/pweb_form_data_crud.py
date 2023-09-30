from flask import flash, redirect
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

    def create(self, view_name: str, form: PWebForm, redirect_url=None, data: dict = None, params=None, response_message: str = "Successfully created!"):
        if form.is_post_data() and form.is_valid_data(form_data=data):
            model = self.save(request_dto=form, data=form.get_request_data(form_data=data))
            flash(response_message, "success")
            if model and redirect_url:
                return redirect(redirect_url)
            if model:
                return model
        return self.render(view_name=view_name, form=form, params=params)

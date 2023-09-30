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

    def paginated_list(self, view_name, response_def: PWebForm = None, query=None, search_fields: list = None, sort_field=None, sort_order=None, item_per_page=None, params: dict = None):
        data_list = self.read_all(query=query, search_fields=search_fields, sort_field=sort_field, sort_order=sort_order, item_per_page=item_per_page)
        if response_def and data_list.items:
            data_list.items = response_def.dump(data_list.items, many=True)
        if not params:
            params = {}
        params.update({"table": data_list})
        return self.render(view_name=view_name, params=params)

    def list(self, view_name, response_def: PWebForm = None, query=None, search_fields: list = None, sort_field=None, sort_order=None, params: dict = None):
        data_list = self.read_all(query=query, search_fields=search_fields, sort_field=sort_field, sort_order=sort_order, enable_pagination=False)
        if response_def:
            data_list = response_def.dump(data_list.items, many=True)
        if not params:
            params = {}
        params.update({"table": data_list})
        return self.render(view_name=view_name, params=params)

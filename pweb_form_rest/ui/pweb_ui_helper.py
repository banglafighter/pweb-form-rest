import json
from flask import get_flashed_messages, render_template, render_template_string
from ppy_file_text import TextFileMan
from pweb_form_rest.common.pweb_fr_config import PWebFRConfig
from pweb_form_rest.crud.pweb_request_data import RequestData
from pweb_form_rest.form.pweb_form import PWebForm


class UIUtil:
    request_data: RequestData = RequestData()

    @property
    def pweb_flashed_messages(self):
        messages = get_flashed_messages(with_categories=True)
        response = {}
        for key, value in messages:
            response[key] = value
        return json.dumps(response)

    def base_url(self):
        info = self.request_data.get_url_info()
        return info.baseURL

    def set_base_js(self, obj_prefix="PWeb"):
        script = f"""
        <script>
            {obj_prefix}.baseURL = "{self.base_url()}"
        </script>
        """
        return script


class PWebSSRUIHelper:

    def get_helper(self) -> dict:
        return {}

    def _process_render_params(self, params: dict = None, form: PWebForm = None):
        if not params:
            params = {}

        if form and form.definition:
            params["form"] = form.definition

        helper = self.get_helper()
        if helper:
            params.update(helper)
        params["util"] = UIUtil()
        return params

    def render_html_file(self, file_path, params: dict = None, form: PWebForm = None, is_exception: bool = False):
        html = TextFileMan.get_text_from_file(file_path=file_path, is_exception=is_exception, exception_message="File Not found!", default="")
        params = self._process_render_params(params=params, form=form)
        return render_template_string(html, **params)

    def render(self, view_name, params: dict = None, form: PWebForm = None):
        params = self._process_render_params(params=params, form=form)
        return render_template(f"{view_name}.html", **params)


def _get_ssr_ui_helper(ssr_ui_helper: PWebSSRUIHelper = None):
    if not ssr_ui_helper:
        ssr_ui_helper = PWebSSRUIHelper()
        if PWebFRConfig.SSR_UI_HELPER and isinstance(PWebFRConfig.SSR_UI_HELPER, PWebSSRUIHelper):
            ssr_ui_helper = PWebFRConfig.SSR_UI_HELPER
    return ssr_ui_helper


def ssr_ui_render(view_name, params: dict = None, form: PWebForm = None, ssr_ui_helper: PWebSSRUIHelper = None):
    ssr_ui_helper = _get_ssr_ui_helper(ssr_ui_helper=ssr_ui_helper)
    return ssr_ui_helper.render(view_name=view_name, params=params, form=form)


def ssr_ui_render_html_file(file_path, params: dict = None, form: PWebForm = None, ssr_ui_helper: PWebSSRUIHelper = None, is_exception: bool = False):
    ssr_ui_helper = _get_ssr_ui_helper(ssr_ui_helper=ssr_ui_helper)
    return ssr_ui_helper.render_html_file(file_path=file_path, params=params, form=form, is_exception=is_exception)

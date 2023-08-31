import json
from flask import get_flashed_messages, render_template
from pweb_form_rest.crud.pweb_request_data import RequestData
from pweb_form_rest.form.pweb_form import PWebForm


class UIUtil:
    request_data: RequestData = RequestData()

    def get_status_message(self):
        messages = get_flashed_messages(with_categories=True)
        response = {}
        message_stack = ""
        for status, message in messages:
            if not status or not message:
                continue
            if status == "success":
                response["isSuccess"] = True
            elif "isSuccess" not in response:
                response["isSuccess"] = False

            if message:
                message_stack += message + " "

        if response and message_stack:
            response["message"] = message_stack.strip()
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

    @property
    def search_value(self):
        return self.request_data.get_query_args_value("search", "")


class PWebUIHelper:

    def get_helper(self) -> dict:
        return {}

    def render(self, name, params: dict = None, form: PWebForm = None):
        if form and form.definition:
            params["form"] = form.definition

        if not params:
            params = {}
        helper = self.get_helper()
        if helper:
            params.update(helper)
        params["util"] = UIUtil()
        return render_template(f"{name}.html", **params)

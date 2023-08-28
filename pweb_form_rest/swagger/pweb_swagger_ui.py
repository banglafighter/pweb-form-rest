from flask import Blueprint, render_template, request
from pweb_form_rest.common.pweb_fr_config import PWebFRConfig


class PWebSwaggerUI:
    _pweb_app = None

    def register(self, pweb_app):
        self._pweb_app = pweb_app

    def init_swagger_blueprint(self):
        if PWebFRConfig.ENABLE_SWAGGER_UI and self._pweb_app:
            blueprint = Blueprint(
                "PWebSwaggerSystem",
                __name__,
                template_folder="template-assets/templates",
                static_folder="template-assets/assets"
            )
            blueprint.add_url_rule(PWebFRConfig.SWAGGER_JSON_URL, "pweb-swagger-json", self.swagger_json)
            blueprint.add_url_rule(PWebFRConfig.SWAGGER_UI_URL, "pweb-swagger-ui", self.swagger_ui)
            self._pweb_app.register_blueprint(blueprint)

    def swagger_ui(self):
        auth = self.check_auth()
        if auth:
            return auth
        return render_template('pweb-swagger-ui.html', config=PWebFRConfig)

    def swagger_json(self):
        pass

    def check_auth(self):
        if PWebFRConfig.ENABLE_SWAGGER_AUTH:
            auth = request.authorization
            if not (auth and auth.username == PWebFRConfig.SWAGGER_AUTH_USERNAME and auth.password == PWebFRConfig.SWAGGER_AUTH_PASSWORD):
                return ('You are not authorize to access the URL.', 401, {
                    'WWW-Authenticate': 'Basic realm="Login Required"'
                })
        return None

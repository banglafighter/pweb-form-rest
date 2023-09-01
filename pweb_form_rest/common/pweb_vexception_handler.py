from pweb_form_rest.common.pweb_fr_config import PWebFRConfig
from pweb_form_rest.common.pweb_fr_exception import FormRESTException, form_rest_exception
from pweb_form_rest.crud.pweb_response_maker import PWebHTTPResponse


class ValidationExceptionHandler:
    pweb_http_response: PWebHTTPResponse = PWebHTTPResponse()

    def exception_response(self, exception: Exception):
        if isinstance(exception, FormRESTException):
            return self.get_exception_response_object(exception)

    def get_exception_response_object(self, exception: FormRESTException):
        if exception.messageResponse:
            json_string_response = exception.messageResponse.to_dict()
        elif exception.error_details_exception:
            json_string_response = exception.errorResponse.to_dict()
        elif exception.message:
            json_string_response = self.get_rest_message_response(exception.message)
        else:
            json_string_response = self.get_rest_message_response(PWebFRConfig.UNKNOWN_ERROR)
        return self.pweb_http_response.json_string_response(json_string_response)

    def get_rest_message_response(self, message: str):
        error_exception = self.get_rest_error_exception(message)
        return error_exception.messageResponse.to_dict()

    def get_rest_error_exception(self, message: str):
        return form_rest_exception.error_message_exception(message)

from ppy_common import PPyCException
from pweb_form_rest.data.pweb_response_data import PWebMessageResponse, PWebErrorResponse
from pweb_form_rest.data.pweb_response_status import PWebResponseCode, PWebHTTPCode


class FormRESTException(PPyCException):
    messageResponse: PWebMessageResponse
    errorResponse: PWebErrorResponse

    def __init__(self, message=None, exception_type: str = None):
        self._set_super(message, exception_type)

    def _set_super(self, message=None, exception_type: str = None):
        super().__init__(message, exception_type)

    def error_message_exception(self, message: str, code=PWebResponseCode.error, http_code=PWebHTTPCode.OK):
        self._set_super(message)
        response = PWebMessageResponse()
        response.message = message
        response.code = code
        response.status = PWebResponseCode.error
        response.http_code = http_code
        self.messageResponse = response
        return self

    def error_details_exception(self, message: str, details: dict, code=PWebResponseCode.error, http_code=PWebHTTPCode.OK):
        self._set_super(message)
        response = PWebErrorResponse()
        response.message = message
        response.code = code
        response.status = PWebResponseCode.error
        response.http_code = http_code
        response.error = details
        self.messageResponse = response
        return self

    def process_validation_exception(self, errors: dict, message: str):
        message_dict: dict = {}
        for message in errors:
            error_text = ""
            for text in errors[message]:
                error_text += str(text) + " "
            message_dict[message] = error_text
        return self.error_details_exception(message=message, details=message_dict)


form_rest_exception = FormRESTException()

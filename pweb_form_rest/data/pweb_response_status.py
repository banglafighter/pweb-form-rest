class PWebResponseStatus:
    success = "success"
    error = "error"


class PWebResponseCode:
    # SUCCESS Codes
    success = 2200

    # ERROR Codes
    error = 5100
    validation_error = 5101

    invalid_token_code = 5500
    token_expired_code = 5501
    token_error_code = 5502


class PWebHTTPCode:
    # SUCCESS Codes
    OK = 200

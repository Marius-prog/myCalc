def validate_number(number):
    error_message = ""
    if not number:
        error_message = "Number Form Field Required"

    if not number.isdigit():
        error_message = "Number should be digit"
    return error_message

from django.http import JsonResponse
import unicodedata


def convert_to_ascii(string):
    """
    Converts a string to ASCII characters.
    """
    if is_ascii(string):
        return string
    else:
        return ''.join(
            (c for c in unicodedata.normalize('NFD', string)
                if unicodedata.category(c) != 'Mn'))


def is_ascii(string):
    """
    Returns true if a string contains only ASCII characters.
    """
    return all(ord(char) < 128 for char in string)


def error_response(status_code, error_code, error_message):
    """
    Returns a formatted Json error response with status code.
    """
    return JsonResponse({
        'success': False,
        'error': {
            'message': error_message,
            'code': error_code
        }
    }, status=status_code)

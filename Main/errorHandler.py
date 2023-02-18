from django.http import JsonResponse


class CustomException(Exception):
    def __init__(self, message, status):
        self.message = message
        self.status = status

def errorHandler(message, code=400):
    return JsonResponse({"error": message}, status=code)

from django.http import JsonResponse


class CustomException(Exception):
    def __init__(self, message, status):
        self.message = message
        self.status = status


def errorHandler(message="Ошибка", code=400):
    return JsonResponse({"message": message}, status=code)

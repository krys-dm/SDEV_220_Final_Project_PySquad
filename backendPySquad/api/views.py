from django.http import JsonResponse


def get_message(request):
    return JsonResponse({"message": "Hello from Django backend!"})

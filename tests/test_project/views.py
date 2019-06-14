from django.http import HttpResponse


def my_view(request):
    return HttpResponse("my_view response OK")

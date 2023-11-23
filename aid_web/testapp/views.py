from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(["GET"])
def hello_rest_api(request):
    data = {"message": "Hello, REST API!"}
    return Response(data)

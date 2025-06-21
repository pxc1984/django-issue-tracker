from django.http import HttpRequest
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET', 'POST'])
def projects_view(request: HttpRequest) -> Response:
    if request.method == 'GET':
        ...
    else: # 'POST'
        ...


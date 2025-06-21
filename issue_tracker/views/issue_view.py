from django.http import HttpRequest
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET'])
def issue_view(request: HttpRequest, project_id: str, issue_id: int) -> Response:
    ...

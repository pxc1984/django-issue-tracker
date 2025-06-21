from django.http import HttpRequest
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET', 'POST'])
def projects_view(request: HttpRequest) -> Response:
    if request.method == 'GET':
        ...
    else: # 'POST'
        ...


@api_view(['GET', 'POST'])
def project_members_view(request: HttpRequest, project_id: str) -> Response:
    if request.method == 'GET':
        ...
    else: # 'POST'
        ...


@api_view(['GET', 'POST'])
def project_issues_view(request: HttpRequest, project_id: str) -> Response:
    if request.method == 'GET':
        ...
    else: # 'POST'
        ...


@api_view(['GET'])
def issue_view(request: HttpRequest, project_id: str, issue_id: int) -> Response:
    ...

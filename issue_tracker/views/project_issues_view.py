from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import *

from issue_tracker.models import ProjectPermission, Issue, IssueSerializer
from issue_tracker.services.validate_request import RequestValidator


@api_view(['GET', 'POST'])
def project_issues_view(request: Request, project_id: str) -> Response:
    if type(request.user) != User:
        return Response({'message': 'You can\'t access this resource as an anonymous user'}, status=HTTP_403_FORBIDDEN)
    if request.method == 'GET':
        return get_project_issues_view(request, project_id)
    else: # 'POST'
        return post_project_issues_view(request, project_id)

def get_project_issues_view(request: Request, project_id: str) -> Response:
    err = RequestValidator.validate_request_permissions(request, project_id, ProjectPermission.Read)
    if err:
        return err

    queryset = Issue.objects.filter(project__name=project_id)
    return Response({'data': IssueSerializer(queryset, many=True).data}, status=HTTP_200_OK)

def post_project_issues_view(request: Request, project_id: str) -> Response:
    return Response({'message': 'ok'}, status=HTTP_200_OK)

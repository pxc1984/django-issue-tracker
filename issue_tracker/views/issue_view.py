from django.contrib.auth.models import User
from django.http import HttpRequest
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import *

from issue_tracker.models import Project, ProjectMembership, ProjectPermission, Issue


@api_view(['GET'])
def issue_view(request: HttpRequest, project_id: str, issue_id: int) -> Response:
    if type(request.user) is not User:
        return Response(status=HTTP_403_FORBIDDEN)

    membership = ProjectMembership.objects.filter(user=request.user, project=project_id).first()
    if membership is None or not membership.role & ProjectPermission.Read.value:
        return Response(status=HTTP_403_FORBIDDEN)

    try:
        issue = Issue.objects.get(issue_id=issue_id, project=project_id)
    except Issue.DoesNotExist:
        return Response(status=HTTP_404_NOT_FOUND)

    return Response(issue.__repr__(), status=HTTP_200_OK)

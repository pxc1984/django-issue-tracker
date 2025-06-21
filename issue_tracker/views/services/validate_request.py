from django.contrib.auth.models import User
from django.http import HttpRequest
from rest_framework.response import Response
from rest_framework.status import *

from issue_tracker.models import ProjectPermission, ProjectMembership


class RequestValidator:
    @staticmethod
    def validate_issue_request(request: HttpRequest, project_id: str, target_permissions: ProjectPermission) -> Response | None:
        if type(request.user) is not User:
            return Response(status=HTTP_403_FORBIDDEN)

        membership = ProjectMembership.objects.filter(user=request.user, project=project_id).first()
        if membership is None or not membership.role & target_permissions.value:
            return Response(status=HTTP_403_FORBIDDEN)
        return None

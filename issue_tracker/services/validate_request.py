from dataclasses import dataclass
from django.contrib.auth.models import User
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import *

from issue_tracker.models import ProjectPermission, ProjectMembership, IssueStatus, IssuePriority
from issue_tracker.services.issue_validator import validate_in_enum


@dataclass
class IssueInfo:
    title: str
    description: str
    status: int
    priority: int

    @classmethod
    def parse_from_request(cls, request):
        title = request.data.get('title')
        if not title or not isinstance(title, str):
            return None, Response(data={'error': 'Title is required'}, status=HTTP_400_BAD_REQUEST)

        description = request.data.get('description', 'No description provided.')
        if not isinstance(description, str):
            return None, Response(data={'error': 'Description must be a string'}, status=HTTP_400_BAD_REQUEST)

        is_valid, status = validate_in_enum(request.data.get('status'), IssueStatus)
        if not is_valid:
            return None, Response(data={'error': 'Invalid issue status'}, status=HTTP_400_BAD_REQUEST)

        is_valid, priority = validate_in_enum(request.data.get('priority'), IssuePriority)
        if not is_valid:
            return None, Response(data={'error': 'Invalid issue priority'}, status=HTTP_400_BAD_REQUEST)

        cls.title = title
        cls.description = description
        cls.status = status
        cls.priority = priority

        return cls, None


class RequestValidator:
    @staticmethod
    def validate_request_permissions(request: Request, project_id: str, target_permissions: ProjectPermission) -> Response | None:
        if type(request.user) is not User:
            return Response(status=HTTP_403_FORBIDDEN)

        membership = ProjectMembership.objects.filter(user=request.user, project=project_id).first()
        if membership is None or not membership.role & target_permissions:
            return Response(status=HTTP_403_FORBIDDEN)
        return None

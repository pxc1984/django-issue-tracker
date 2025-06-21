from typing import Optional

from django.http import HttpRequest
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import *

from issue_tracker.models import ProjectPermission, Project, IssueStatus, Issue
from issue_tracker.views.services.validate_request import RequestValidator


def validate_issue_status(status_value: Optional[str]) -> tuple[bool, Optional[int]]:
    """
    Validates the issue status and converts it to integer format.
    Returns a tuple of (is_valid, status_value).
    """
    if not status_value:
        return False, None

    try:
        status_int = int(status_value)
        if not IssueStatus.is_valid_status(status_int):
            return False, None
        return True, status_int
    except ValueError:
        # Try parsing as enum string
        try:
            if status_value in IssueStatus.__members__:
                return True, IssueStatus[status_value].value
        except KeyError:
            pass
        return False, None


def validate_issue_priority(priority_value: Optional[str]) -> tuple[bool, Optional[int]]:
    """
    Validates the issue priority and converts it to integer format.
    Returns a tuple of (is_valid, priority_value).
    """
    if not priority_value:
        return True, 0  # Default priority

    try:
        priority_int = int(priority_value)
        if priority_int not in [0, 1, 2]:  # Valid priority values
            return False, None
        return True, priority_int
    except ValueError:
        return False, None


@api_view(['POST'])
def create_issue_view(request: HttpRequest, project_id: str) -> Response:
    err = RequestValidator.validate_issue_request(request, project_id, ProjectPermission.Write)
    if err is not None:
        return err

    title = request.POST.get('title')
    if not title:
        return Response(data={'error': 'Title is required'}, status=HTTP_400_BAD_REQUEST)

    description = request.POST.get('description', 'No description provided.')
    if not isinstance(description, str):
        return Response(data={'error': 'Description must be a string'}, status=HTTP_400_BAD_REQUEST)

    is_valid, status = validate_issue_status(request.POST.get('status'))
    if not is_valid:
        return Response(data={'error': 'Invalid issue status'}, status=HTTP_400_BAD_REQUEST)

    is_valid, priority = validate_issue_priority(request.POST.get('priority'))
    if not is_valid:
        return Response(data={'error': 'Invalid issue priority'}, status=HTTP_400_BAD_REQUEST)

    try:
        project = Project.objects.get(name=project_id)

        # Get the next issue_id for this project
        latest_issue = Issue.objects.filter(project=project).order_by('-issue_id').first()
        next_issue_id = (latest_issue.issue_id + 1) if latest_issue else 1

        issue = Issue.objects.create(
            issue_id=next_issue_id,
            title=title,
            description=description,
            project=project,
            reporter=request.user,
            status=status,
            priority=priority
        )

        return Response(data=issue.__repr__(), status=HTTP_201_CREATED)

    except Project.DoesNotExist:
        return Response(data={'error': f'Project {project_id} not found'}, status=HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response(data={'error': str(e)}, status=HTTP_500_INTERNAL_SERVER_ERROR)

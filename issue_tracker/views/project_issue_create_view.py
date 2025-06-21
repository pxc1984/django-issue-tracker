from django.http import HttpRequest
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import *

from issue_tracker.models import ProjectPermission, Project, IssueStatus, Issue, IssuePriority
from issue_tracker.services.issue_validator import validate_in_enum
from issue_tracker.services.validate_request import RequestValidator


@api_view(['POST'])
def create_issue_view(request: HttpRequest, project_id: str) -> Response:
    err = RequestValidator.validate_issue_request(request, project_id, ProjectPermission.Write)
    if err is not None:
        return err

    title = request.POST.get('title')
    if not title or not isinstance(title, str):
        return Response(data={'error': 'Title is required'}, status=HTTP_400_BAD_REQUEST)

    description = request.POST.get('description', 'No description provided.')
    if not isinstance(description, str):
        return Response(data={'error': 'Description must be a string'}, status=HTTP_400_BAD_REQUEST)

    is_valid, status = validate_in_enum(request.POST.get('status'), IssueStatus)
    if not is_valid:
        return Response(data={'error': 'Invalid issue status'}, status=HTTP_400_BAD_REQUEST)

    is_valid, priority = validate_in_enum(request.POST.get('priority'), IssuePriority)
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

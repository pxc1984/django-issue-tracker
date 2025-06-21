from django.http import HttpRequest
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import *

from issue_tracker.models import ProjectPermission, Project, Issue
from issue_tracker.services.validate_request import RequestValidator, IssueInfo


@api_view(['POST'])
def create_issue_view(request: HttpRequest, project_id: str) -> Response:
    err = RequestValidator.validate_issue_request(request, project_id, ProjectPermission.Write)
    if err is not None:
        return err

    info, err = IssueInfo.parse_from_request(request)
    if err is not None:
        return err

    try:
        project = Project.objects.get(name=project_id)

        # Get the next issue_id for this project
        latest_issue = Issue.objects.filter(project=project).order_by('-issue_id').first()
        next_issue_id = (latest_issue.issue_id + 1) if latest_issue else 1

        issue = Issue.objects.create(
            issue_id=next_issue_id,
            title=info.title,
            description=info.description,
            project=project,
            reporter=request.user,
            status=info.status,
            priority=info.priority,
        )

        return Response(data=issue.__repr__(), status=HTTP_201_CREATED)

    except Project.DoesNotExist:
        return Response(data={'error': f'Project {project_id} not found'}, status=HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response(data={'error': str(e)}, status=HTTP_500_INTERNAL_SERVER_ERROR)

from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import *

from issue_tracker.models import Issue, ProjectPermission, IssueSerializer
from issue_tracker.services.validate_request import RequestValidator


@api_view(['GET'])
def issue_view(request: Request, project_id: str, issue_id: int) -> Response:
    err = RequestValidator.validate_request_permissions(request, project_id, ProjectPermission.Read)
    if err is not None:
        return err

    try:
        issue = Issue.objects.get(issue_id=issue_id, project=project_id)
    except Issue.DoesNotExist:
        return Response(status=HTTP_404_NOT_FOUND)

    return Response(IssueSerializer(issue).data, status=HTTP_200_OK)

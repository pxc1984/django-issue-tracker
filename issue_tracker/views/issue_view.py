from django.http import HttpRequest
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import *

from issue_tracker.models import Issue, ProjectPermission
from issue_tracker.services.validate_request import RequestValidator


@api_view(['GET'])
def issue_view(request: HttpRequest, project_id: str, issue_id: int) -> Response:
    err = RequestValidator.validate_issue_request(request, project_id, ProjectPermission.Read)
    if err is not None:
        return err

    try:
        issue = Issue.objects.get(issue_id=issue_id, project=project_id)
    except Issue.DoesNotExist:
        return Response(status=HTTP_404_NOT_FOUND)

    return Response(issue.__repr__(), status=HTTP_200_OK)

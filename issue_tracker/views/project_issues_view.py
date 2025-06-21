from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response



@api_view(['GET', 'POST'])
def project_issues_view(request: Request, project_id: str) -> Response:
    if request.method == 'GET':
        ...
    else: # 'POST'
        ...


from django.contrib.auth.models import User
from django.core.signals import request_started
from django.http import HttpRequest
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import *

from issue_tracker.models import Project


@api_view(['GET', 'POST', 'DELETE'])
def projects_view(request: HttpRequest) -> Response:
    """
    Веб-сервис, отвечающий за взаимодействие с проектами.

        GET -> должен выводить все созданные проекты.
        POST -> должен создавать новый проект.
        DELETE -> должен удалять указанный проект.

    :param request:
    :return:
    """
    if request.method == 'GET':
        return handle_get_projects_view(request)
    elif request.method == 'POST':
        return handle_create_projects_view(request)
    else: # DELETE
        return handle_delete_projects_view(request)


def handle_get_projects_view(request: HttpRequest) -> Response:
    projects_list = [project.__repr__() for project in Project.objects.all()]
    return Response({'data': projects_list}, status=HTTP_200_OK)


def handle_create_projects_view(request: HttpRequest) -> Response:
    ...

def handle_delete_projects_view(request: HttpRequest) -> Response:
    ...

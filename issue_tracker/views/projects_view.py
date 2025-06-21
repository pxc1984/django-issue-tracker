from django.contrib.auth.models import User
from django.core.signals import request_started
from django.http import HttpRequest
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import *

from issue_tracker.models import Project, ProjectMembership


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
    if type(request.user) != User:
        return Response({'message': 'You can\'t access this resource as an anonimous user'}, status=HTTP_403_FORBIDDEN)
    project_name = request.POST.get('name')
    if project_name is None:
        return Response({'message': 'Please provide project name'}, status=HTTP_400_BAD_REQUEST)
    if Project.objects.filter(name=project_name).exists():
        return Response({'message': 'This project name is already taken'}, status=HTTP_400_BAD_REQUEST)

    description = request.POST.get('description')
    if description is None:
        description = 'No description provided'

    project = Project.objects.create(
        name=project_name,
        description=description,
    )
    ProjectMembership.objects.create(
        user=request.user,
        project=project,
        role=2,
    )

    return Response({'message': 'created'}, status=HTTP_200_OK)


def handle_delete_projects_view(request: HttpRequest) -> Response:
    if type(request.user) != User:
        return Response({'message': 'You can\'t access this resource as an anonymous user'}, status=HTTP_403_FORBIDDEN)
    project_name = request.POST.get('name')
    if project_name is None:
        return Response({'message': 'Please provide project name'}, status=HTTP_400_BAD_REQUEST)
    project = Project.objects.filter(name=project_name).first()
    if project is None:
        return Response({'message': 'This project does not exist'}, status=HTTP_400_BAD_REQUEST)
    membership = ProjectMembership.objects.filter(
        user=request.user,
        project=project,
    ).first()
    if membership is None or membership.role != '2':
        return Response({'message': 'User doesn\'t have proper access rights'}, status=HTTP_403_FORBIDDEN)

    project.delete()

    return Response({'message': 'deleted'}, status=HTTP_200_OK)



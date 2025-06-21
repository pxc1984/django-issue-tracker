from django.contrib.auth.models import User
from django.http import HttpRequest
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import *

from issue_tracker.models import Project, ProjectMembership, ProjectPermission


@api_view(['GET', 'POST'])
def project_members_view(request: HttpRequest, project_id: str) -> Response:
    """
    Веб-сервис, отвечающий за работу с членами проекта.

        GET -> Вывести список людей и их привилегий в проекте, если у запрашивающего есть доступ на Read в проекте
        POST -> Изменить статус человека в проекте. Запрашивающий должен иметь право на Manage

    :param request:
    :param project_id:
    :return:
    """
    if type(request.user) != User:
        return Response({'message': 'You can\'t access this resource as an anonymous user'}, status=HTTP_403_FORBIDDEN)

    project = Project.objects.filter(name=project_id).first()
    if project is None:
        return Response({'message': 'This project does not exist'}, status=HTTP_400_BAD_REQUEST)
    membership = ProjectMembership.objects.filter(
        user=request.user,
        project=project,
    ).first()

    if request.method == 'GET':
        return get_project_members_view(request, project, membership)
    else: # 'POST'
        return edit_project_members_view(request, project, membership)

def get_project_members_view(request: HttpRequest, project: Project, membership: ProjectMembership) -> Response:
    if not membership or not membership.role & ProjectPermission.Read.value:
        return Response({'Not enough permissions to view this resource'}, status=HTTP_403_FORBIDDEN)

    members = [{'username': membership.user.username, 'roles': ProjectPermission(membership.role).name} for membership in ProjectMembership.objects.filter(project=project)]

    return Response({'data': members}, status=HTTP_200_OK)

def edit_project_members_view(request: HttpRequest, project: Project, membership: ProjectMembership) -> Response:
    if not membership or not membership.role & ProjectPermission.Manage.value:
        return Response({'Not enough permissions to edit this resource'}, status=HTTP_403_FORBIDDEN)

    raise NotImplementedError()

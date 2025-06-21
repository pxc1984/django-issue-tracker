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
        return get_project_members_view(project, membership)
    else: # 'POST'
        return edit_project_members_view(request, project, membership)

def get_project_members_view(project: Project, membership: ProjectMembership) -> Response:
    if not membership or not membership.role & ProjectPermission.Read:
        return Response({'Not enough permissions to view this resource'}, status=HTTP_403_FORBIDDEN)

    members = [{'username': membership.user.username, 'roles': ProjectPermission(membership.role).name} for membership in ProjectMembership.objects.filter(project=project)]

    return Response({'data': members}, status=HTTP_200_OK)

def edit_project_members_view(request: HttpRequest, project: Project, membership: ProjectMembership) -> Response:
    """
    Handles editing project membership details based on user permissions and request input.
    This view provides functionality to add a new member to a project or update the role
    of an existing member. It verifies whether the user making the request has sufficient
    permissions and ensures that valid input is provided for the target username and role.

    :param request: The HTTP request object, containing user details, POST data, and other
                    metadata required for processing the membership changes
    :type request: HttpRequest
    :param project: The project instance for which the membership changes are being made
    :type project: Project
    :param membership: The current user's membership in the project, used to verify if
                       the user holds sufficient permissions to edit memberships
    :type membership: ProjectMembership
    :return: A Response object indicating the success or failure of the membership edit
             operation, with an appropriate HTTP status code and a descriptive message
    :rtype: Response
    """
    if not membership or not membership.role & ProjectPermission.Manage:
        return Response({'Not enough permissions to edit this resource'}, status=HTTP_403_FORBIDDEN)

    username = request.POST.get('username')
    if username is None or type(username) != str:
        return Response({'message': 'Please provide a valid target`s username'}, status=HTTP_400_BAD_REQUEST)
    target_user = User.objects.filter(
        username=username,
    ).first()
    if target_user is None:
        return Response({'message': 'Specified user does not exist'}, status=HTTP_400_BAD_REQUEST)

    role = request.POST.get('role')
    if role is None:
        return Response({'message': 'Please provide desired role'}, status=HTTP_400_BAD_REQUEST)

    target_membership = ProjectMembership.objects.filter(
        user__username=username,
        project=project,
    ).first()
    if target_membership is None:
        # Create a new membership
        ProjectMembership.objects.create(
            user=target_user,
            project=project,
            role=role,
        )
    else:
        # Edit current
        target_membership.role = role
        target_membership.save()

    return Response({'message': 'ok'}, status=HTTP_200_OK)

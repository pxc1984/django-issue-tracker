from django.urls import path

from issue_tracker.views.issue_view import issue_view
from issue_tracker.views.project_issue_create_view import create_issue_view
from issue_tracker.views.project_issues_view import project_issues_view
from issue_tracker.views.project_members_view import project_members_view
from issue_tracker.views.projects_view import projects_view

urlpatterns = [
    path('projects/', projects_view, name='projects view'),
    path('projects/<str:project_id>/members/', project_members_view, name='project members view'),
    path('projects/<str:project_id>/issues/', project_issues_view, name='project issues view'),
    path('projects/<str:project_id>/issue/<int:issue_id>/', issue_view, name='issue view'),
    path('projects/<str:project_id>/issues/new/', create_issue_view, name='create issue'),
]

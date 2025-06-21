from django.urls import path

from issue_tracker.views import projects_view, project_members_view, project_issues_view, issue_view

urlpatterns = [
    path('projects/', projects_view, name='projects view'),
    path('projects/<str:project_id>/members/', project_members_view, name='project members view'),
    path('projects/<str:project_id>/issues/', project_issues_view, name='project issues view'),
    path('projects/<str:project_id>/issue/<int:issue_id>/', issue_view, name='issue view'),
]

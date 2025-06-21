from enum import Enum

from django.contrib.auth.models import User
from django.db import models


class Project(models.Model):
    name = models.CharField(max_length=63, unique=True, primary_key=True)
    description = models.TextField(max_length=255, default='No description provided')
    creation_date = models.DateTimeField(auto_now_add=True)

    def __repr__(self):
        return {
            'name': self.name,
            'description': self.description,
        }

    class Meta:
        db_table = 'projects'
        verbose_name = 'Project'
        verbose_name_plural = 'Projects'


class IssueStatus(Enum):
    OPEN = 0
    NOT_PLANNED = 1
    CLOSED = 2

class IssuePriority(Enum):
    LOW = 0
    MEDIUM = 1
    HIGH = 2

class Issue(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=1023)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    reporter = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.SmallIntegerField(default=0)
    priority = models.SmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'issues'
        verbose_name = 'Issue'
        verbose_name_plural = 'Issues'

class Assignment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)

    class Meta:
        db_table = 'assignments'
        verbose_name = 'Assignment'
        verbose_name_plural = 'Assignments'


class ProjectPermission(Enum):
    Null = 0
    Read = 1
    Write = 2
    ReadWrite = 3
    Manage = 4
    Owner = 7

class ProjectMembership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    role = models.SmallIntegerField(default=0)

    class Meta:
        db_table = 'memberships'
        verbose_name = 'Project membership'
        verbose_name_plural = 'Project memberships'

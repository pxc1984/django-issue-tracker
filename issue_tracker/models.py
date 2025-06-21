import enum

from django.contrib.auth.models import User
from django.db import models
from rest_framework import serializers


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


class IssueStatus(enum.Enum):
    OPEN = 0
    NOT_PLANNED = 1
    CLOSED = 2

    @classmethod
    def is_valid(cls, n: int):
        return n in [member.value for member in cls]


class IssuePriority(enum.Enum):
    LOW = 0
    MEDIUM = 1
    HIGH = 2

    @classmethod
    def is_valid(cls, n: int):
        return n in [member.value for member in cls]


class Issue(models.Model):
    issue_id = models.IntegerField()
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=1023, default='No description provided.')
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
        unique_together = ('project', 'issue_id')

class IssueSerializer(serializers.ModelSerializer):
    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all())
    reporter = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Issue
        fields = [
            'issue_id',
            'title',
            'description',
            'project',
            'reporter',
            'status',
            'priority',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['created_at', 'updated_at']


class Assignment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)

    class Meta:
        db_table = 'assignments'
        verbose_name = 'Assignment'
        verbose_name_plural = 'Assignments'


class ProjectPermission(enum.IntFlag):
    Null = 0
    Read = 1
    Write = 2
    Manage = 4

class ProjectMembership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    role = models.SmallIntegerField(default=0)

    class Meta:
        db_table = 'memberships'
        verbose_name = 'Project membership'
        verbose_name_plural = 'Project memberships'

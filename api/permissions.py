# from .models import Project
from rest_framework import permissions
# from rest_framework.permissions import BasePermission

from api.models import Project, Contributor

# To implement a custom permission, override BasePermission and implement either, or both, of the following methods:
#   .has_permission(self, request, view)
#   .has_object_permission(self, request, view, obj)


class ProjectPermissions(permissions.BasePermission):
    # Custom permissions:

    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        # SAFE_METHODS: tuple contenant 'GET' , 'OPTIONS' et 'HEAD'
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user == obj.author


class ContributorPermissions(permissions.BasePermission):

    def has_permission(self, request, view):
        project = Project.objects.get(id=view.kwargs['project_pk'])

        user_project = Project.objects.filter(contributors__user=request.user)
        if project in user_project:
            project = Project.objects.get(id=view.kwargs['project_pk'])
            if request.method in permissions.SAFE_METHODS:
                return True
            return request.user == project.author
        return False

    def has_object_permission(self, request, view, obj):
        project = Project.objects.get(id=view.kwargs['project_pk'])
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user == project.author


class IssuePermissions(permissions.BasePermission):

    def has_permission(self, request, view):
        project = Project.objects.get(id=view.kwargs['project_pk'])
        usr_projects = Project.objects.filter(contributors__user=request.user)
        if project in usr_projects:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user == obj.author


class CommentPermissions(permissions.BasePermission):

    def has_permission(self, request, view):
        project = Project.objects.get(id=view.kwargs['project_pk'])
        usr_projects = Project.objects.filter(contributors__user=request.user)
        if project in usr_projects:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user == obj.author
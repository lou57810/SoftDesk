# from .models import Project
from rest_framework import permissions
# from rest_framework.permissions import BasePermission
from django.core.exceptions import ObjectDoesNotExist
from api import models
from api.models import Project, Contributor
from django.db.models import Q




# To implement a custom permission, override BasePermission and implement either, or both, of the following methods:
#   .has_permission(self, request, view)
#   .has_object_permission(self, request, view, obj)


class IsAuthor(permissions.BasePermission):
    def is_author(self, pk, user):
        try:
            content = models.Project.objects.get(pk=pk)

        except ObjectDoesNotExist:
            return False
        return content.author == user

class IsContributor(permissions.BasePermission):
    def is_contributor(self, project, user):
        try:
            models.Contributor.objects.get(user=user, project=project)
            # print('content2:', models.Contributor.objects.get(user=user, project=project))
        except ObjectDoesNotExist:
            return False

        return True

class IsContributorOrAuthorProject(IsContributor, IsAuthor):

    def has_permission(self, request, view):
        if view.action == "create":
            return True
        if view.action in ("destroy", "update"):
            return self.is_author(view.kwargs["pk"], request.user)
        if "pk" not in view.kwargs:         # view.kwargs dictionnaire vide.
            return True
        return self.is_contributor(view.kwargs["pk"], request.user) or self.is_author(view.kwargs["pk"], request.user)

class IsProjectContributor(IsContributor, IsAuthor):

    def has_permission(self, request, view):
        print('logged:', request.user) # => user1 (user login)
        print('proj_id:', view.kwargs)  # => {'projects_pk': '21'}
        print('projects:', Project.objects.filter(author_id=request.user))
        project = Project.objects.filter(id=view.kwargs['projects_pk'])
        print('project:', project, project[0])
        projects = Project.objects.filter(author_id=request.user)

        print('project_user:', projects)
        print('project[0]:', project[0])


        if view.action in ("create", "destroy", "update"):
            return self.is_author(view.kwargs["projects_pk"], request.user)

        return self.is_contributor(view.kwargs["projects_pk"], request.user) or self.is_author(view.kwargs["projects_pk"], request.user)

        # if "pk" not in view.kwargs:  # view.kwargs dictionnaire vide.
        #   return True


class IsIssueContributor(IsContributor, IsAuthor):

    def has_permission(self, request, view):
        user = request.user
        project = Project.objects.get(id=view.kwargs['projects_pk'])
        if view.action in "list":
            return self.is_contributor(view.kwargs["projects_pk"], request.user) or self.is_author(
                view.kwargs["projects_pk"], request.user)

        if view.action in ("create", "destroy", "update"):
            for contributor in Contributor.objects.filter(project_id=project.id):
                if user == contributor.user_id:
                    return True
                return self.is_contributor(view.kwargs["projects_pk"], contributor.user)


class IsCommentAuthorOrContributor(IsAuthor, IsContributor):

    def has_permission(self, request, view):
        if view.action == "list":
            return self.is_issue_contributor_or_author(request.user, view.kwargs["pk"])
        if view.action in ("destroy", "update"):
            # return self.is_author(view.kwargs["pk"], request.user)
            # return self.is_contributor(request.user, view.kwargs["pk"]) or self.is_author(
            # view.kwargs["pk"], request.user)
            return True

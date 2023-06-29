# from .models import Project
from rest_framework import permissions
# from rest_framework.permissions import BasePermission
from django.core.exceptions import ObjectDoesNotExist
from api import models
from api.models import Project, Contributor



# To implement a custom permission, override BasePermission and implement either, or both, of the following methods:
#   .has_permission(self, request, view)
#   .has_object_permission(self, request, view, obj)


class IsAuthor(permissions.BasePermission):
    def is_author(self, pk, user):
        try:
            content = models.Project.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return False

        return content.author_id == user


class IsContributor(permissions.BasePermission):
    def is_contributor(self, pk, user):
        try:
            content = models.Project.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return False

        return content.contributors  # _user_id == user       # contributor_user_id


class IsContributorOrAuthorProject(IsContributor, IsAuthor):

    def has_permission(self, request, view):
        print('test_view:', view.kwargs)
        if view.action == "create":
            return True
        if view.action in ("destroy", "update"):
            return self.is_author(view.kwargs["pk"], request.user)
        if "pk" not in view.kwargs:         # view.kwargs dictionnaire vide.
            return True
        return self.is_contributor(view.kwargs["pk"], request.user) or self.is_author(view.kwargs["pk"], request.user)


"""
def check_contributor(user, project):
    for contributor in Contributor.objects.filter(project_id=project.id):
        if user == contributor.user_id:
            return True
    return False
"""


class IsProjectContributor(IsContributor, IsAuthor):

    def has_permission(self, request, view):
        if view.action == "create":
            return True
        if view.action in ("destroy", "update"):

            # print('current:', view.kwargs["projects_pk"])
            # print('request:', request.user.id, request.user, view.kwargs["pk"], self.is_contributor(view.kwargs["pk"], request.user))
            # print('request2:', view.kwargs["pk"], request.user.id)
            return self.is_author(view.kwargs["pk"], request.user)

        return self.is_contributor(view.kwargs["pk"], request.user.id) or self.is_author(view.kwargs["pk"],
                                                                                          request.user.id)
            # return True
            # return True



class IsIssueContributor(IsContributor):
    message = "You do not have permission to perform this action."

    def has_permissions(self, request, view):
        if view.action == "create":
            return True

        if view.action in ("destroy", "update"):
            # print('request_issue:', request.user, view.kwargs["pk"])
            # return self.is_issue_contributor_or_author(request.user, view.kwargs["pk"])
            return self.is_contributor(request.user, view.kwargs["pk"])


class IsCommentAuthorOrContributor(IsAuthor, IsContributor):

    def has_permissions(self, request, view, obj):
        if view.action == "create":
            return True
        if view.action in ("destroy", "update"):
            # return self.is_author(view.kwargs["pk"], request.user)
            # return self.is_contributor(request.user, view.kwargs["pk"]) or self.is_author(
            # view.kwargs["pk"], request.user)
            return True

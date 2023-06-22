# from .models import Project
from rest_framework import permissions
# from rest_framework.permissions import BasePermission

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

        return content.author_user_id == user


class IsContributor(permissions.BasePermission):
    def is_contributor(self, pk, user):
        try:
            content = models.Project.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return False

        return content.contributor_id == user       # contributor_user_id


class IsContributorOrAuthorProject(IsContributor, IsAuthor):
    message = "You don't have the rights to access this info."

    def has_permission(self, request, view):
        if view.action == "create":
            return True
        if view.action in ("destroy", "update"):
            return self.is_contributor(view.kwargs["pk"], request.user)
        return self.is_contributor(view.kwargs["pk"], request.user) or self.is_author(view.kwargs["pk"], request.user)
"""
def check_contributor(user, project):
    for contributor in Contributor.objects.filter(project_id=project.id):
        if user == contributor.user_id:
            return True
    return False
"""

class IsProjectContributor(IsContributorOrAuthorProject):
    def is_issue_contributor_or_author(self, pk, user):
        try:
            content = models.Project.objects.get(pk=pk)
            print('contents:', content)
        except ObjectDoesNotExist:
            return False

        return content.issue_id == user


class IsIssueContributor(IsProjectContributor):
    message = "You don't have the rights to access this info."

    def has_permissions(self, request, view):
        if view.action == "create":
            return True

        if view.action in ("destroy", "update"):
            # print('request:', request.user)
            return self.is_issue_contributor_or_author(request.user, view.kwargs["pk"])



class IsCommentAuthor(permissions.BasePermission):

    def is_comment_author(self, pk, user):
        try:
            content = models.Comment.object.get(pk=pk)
        except ObjectDoesNotExist:
            return False

        # return content.author_user_id == author_user_id
        return content.author_id == user


class IsCommentContributor(permissions.BasePermission):
    def is_comment_contributor(self, pk, user):
        try:
            content = models.Comment.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return False

        return content.contributor_id == user


class IsCommentAuthorOrContributor(IsCommentAuthor, IsCommentContributor):
    def has_object_permission(self, request, view, obj):
        if view.action == "create":
            return True
        if view.action in ("destroy", "update"):
            return self.is_comment_author(view.kwargs["pk"], request.user)
        return self.is_comment_contributor(request.user, view.kwargs["pk"]) or self.is_comment_author(view.kwargs["pk"], request.user)



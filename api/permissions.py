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

        return content.contributor_id == user


class IsContributorOrAuthorProjectInProjectView(IsContributor, IsAuthor):
    def has_permission(self, request, view):
        if view.action == "create":
            return True
        if view.action in ("destroy", "update"):
            return self.is_author(view.kwargs["pk"], request.user)
        return self.is_contributor(request.user, view.kwargs["pk"]) or self.is_author(view.kwargs["pk"], request.user)

# Seuls les contributeurs sont autorisés
# à créer ou à consulter les problèmes
# d'un projet.(Auteur == Contributeur ??)
class IsIssueAuthor(IsContributor):
    def is_issue_author(self, pk, user):
        try:
            content = models.Issue.objects.get(pk=pk)
            print('pk:', pk)
        except ObjectDoesNotExist:
            return False

        return content.issue_id == user


class IsIssueContributor(IsIssueAuthor, IsContributor):
    def has_permissions(self, request, view):
        if view.action == "create":
            return True
        if view.action in ("destroy", "update"):
            return self.is_issue_author(view.kwargs["pk"], request.user)
        return self.is_contributor(request.user, view.kwargs["pk"]) and self.is_issue_author(view.kwargs["pk"], request.user)


class IsCommentAuthor(IsContributor):
    def is_comment_author(self, pk, user):
        try:
            content = models.Comment.object.get(pk=pk)
        except ObjectDoesNotExist:
            return False

        return content.comment_user_id == user


class IsCommentContributor(IsCommentAuthor, IsContributor):
    def has_permissions(self, request, view):
        if view.action == "create":
            return True
        if view.action in ("destroy", "update"):
            return self.is_comment_author(view.kwargs["pk"], request.user)
        return self.is_contributor(request.user, view.kwargs["pk"]) and self.is_comment_author(view.kwargs["pk"], request.user)
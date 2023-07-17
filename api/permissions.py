from rest_framework import permissions

from django.core.exceptions import ObjectDoesNotExist
from api import models



# To implement a custom permission, override BasePermission
# and implement either, or both, of the following methods:
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
            print('content2:', user, project)
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
        return self.is_contributor(view.kwargs["pk"], request.user) or\
            self.is_author(view.kwargs["pk"], request.user)


class IsProjectContributor(IsContributor, IsAuthor):

    def has_permission(self, request, view):

        if view.action in ("create", "destroy", "update"):
            return self.is_author(view.kwargs["projects_pk"], request.user)

        return self.is_contributor(view.kwargs["projects_pk"], request.user) or\
            self.is_author(view.kwargs["projects_pk"], request.user)


class IsIssueContributor(IsContributor, IsAuthor):

    def has_permission(self, request, view):
        if view.action in ("destroy", "update"):
            return self.is_author(
                view.kwargs["projects_pk"], request.user)
        return self.is_contributor(view.kwargs["projects_pk"], request.user) or\
            self.is_author(view.kwargs["projects_pk"], request.user)


class IsAuthorComment(permissions.BasePermission):
    def is_author_comment(self, pk, user):
        try:
            content = models.Comment.objects.get(pk=pk)

        except ObjectDoesNotExist:
            return False
        return content.author == user


class IsCommentAuthorOrContributor(IsContributor, IsAuthor, IsAuthorComment):

    def has_permission(self, request, view):

        if view.action in ("update", "destroy"):
            return self.is_author_comment(view.kwargs["pk"], request.user)

        return self.is_contributor(view.kwargs["projects_pk"], request.user)\
            or self.is_author(view.kwargs["projects_pk"], request.user)

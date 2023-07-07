from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated
from authentication.models import CustomUser
from .serializers import ContributorSerializer, ProjectsListSerializer,\
    ProjectsDetailSerializer, IssueSerializer, CommentSerializer

from django.db.models import Q
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from .models import Contributor, Project, Issue, Comment
from rest_framework import status
from django.contrib.auth import get_user_model
from .permissions import IsAuthor, IsContributor, IsContributorOrAuthorProject, \
    IsProjectContributor, IsIssueContributor, IsCommentAuthorOrContributor  # , ProjectPermissions, ContributorPermissions
# from .permissions import ProjectContributorReadOnly, ContributorReadOnly, \
    # AuthorFullAccess  # ProjectPermissions,

from django.db.models import Q


class ProjectsViewset(ModelViewSet):
    serializer_class = ProjectsListSerializer
    detail_serializer_class = ProjectsDetailSerializer
    permission_classes = [IsAuthenticated, IsContributorOrAuthorProject]

    def get_serializer_class(self):
        """ Return the serializer class for request """
        if self.action == "retrieve":
            return self.detail_serializer_class
        return super().get_serializer_class()

    def get_queryset(self):
        # Filtre sur l'utilisateur connecté
        user = self.request.user
        print('user, user.id:', user, user.id)
        # Affichage contrib + authors
        queryset = Project.objects.filter(Q(author_id=user.id) | Q(contributors__user=user.id))
        return queryset.distinct()      # Projets uniques

    def perform_create(self, serializer):
        """ Add a project for authenticated user """
        serializer.save(author=self.request.user)


class ContributorsViewset(ModelViewSet):

    serializer_class = ContributorSerializer
    permission_classes = [IsAuthenticated, IsProjectContributor]

    def get_queryset(self):
        return Contributor.objects.filter(project_id=self.kwargs['projects_pk'])

    def perform_create(self, serializer):
        project = get_object_or_404(Project, id=self.kwargs.get("projects_pk"))
        serializer.save(project=project)


class IssuesViewset(ModelViewSet):

    serializer_class = IssueSerializer
    permission_classes = [IsAuthenticated, IsIssueContributor]
    # detail_serializer_class = IssuesDetailSerializer

    def get_queryset(self):
        # print('user:', self.request.user)
        # print('project_id:', self.kwargs['project_pk'])
        return Issue.objects.filter(project_id=self.kwargs['projects_pk'])

    def perform_create(self, serializer):
        project = get_object_or_404(Project, pk=self.kwargs["projects_pk"])
        serializer.save(author=self.request.user, project=project)

    # def get_permissions(self):
        # pass


class CommentsViewset(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsCommentAuthorOrContributor]


    def get_queryset(self):
        user = self.request.user
        # queryset = Comment.objects.filter(author_id=user.id)
        print('users:', user.id)
        return Comment.objects.filter(issue=self.kwargs['issue_pk'])


    def perform_create(self, serializer):

        issue = get_object_or_404(Issue, pk=self.kwargs["issue_pk"])
        serializer.save(author=self.request.user, issue=issue)          # l'auteur est user connecté


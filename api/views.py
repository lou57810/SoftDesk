from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
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
    IsIssueContributor, IsCommentAuthor, IsCommentAuthorOrContributor  # , ProjectPermissions, ContributorPermissions
# from .permissions import ProjectContributorReadOnly, ContributorReadOnly, \
    # AuthorFullAccess  # ProjectPermissions,

from django.db.models import Q


class ProjectsViewset(ModelViewSet):
    serializer_class = ProjectsListSerializer
    detail_serializer_class = ProjectsDetailSerializer
    permissions_classes = [IsAuthenticated, IsContributorOrAuthorProject]

    def get_serializer_class(self):
        """ Return the serializer class for request """
        if self.action == "retrieve":
            return self.detail_serializer_class
        return super().get_serializer_class()

    def get_queryset(self):
        # Filtre sur l'utilisateur connecté
        user = self.request.user
        # print('Queryset:', Project.objects.filter(Q(author_id=user.id) | Q(contributors=user.id)))
        queryset = Project.objects.filter(Q(author_id=user.id) | Q(contributors=user.id))

        return queryset

    def perform_create(self, serializer):
        """ Add a project for authenticated user """
        serializer.save(author=self.request.user)


class ContributorsViewset(ModelViewSet):

    serializer_class = ContributorSerializer
    # permission_classes = [IsAuthenticated, ContributorPermissions]
    permission_classes = [IsAuthenticated, IsContributor]

    def get_queryset(self):
        return Contributor.objects.filter(project_id=self.kwargs["project_pk"])

    def perform_create(self, serializer):
        project = get_object_or_404(Project, pk=self.kwargs["project_pk"])
        serializer.save(project=project)


class IssuesViewset(ModelViewSet):

    serializer_class = IssueSerializer
    permission_classes = [IsAuthenticated, IsIssueContributor]
    # detail_serializer_class = IssuesDetailSerializer

    def get_queryset(self):
        print('user:', self.request.user)
        print('project_id:', self.kwargs['project_pk'])
        return Issue.objects.filter(project_id=self.kwargs['project_pk'])

    def perform_create(self, serializer):
        project = get_object_or_404(Project, pk=self.kwargs["project_pk"])
        serializer.save(author=self.request.user, project=project)

    # def get_permissions(self):
        # pass


class CommentsViewset(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsCommentAuthorOrContributor]


    def get_queryset(self):
        user = self.request.user
        queryset = Comment.objects.filter(author_id=user.id)
        print('users:', self.request.user)

        return Comment.objects.filter(issue=self.kwargs['issues_pk'])


    def perform_create(self, serializer):

        issue = get_object_or_404(Issue, pk=self.kwargs["issues_pk"])
        serializer.save(author=self.request.user, issue=issue)          # l'auteur est user connecté


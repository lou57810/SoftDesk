from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from .serializers import ContributorSerializer, ProjectsListSerializer,\
    ProjectsDetailSerializer, IssueSerializer, CommentSerializer

from django.db.models import Q
from rest_framework.viewsets import ModelViewSet
from .models import Contributor, Project, Issue, Comment

from .permissions import IsContributorOrAuthorProject, \
    IsProjectContributor, IsIssueContributor, IsCommentAuthorOrContributor  # ProjectPermissions,



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

    def get_queryset(self):
        return Issue.objects.filter(project_id=self.kwargs['projects_pk'])

    def perform_create(self, serializer):

        project = get_object_or_404(Project, pk=self.kwargs["projects_pk"])
        serializer.save(author=self.request.user, project=project)


class CommentsViewset(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsCommentAuthorOrContributor]

    def get_queryset(self):
        return Comment.objects.filter(issue=self.kwargs['issue_pk'])

    def perform_create(self, serializer):

        issue = get_object_or_404(Issue, pk=self.kwargs["issue_pk"])
        serializer.save(author=self.request.user, issue=issue)
        return True

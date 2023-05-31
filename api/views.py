from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from authentication.models import CustomUser
from .serializers import ContributorSerializer, ProjectsListSerializer,\
    ProjectsDetailSerializer, IssueSerializer, CommentSerializer

from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from .models import Contributor, Project, Issue, Comment
from rest_framework import status
from django.contrib.auth import get_user_model

from .permissions import ProjectContributorReadOnly, ContributorReadOnly, \
    AuthorFullAccess  # ProjectPermissions,

from django.db.models import Q




class ProjectsViewset(ModelViewSet):
    serializer_class = ProjectsListSerializer
    detail_serializer_class = ProjectsDetailSerializer
    permissions_classes = [IsAuthenticated]#, IsProjectAuthentication]

    def get_queryset(self):
        # return Project.objects.filter(contributors__user=request.user)
        return Project.objects.all()

    @action(detail=True, methods=['post'])
    def disable(self, request, pk):
        self.get_object().disable()
        return Response()

    def retrieve(self, request, *args, **kwargs):
        if Project.objects.get(id=kwargs['pk']):
            raw = Project.objects.get(id=kwargs['pk'])
            project = ProjectsDetailSerializer(raw, many=False)
            return Response(project.data, status=status.HTTP_200_OK)
    """
    def get(self, request):
        if request.user.is_authenticated:
            print("User is logged in :)")
            print(f"Username --> {request.user.username}")
        else:
            print("User is not logged in :(")
    

    def get_serializer_class(self):
    # Si l'action demandée est retrieve nous retournons le serializer de détail
        if self.action == 'retrieve':
            return self.detail_serializer_class
        return super().get_serializer_class()

    def perform_create(self, serializer):
        # Add a project for authenticated user
        serializer.save(author=self.request.user)
    
    def get_queryset(self):
        # Retrieve projects for authenticated user 

        # "Define Projects where current user is author or contributor"
        current_user = self.request.user
        current_user_contribution = Contributor.objects.filter(Q(author=self.request.user))
        contribution_projects_id = current_user_contribution.values("project").distinct()

        # "Retrieve only projects where current user is author or contributor"

        queryset = Project.objects.filter(
            Q(author=current_user) | Q(
                id__in=contribution_projects_id)).distinct().order_by('pk')

        return queryset
    
    

    def get_permissions(self):
        if self.request.method in ['PATCH', 'PUT', 'DELETE']:
            return [AuthorFullAccess()]
        return [ContributorReadOnly()]
    """


class ContributorsViewset(ModelViewSet):

    serializer_class = ContributorSerializer
    # detail_serializer_class = ContributorsDetailSerializer

    def get_queryset(self):
        return Contributor.objects.filter(
            project_id=self.kwargs['project_pk'])

    def perform_create(self, serializer):
        project = get_object_or_404(Project, pk=self.kwargs["project_pk"])
        serializer.save(project=project)


class IssuesViewset(ModelViewSet):

    serializer_class = IssueSerializer
    # detail_serializer_class = IssuesDetailSerializer

    def get_queryset(self):
        return Issue.objects.filter(
            project_id=self.kwargs['project_pk'])

    def perform_create(self, serializer):
        project = get_object_or_404(Project, pk=self.kwargs["project_pk"])
        serializer.save(author=self.request.user, project=project)

    """
    def get_comments(self, instance):
        # Le paramètre 'instance' est l'instance de la catégorie consultée.
        # Dans le cas d'une liste, cette méthode est appelée autant de fois qu'il y a
        # d'entités dans la liste

        # On applique le filtre sur notre queryset pour n'avoir que les produits actifs
        # queryset = instance.comments.filter(active=True)
        # Le serializer est créé avec le queryset défini et toujours défini en tant que many=True
        serializer = CommentsSerializer(queryset, many=True)
        # la propriété '.data' est le rendu de notre serializer que nous retournons ici
        return serializer.data
    """


class CommentsViewset(ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comment.objects.filter(issue=self.kwargs['issues_pk'])

    def perform_create(self, serializer):
        issue = get_object_or_404(Issue, pk=self.kwargs["issues_pk"])
        serializer.save(author=self.request.user, issue=issue)          # l'auteur est user connecté


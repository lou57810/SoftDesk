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
from .permissions import IsAuthor, IsContributorOrAuthorProjectInProjectView  # , ProjectPermissions, ContributorPermissions
# from .permissions import ProjectContributorReadOnly, ContributorReadOnly, \
    # AuthorFullAccess  # ProjectPermissions,

from django.db.models import Q


class ProjectsViewset(ModelViewSet):
    serializer_class = ProjectsListSerializer
    detail_serializer_class = ProjectsDetailSerializer
    permissions_classes = [IsAuthenticated, IsAuthor]

    def get_queryset(self):
        # return Project.objects.filter(contributors__user=request.user)
        # return Project.objects.filter(contributors__user=self.request.user)
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


class ContributorsViewset(ModelViewSet):

    serializer_class = ContributorSerializer
    # permission_classes = [IsAuthenticated, ContributorPermissions]
    permission_classes = [IsContributorOrAuthorProjectInProjectView]

    def get_queryset(self):
        return Contributor.objects.filter(
            project_id=self.kwargs['project_pk'])

    #contributors = Project.objects.filter(
        # Q(user=request.user) | Q(contributors__in=contributors_list)) #  .exclude(review__in=reviews)

    def create(self, project_pk=None):

        contributors_list = []
        data = request.data.copy()

        for object in Contributor.objects.filter(project_id=project_pk):
            contributors_list.append(object.user_id)

        if int(data['user']) in contributors_list:
            return Response(
                'User already added.', status=status.HTTP_400_BAD_REQUEST)

        else:
            data['project'] = project_pk
            data['role'] = 'Contributor'
            serialized_data = ContributorsSerializer(data=data)
            serialized_data.is_valid(raise_exception=True)
            serialized_data.save()

            return Response(
                serialized_data.data, status=status.HTTP_201_CREATED)




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


from rest_framework.serializers import ModelSerializer, StringRelatedField,\
    SerializerMethodField, SlugRelatedField, HyperlinkedIdentityField
from rest_framework import serializers


from .models import Contributor, Project, Issue, Comment
from authentication.models import CustomUser
from django.contrib.auth import get_user_model


class ContributorSerializer(serializers.ModelSerializer):
    user = SlugRelatedField(queryset=get_user_model().objects.all(),
                                   slug_field="username")
    project = StringRelatedField()

    class Meta:
        model = Contributor
        fields = ['pk', 'user', 'project', 'permission', 'role']


class ProjectsListSerializer(serializers.ModelSerializer):
    # author = serializers.StringRelatedField()   # Permet l'affichage de l'auteur / id
    # edit_url = HyperlinkedIdentityField(view_name="projects-detail")
    author = SlugRelatedField(queryset=get_user_model().objects.all(),
                              slug_field="username")

    class Meta:
        model = Project
        fields = ['pk', 'title', 'description', 'type', 'author']


class ProjectsDetailSerializer(serializers.ModelSerializer):
    # En utilisant un `SerializerMethodField', il est nécessaire d'écrire une méthode
    # nommée 'get_XXX' où XXX est le nom de l'attribut, ici 'contributors' et 'issues'.
    contributors = SerializerMethodField()
    issue = SerializerMethodField()
    author = StringRelatedField()

    class Meta:
        model = Project
        fields = ['pk', 'title', 'description', 'type', 'author', 'contributors', 'issue']

    def get_contributors(self, instance):
        queryset = instance.contributors.all()
        serializer = ContributorSerializer(queryset, many=True)
        return serializer.data

    def get_issue(self, instance):
        queryset = instance.issue.all()
        serializer = IssueSerializer(queryset, many=True)
        return serializer.data


class CommentSerializer(serializers.ModelSerializer):
    # author = SerializerMethodField()
    author = SlugRelatedField(queryset=get_user_model().objects.all(),
                              slug_field="username")
    issue = StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ['pk', 'description', 'author', 'issue', 'created_time']


class IssueSerializer(serializers.ModelSerializer):
    project = StringRelatedField()
    author = StringRelatedField()
    # author = StringRelatedField(read_only=True)
    comments = SerializerMethodField()
    assignee_user_id = SlugRelatedField(queryset=get_user_model().objects.all(),
                                        slug_field="username")

    class Meta:
        model = Issue
        fields = ['pk', 'title', 'desc', 'tag', 'priority', 'project', 'status',
                  'author', 'assignee_user_id', 'created_time', 'comments']

    def get_comments(self, instance):
        queryset = instance.comments.all()
        serializer = CommentSerializer(queryset, many=True)
        return serializer.data










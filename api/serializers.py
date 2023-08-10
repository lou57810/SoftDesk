from rest_framework.serializers import StringRelatedField,\
    SerializerMethodField, SlugRelatedField
from rest_framework import serializers


from .models import Contributor, Project, Issue, Comment
from django.contrib.auth import get_user_model


class ProjectsListSerializer(serializers.ModelSerializer):
    author = StringRelatedField()

    class Meta:
        model = Project
        fields = ['pk', 'title', 'description', 'type', 'author']


class ProjectsDetailSerializer(serializers.ModelSerializer):
    # En utilisant un `SerializerMethodField', il est nécessaire d'écrire une méthode
    # nommée 'get_XXX' où XXX est le nom de l'attribut, ici 'contributors' et 'issues'.
    contributors = SerializerMethodField()
    issues = SerializerMethodField()
    author = StringRelatedField()

    class Meta:
        model = Project
        fields = ['pk', 'title', 'description', 'type', 'author', 'contributors', 'issues']

    def get_contributors(self, instance):
        queryset = instance.contributors.all()
        serializer = ContributorSerializer(queryset, many=True)
        return serializer.data

    def get_issues(self, instance):
        queryset = instance.issue.all()
        serializer = IssueSerializer(queryset, many=True)
        return serializer.data


class ContributorSerializer(serializers.ModelSerializer):
    user = SlugRelatedField(queryset=get_user_model().objects.all(),
                            slug_field="username")
    project = StringRelatedField()

    class Meta:
        model = Contributor
        fields = ['pk', 'user', 'project', 'permission', 'role']


class IssueSerializer(serializers.ModelSerializer):
    project = StringRelatedField()
    author = StringRelatedField()

    comments = SerializerMethodField()
    assignee_user_id = SlugRelatedField(queryset=get_user_model().objects.all(),
                                        slug_field="username")

    class Meta:
        model = Issue
        fields = ['pk', 'title', 'desc', 'tag', 'priority', 'project',
                  'status', 'author', 'assignee_user_id', 'created_time', 'comments']

    def get_comments(self, instance):
        queryset = instance.comments.all()
        serializer = CommentSerializer(queryset, many=True)
        return serializer.data


class CommentSerializer(serializers.ModelSerializer):

    author = StringRelatedField(read_only=True)
    issue = StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ['pk', 'description', 'author', 'issue', 'created_time']

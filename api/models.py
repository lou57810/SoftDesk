from django.db import models, transaction
# from django.contrib.auth.models import User
# from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings


class Project(models.Model):
    title = models.CharField(max_length=128, blank=False, unique=True)
    description = models.CharField(max_length=1024)
    type = models.CharField(max_length=16, choices=[("Back-end", "Back-end"), ("Front-end", "Front-end"),
                                                    ("iOS", "iOS"), ("Android", "Android")])
    author = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def validate_title(self, value):
        if Project.objects.filter(name=value).exists():
            raise serializers.ValidationError('Project already exists')
        return value

    def __str__(self):
        return self.title


class Contributor(models.Model):
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE, related_name="contributors")
    permission = models.CharField(max_length=16, choices=[("Author", "Author"), ("Contributor", "Contributor")])
    role = models.CharField(max_length=128, choices=[("Developpeur Python", "Developpeur Python"),
                                                     ("UX-Designer", "UX-Designer"),
                                                     ("Administrateur Database", "Administrateur Database")])

    class Meta:
        unique_together = ['user', 'project']


class Issue(models.Model):
    title = models.CharField(max_length=128)
    desc = models.TextField(max_length=1024)
    tag = models.CharField(max_length=16, choices=[("Bug", "Bug"), ("Task", "Task"), ("Enhance", "Enhance")])
    priority = models.CharField(max_length=16, choices=[("High", "High"), ("Medium", "Medium"), ("Low", "Low"), ])

    project = models.ForeignKey(to=Project, on_delete=models.CASCADE, related_name='issue')

    status = models.CharField(max_length=16, choices=[("Todo", "Todo"),
                                                      ("In progress", "In progress"), ("Finished", "Finished"), ])
    author = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    assignee_user_id = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                         related_name='assignee_user_id')

    created_time = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.title


class Comment(models.Model):
    description = models.TextField(max_length=1024)
    author = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)  # author=user_login
    issue = models.ForeignKey(to=Issue, on_delete=models.CASCADE, related_name="comments")
    created_time = models.DateTimeField(auto_now_add=True)



from django.contrib import admin

from api.models import Project, Issue, Contributor, Comment

admin.site.register(Project)
admin.site.register(Issue)
admin.site.register(Contributor)
admin.site.register(Comment)

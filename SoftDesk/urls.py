"""
URL configuration for SoftDesk project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from api.views import ContributorsViewset, ProjectsViewset, IssuesViewset, CommentsViewset

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from authentication.views import MyObtainTokenPairView, RegisterView  # , UserList, UserDetail
from rest_framework import routers
from rest_framework_nested import routers


router = routers.SimpleRouter()

router.register('projects', ProjectsViewset, basename='projects')

project_router = routers.NestedSimpleRouter(router, 'projects', lookup='project')
project_router.register('users', ContributorsViewset, basename='contributors')
project_router.register('issues', IssuesViewset, basename='issues')
issue_router = routers.NestedSimpleRouter(project_router, 'issues', lookup='issues')
issue_router.register('comments', CommentsViewset, basename='comments')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('', include(router.urls)),
    path('', include(project_router.urls)),
    path('', include(issue_router.urls)),

    path('login/', MyObtainTokenPairView.as_view(), name='obtain_token'),
    path('login/refresh/', TokenRefreshView.as_view(), name='refresh_token'),
    path('signup/', RegisterView.as_view(), name='auth_register'),



]

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
from django.urls import re_path

from rest_framework_simplejwt.views import TokenObtainPairView  # , TokenRefreshView
# from authentication.views import MyObtainTokenPairView, RegisterView, LogoutPage
from authentication.views import RegisterView, LogoutPage
from rest_framework import routers
from rest_framework_nested import routers
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions


schema_view = get_schema_view(
   openapi.Info(
      title="SoftDesk API",
      default_version='v1',
      description="Project manager",
      # terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@mysite.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

"""
router = routers.SimpleRouter()
router.register('projects/', ProjectsViewset, basename='projects')

project_router = routers.NestedSimpleRouter(router, 'projects/', lookup='projects')
project_router.register('users/', ContributorsViewset, basename='contributors')

project_router.register('issues/', IssuesViewset, basename='issues')

issue_router = routers.NestedSimpleRouter(project_router, 'issues', lookup='issues')
issue_router.register('comments', CommentsViewset, basename='comments')
"""
router = routers.SimpleRouter()   # (trailing_slash=False)
router.register("projects", ProjectsViewset, basename="project")

projects_router = routers.NestedSimpleRouter(router, "projects", lookup="projects")
projects_router.register("users", ContributorsViewset, basename="project-users")
projects_router.register("issues", IssuesViewset, basename="project-issues")

issues_router = routers.NestedSimpleRouter(projects_router, "issues", lookup="issue")
issues_router.register('comments', CommentsViewset, basename="comments")


"""
comments_router = routers.NestedSimpleRouter(issues_router, r"issues/?", lookup="issues")
comments_router.register(r"comments/?", CommentsViewset, basename="comments")
"""


urlpatterns = [

    path('admin/', admin.site.urls),
    # path('api-auth/', include('rest_framework.urls')),  # Affiche login dans navbar rest_framework
    path("", include(router.urls)),
    path("", include(projects_router.urls)),
    path("", include(issues_router.urls)),

    path('login/', TokenObtainPairView.as_view(), name='obtain_token'),
    path('signup/', RegisterView.as_view(), name='auth_register'),
    path('logout/', LogoutPage.as_view(), name='logout'),

    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

]

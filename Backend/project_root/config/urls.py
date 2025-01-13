from django.contrib import admin
from django.urls import include, path
# from graphene_django.views import GraphQLView
from django.views.decorators.csrf import csrf_exempt
from apps.users.views import CustomTokenObtainPairView
from rest_framework_simplejwt.views import  TokenRefreshView 

urlpatterns = [
    path('api/admin/', admin.site.urls),  # Admin site
    path('api/users/', include('apps.users.urls')),  # Users API
    path('api/resumes/', include('apps.resumes.urls')),  # Resumes API
    path('api/jobs/', include('apps.jobs.urls')),  # Jobs API
    path('api/jobmatches/', include('apps.jobmatches.urls')),  # Job matches API

    # Authentication endpoints
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # GraphQL endpoint
    # path('graphql/', csrf_exempt(GraphQLView.as_view(graphiql=True))),  
] 

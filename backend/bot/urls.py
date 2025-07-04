from django.urls import path
from .views import BotView, UserGitHubProfileView, UserGitHubReposView

urlpatterns = [
    path('user', BotView.as_view(), name='user-bot-view'),
    path('profile', UserGitHubProfileView.as_view(), name='user-github-profile-view'),
    path('repos', UserGitHubReposView.as_view(), name='user-github-repos-view'),
]

from rest_framework.views import APIView
from core.utils.github_rapper import *
from user.models import User, GitHubTokern
from rest_framework.response import Response
from rest_framework import status


# Create your views here.

class BotView(APIView):
    """
    A simple view to handle bot-related requests.
    This can be extended with more functionality as needed.
    """

    def get(self, request):
        """
        Handle GET requests to the bot view.
        """
        user = request.user
        githubtoken = GitHubTokern.objects.filter(user=user).first()
        github_token = githubtoken.token if githubtoken else None

        auth = PersonalAccessTokenAuth(token=github_token)

        github_client = GitHubAPIWrapper(auth_strategy=auth)

        user_data = github_client.get_user()
        repo = github_client.get_repos()


        return Response({
            "message": "Hello, this is a bot view!",
            "user_data": user_data,
            "github_token": github_token,
            "repos": repo
        })


class UserGitHubProfileView(APIView):

    def get(self, request):
        """
        Handle GET requests to retrieve the user's GitHub profile.
        """
        user = request.user
        githubtoken = GitHubTokern.objects.filter(user=user).first()
        github_token = githubtoken.token if githubtoken else None

        if not github_token:
            return Response(
                {
                    "message": "GitHub token not found for the user.",
                    "user_data": None
                },
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            auth = PersonalAccessTokenAuth(token=github_token)
            github_client = GitHubAPIWrapper(auth_strategy=auth)
            user_data = github_client.get_user()

            if not user_data:
                return Response(
                    {
                        "message": "Failed to retrieve GitHub user data.",
                        "user_data": None
                    },
                    status=status.HTTP_502_BAD_GATEWAY
                )

            return Response(
                {
                    "message": "User GitHub profile retrieved successfully.",
                    "user_data": user_data
                },
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {
                    "message": f"An error occurred: {str(e)}",
                    "user_data": None
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class UserGitHubReposView(APIView):
    """
    View to handle requests for the user's GitHub repositories.
    """

    def get(self, request):
        """
        Handle GET requests to retrieve the user's GitHub repositories.
        """
        user = request.user
        githubtoken = GitHubTokern.objects.filter(user=user).first()
        github_token = githubtoken.token if githubtoken else None

        if not github_token:
            return Response(
                {"message": "GitHub token not found for the user."},
                status=status.HTTP_404_NOT_FOUND
            )

        auth = PersonalAccessTokenAuth(token=github_token)
        github_client = GitHubAPIWrapper(auth_strategy=auth)

        repos = github_client.get_repos()

        return Response(
            {"repos": repos},
            status=status.HTTP_200_OK
        )


class

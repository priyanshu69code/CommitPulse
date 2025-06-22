import os
import requests
from datetime import datetime, timedelta
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional

# --- Interfaces (Abstract Base Classes) for SOLID Principles ---

class GitHubAuth(ABC):
    """
    Abstract base class for GitHub authentication strategies.
    This promotes the Open/Closed Principle, allowing new auth methods
    to be added without modifying existing code.
    """
    @abstractmethod
    def get_headers(self) -> Dict[str, str]:
        """Returns the authentication headers for API requests."""
        pass

class GitHubUserFetcher(ABC):
    """
    Abstract base class for fetching user data.
    Separates the concern of user data retrieval (Interface Segregation).
    """
    @abstractmethod
    def get_user(self) -> Optional[Dict[str, Any]]:
        """Fetches the authenticated user's information."""
        pass

class GitHubCommitFetcher(ABC):
    """
    Abstract base class for fetching commit data.
    Separates the concern of commit retrieval (Interface Segregation).
    """
    @abstractmethod
    def get_recent_commits(self, repos: List[str], since: datetime) -> List[Dict[str, Any]]:
        """Fetches commits from a list of repositories since a given datetime."""
        pass


# --- Concrete Implementations ---

class PersonalAccessTokenAuth(GitHubAuth):
    """
    Implements GitHub authentication using a Personal Access Token (PAT).
    """
    def __init__(self, token: str):
        """
        Initializes the authentication handler with a GitHub PAT.

        Args:
            token: The Personal Access Token.
        """
        if not token:
            raise ValueError("GitHub Personal Access Token cannot be empty.")
        self._token = token

    def get_headers(self) -> Dict[str, str]:
        """
        Constructs the authorization headers for the GitHub API.

        Returns:
            A dictionary containing the authorization headers.
        """
        return {
            "Authorization": f"token {self._token}",
            "Accept": "application/vnd.github.v3+json"
        }


class GitHubAPIWrapper(GitHubUserFetcher, GitHubCommitFetcher):
    """
    A wrapper class for the GitHub API, handling user and commit data.
    This class depends on abstractions (GitHubAuth), not concrete implementations,
    adhering to the Dependency Inversion Principle.
    """
    BASE_URL = "https://api.github.com"

    def __init__(self, auth_strategy: GitHubAuth):
        """
        Initializes the GitHub API wrapper.

        Args:
            auth_strategy: An object providing authentication headers.
        """
        self.auth_strategy = auth_strategy
        self.session = requests.Session()
        self.session.headers.update(self.auth_strategy.get_headers())

    def get_user(self) -> Optional[Dict[str, Any]]:
        """
        Retrieves the authenticated user's details from the GitHub API.

        Returns:
            A dictionary containing user information, or None on failure.
        """
        try:
            response = self.session.get(f"{self.BASE_URL}/user")
            response.raise_for_status()  # Raises an HTTPError for bad responses
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching user from GitHub: {e}")
            return None

    def get_recent_commits(self, repos: List[str], since: datetime) -> List[Dict[str, Any]]:
        """
        Fetches all commits from the last 24 hours for a list of whitelisted repositories.

        Args:
            repos: A list of 'owner/repo' strings.
            since: A datetime object to fetch commits after this time.

        Returns:
            A list of commit data dictionaries.
        """
        since_iso = since.isoformat()
        all_commits = []

        user = self.get_user()
        if not user or 'login' not in user:
            print("Could not authenticate or fetch user login.")
            return []

        username = user['login']

        for repo_name in repos:
            print(f"Fetching commits for {repo_name}...")
            try:
                # The 'author' parameter filters commits by the commit author's GitHub login.
                params = {"since": since_iso, "author": username}
                url = f"{self.BASE_URL}/repos/{repo_name}/commits"

                response = self.session.get(url, params=params)
                response.raise_for_status()

                commits = response.json()
                all_commits.extend(commits)
                print(f"Found {len(commits)} new commits in {repo_name}.")

            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 404:
                    print(f"Repository not found: {repo_name}. Please check the name and your permissions.")
                else:
                    print(f"HTTP Error fetching commits for {repo_name}: {e}")
            except requests.exceptions.RequestException as e:
                print(f"An unexpected error occurred for repo {repo_name}: {e}")

        return all_commits

# --- Example Usage ---
if __name__ == '__main__':
    # --- Configuration ---
    # In a real application, use something like python-dotenv to load from a .env file
    # For this example, we get it from environment variables.
    # Make sure to set GITHUB_TOKEN in your environment.
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

    # A whitelist of repositories to check for commits.
    # Format: ["owner/repo_name", "another-owner/another-repo"]
    WHITELISTED_REPOS = [
        "google/gemini-api-python"
    ]

    if not GITHUB_TOKEN:
        print("Error: GITHUB_TOKEN environment variable not set.")
        print("Please set your GitHub Personal Access Token as an environment variable.")
    else:
        # --- Initialization ---
        # 1. Create an authentication strategy instance.
        auth = PersonalAccessTokenAuth(token=GITHUB_TOKEN)

        # 2. Inject the auth strategy into the API wrapper (Dependency Injection).
        github_client = GitHubAPIWrapper(auth_strategy=auth)

        # --- Execution ---
        # 1. Fetch user information
        current_user = github_client.get_user()
        if current_user:
            print(f"Successfully authenticated as: {current_user.get('login')}")

            # 2. Fetch commits from the last 24 hours
            twenty_four_hours_ago = datetime.utcnow() - timedelta(days=1)
            print(f"\nFetching commits since {twenty_four_hours_ago.strftime('%Y-%m-%d %H:%M:%S')} UTC...")

            recent_commits = github_client.get_recent_commits(
                repos=WHITELISTED_REPOS,
                since=twenty_four_hours_ago
            )

            # 3. Display results
            if recent_commits:
                print(f"\n--- Found {len(recent_commits)} total commits in the last 24 hours ---")
                for commit in recent_commits:
                    commit_data = commit.get('commit', {})
                    sha = commit.get('sha', 'N/A')[:7]
                    message = commit_data.get('message', 'No message').split('\n')[0]
                    author = commit_data.get('author', {}).get('name', 'N/A')
                    print(f"- [{sha}] {message} ({author})")
            else:
                print("\nNo new commits found in the whitelisted repositories in the last 24 hours.")
        else:
            print("\nCould not authenticate with GitHub. Please check your token.")

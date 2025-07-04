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

class GitHubRepoFetcher(ABC):
    """
    Abstract base class for fetching repository data.
    """
    @abstractmethod
    def get_repos(self, repo_type: str = 'owner') -> List[Dict[str, Any]]:
        """
        Fetches a list of repositories for the authenticated user.
        repo_type can be 'all', 'owner', 'member'.
        """
        pass

    @abstractmethod
    def get_repo_details(self, repo_name: str) -> Optional[Dict[str, Any]]:
        """Fetches detailed information for a specific repository."""
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

    @abstractmethod
    def get_commit_diff(self, repo_name: str, sha: str) -> Optional[str]:
        """Fetches the diff for a specific commit."""
        pass


# --- Concrete Implementations ---

class PersonalAccessTokenAuth(GitHubAuth):
    """
    Implements GitHub authentication using a Personal Access Token (PAT).
    """
    def __init__(self, token: str):
        if not token:
            raise ValueError("GitHub Personal Access Token cannot be empty.")
        self._token = token

    def get_headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"token {self._token}",
            "Accept": "application/vnd.github.v3+json"
        }


class GitHubAPIWrapper(GitHubUserFetcher, GitHubRepoFetcher, GitHubCommitFetcher):
    """
    An extended wrapper for the GitHub API.
    This class depends on abstractions (GitHubAuth), not concrete implementations,
    adhering to the Dependency Inversion Principle.
    """
    BASE_URL = "https://api.github.com"

    def __init__(self, auth_strategy: GitHubAuth):
        self.auth_strategy = auth_strategy
        self.session = requests.Session()
        self.session.headers.update(self.auth_strategy.get_headers())

    def _make_paginated_request(self, url: str, params: Optional[Dict] = None) -> List[Dict[str, Any]]:
        """Helper to handle paginated GitHub API responses."""
        results = []
        while url:
            try:
                response = self.session.get(url, params=params)
                response.raise_for_status()
                results.extend(response.json())

                # Check for next page link
                if 'next' in response.links:
                    url = response.links['next']['url']
                else:
                    url = None
                # Params are only needed for the first request
                params = None
            except requests.exceptions.RequestException as e:
                print(f"Error during paginated request for {url}: {e}")
                break
        return results

    def get_user(self) -> Optional[Dict[str, Any]]:
        """Retrieves the authenticated user's details."""
        try:
            response = self.session.get(f"{self.BASE_URL}/user")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching user from GitHub: {e}")
            return None

    def get_repos(self, repo_type: str = 'owner') -> List[Dict[str, Any]]:
        """
        Fetches all repositories for the authenticated user, handling pagination.

        Args:
            repo_type: Type of repos to fetch. Can be one of:
                       'all', 'owner', 'public', 'private', 'member'.
        """
        params = {'type': repo_type, 'per_page': 100}
        url = f"{self.BASE_URL}/user/repos"
        return self._make_paginated_request(url, params)

    def get_repo_details(self, repo_name: str) -> Optional[Dict[str, Any]]:
        """Fetches details for a single repository."""
        url = f"{self.BASE_URL}/repos/{repo_name}"
        try:
            response = self.session.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching details for repo {repo_name}: {e}")
            return None

    def get_recent_commits(self, repos: List[str], since: datetime) -> List[Dict[str, Any]]:
        """Fetches recent commits for a list of whitelisted repositories."""
        since_iso = since.isoformat()
        all_commits = []

        user = self.get_user()
        if not user or 'login' not in user:
            print("Could not authenticate or fetch user login.")
            return []

        username = user['login']

        for repo_name in repos:
            print(f"Fetching commits for {repo_name}...")
            params = {"since": since_iso, "author": username, "per_page": 100}
            url = f"{self.BASE_URL}/repos/{repo_name}/commits"

            try:
                response = self.session.get(url, params=params)
                response.raise_for_status()
                commits = response.json()
                # Add repo_name to each commit for context
                for commit in commits:
                    commit['repo_name'] = repo_name
                all_commits.extend(commits)
                print(f"Found {len(commits)} new commits in {repo_name}.")
            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 404:
                    print(f"Repository not found: {repo_name}.")
                else:
                    print(f"HTTP Error fetching commits for {repo_name}: {e}")
            except requests.exceptions.RequestException as e:
                print(f"An unexpected error occurred for repo {repo_name}: {e}")

        return all_commits

    def get_commit_diff(self, repo_name: str, sha: str) -> Optional[str]:
        """Retrieves the diff for a given commit SHA."""
        url = f"{self.BASE_URL}/repos/{repo_name}/commits/{sha}"
        # Request the diff format specifically
        headers = self.auth_strategy.get_headers()
        headers['Accept'] = 'application/vnd.github.v3.diff'

        try:
            response = self.session.get(url, headers=headers)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            print(f"Error fetching diff for commit {sha} in {repo_name}: {e}")
            return None

# --- Example Usage ---
if __name__ == '__main__':
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
    WHITELISTED_REPOS = [
        "google/gemini-api-python",
        "pallets/flask" # Example of another repo
    ]

    if not GITHUB_TOKEN:
        print("Error: GITHUB_TOKEN environment variable not set.")
    else:
        auth = PersonalAccessTokenAuth(token=GITHUB_TOKEN)
        github_client = GitHubAPIWrapper(auth_strategy=auth)

        current_user = github_client.get_user()
        if current_user:
            print(f"Successfully authenticated as: {current_user.get('login')}\n")

            # --- Utility 1: List Public and Private Repos ---
            print("--- Fetching Your Repositories ---")
            all_my_repos = github_client.get_repos(repo_type='owner')
            public_repos = [r['full_name'] for r in all_my_repos if not r['private']]
            private_repos = [r['full_name'] for r in all_my_repos if r['private']]

            print(f"Found {len(public_repos)} public repos.")
            print(f"Found {len(private_repos)} private repos.\n")

            # --- Utility 2: Get Recent Commits ---
            print("--- Fetching Recent Commits from Whitelist ---")
            twenty_four_hours_ago = datetime.utcnow() - timedelta(days=1)
            recent_commits = github_client.get_recent_commits(
                repos=WHITELISTED_REPOS,
                since=twenty_four_hours_ago
            )

            if recent_commits:
                print(f"\nFound {len(recent_commits)} total commits in the last 24 hours.\n")

                # --- Utility 3: Get Diff for the Latest Commit ---
                print("--- Fetching Diff for the Latest Commit ---")
                latest_commit = recent_commits[0]
                latest_commit_sha = latest_commit['sha']
                latest_commit_repo = latest_commit['repo_name']

                print(f"Repo: {latest_commit_repo}")
                print(f"SHA: {latest_commit_sha}")

                diff = github_client.get_commit_diff(latest_commit_repo, latest_commit_sha)

                if diff:
                    print("\n--- Commit Diff ---")
                    # Print first 15 lines of the diff
                    diff_lines = diff.strip().split('\n')
                    print('\n'.join(diff_lines[:15]))
                    if len(diff_lines) > 15:
                        print("... (diff truncated)")
                    print("--- End of Diff ---\n")

            else:
                print("\nNo new commits found in the whitelisted repositories.")
        else:
            print("\nCould not authenticate with GitHub. Please check your token.")

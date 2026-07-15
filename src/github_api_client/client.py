import requests
import logging
from typing import List, Dict, Any

from .exceptions import (
    GitHubAPIError,
    RepositoryNotFoundError,
    RateLimitError,
    AuthenticationError,
    ValidationError
)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class GitHubAPIClient:
    """Client for GitHub REST API with CRUD operations."""

    BASE_URL = "https://api.github.com"
    API_VERSION = "2026-03-10"

    def __init__(self, token: str, owner: str):
        """Initialize GitHub API client."""
        self.token = token
        self.owner = owner
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": self.API_VERSION
        }
        logging.info(f"GitHubAPIClient initialized for {owner}")

    def _handle_response(self, response, success_status: int = 200):
        """
        Handle API response and raise appropriate exceptions.

        Args:
            response: requests Response object
            success_status: Expected success status code

        Returns:
            Response data as dict

        Raises:
            Appropriate exception based on status code
        """
        status_code = response.status_code

        if status_code == success_status:
            return response.json() if response.text else {}

        # Handle errors
        if status_code == 401:
            raise AuthenticationError("Invalid or expired token")
        elif status_code == 403:
            # Check if it's rate limit
            if 'X-RateLimit-Remaining' in response.headers:
                remaining = int(response.headers['X-RateLimit-Remaining'])
                if remaining == 0:
                    raise RateLimitError("Rate limit exceeded. Please wait.")
            raise GitHubAPIError(f"Forbidden: {response.text}", status_code)
        elif status_code == 404:
            raise RepositoryNotFoundError(f"Repository not found, status_code")
        elif status_code == 422:
            error_data = response.json() if response.text else None
            raise ValidationError("Validation failed", status_code, error_data)
        else:
            error_data = response.json() if response.text else None
            raise GitHubAPIError(
                f"API error {status_code}: {response.text}",
                status_code,
                error_data
            )

    def create_repo(self, name: str, description: str = None, private: bool = True) -> Dict[str, Any]:
        """Create a new repository."""
        url = f"{self.BASE_URL}/user/repos"
        repo_data = {
            "name": name,
            "description": description,
            "private": private,
            "auto_init": True
        }
        logging.info(f"Creating repository: {name}")
        response = requests.post(url, headers=self.headers, json=repo_data)
        return self._handle_response(response, 201)

    def get_repo(self, name: str) -> Dict[str, Any]:
        """Get repository by name."""
        url = f"{self.BASE_URL}/repos/{self.owner}/{name}"
        logging.info(f"Getting repository: {name}")
        response = requests.get(url, headers=self.headers)
        return self._handle_response(response, 200)

    def update_repo(self, name: str, data: dict) -> Dict[str, Any]:
        """Update repository."""
        url = f"{self.BASE_URL}/repos/{self.owner}/{name}"
        logging.info(f"Updating repository: {name}")
        response = requests.patch(url, headers=self.headers, json=data)
        return self._handle_response(response, 200)

    def delete_repo(self, name: str) -> bool:
        """Delete repository."""
        # Check if repo exists first
        if not self.repo_exists(name):
            logging.warning(f"Repository '{name}' does not exist")
            return False

        url = f"{self.BASE_URL}/repos/{self.owner}/{name}"
        logging.info(f"Deleting repository: {name}")
        response = requests.delete(url, headers=self.headers)

        if response.status_code == 204:
            logging.info(f"Repository deleted: {name}")
            return True

        # Handle error
        self._handle_response(response, 204)
        return False

    def repo_exists(self, name: str) -> bool:
        """Check if repository exists."""
        url = f"{self.BASE_URL}/repos/{self.owner}/{name}"
        response = requests.get(url, headers=self.headers)
        return response.status_code == 200

    def get_all_repos(self, per_page: int = 30) -> List[Dict[str, Any]]:
        """
        Get all repositories for the authenticated user.

        Args:
            per_page: Number of repositories per page (max 100)

        Returns:
            List of repository dictionaries
        """
        all_repos = []
        page = 1

        while True:
            url = f"{self.BASE_URL}/user/repos"
            params = {
                "per_page": min(per_page, 100),
                "page": page,
                "sort": "created",
                "direction": "desc"
            }

            response = requests.get(url, headers=self.headers, params=params)
            repos = self._handle_response(response, 200)

            if not repos:  # Empty response — no more repos
                break

            all_repos.extend(repos)

            # If we got fewer than requested — this is the last page
            if len(repos) < per_page:
                break

            page += 1

        return all_repos

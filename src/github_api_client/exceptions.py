"""
Custom exceptions for GitHub API Client.
"""


class GitHubAPIError(Exception):
    """Base exception for GitHub API errors."""
    def __init__(self, message: str, status_code: int = None, response: dict = None):
        self.message = message
        self.status_code = status_code
        self.response = response
        super().__init__(message)


class RepositoryNotFoundError(GitHubAPIError):
    """Raised when a repository is not found."""
    def __init__(self, message: str = "Repository not found", status_code: int = 404):
        super().__init__(message, status_code)


class RateLimitError(GitHubAPIError):
    """Raised when rate limit is exceeded."""
    def __init__(self, message: str = "Rate limit exceeded", status_code: int = 403):
        super().__init__(message, status_code)


class AuthenticationError(GitHubAPIError):
    """Raised when authentication fails."""
    def __init__(self, message: str = "Authentication failed", status_code: int = 401):
        super().__init__(message, status_code)


class ValidationError(GitHubAPIError):
    """Raised when request validation fails."""
    def __init__(self, message: str = "Validation failed", status_code: int = 422, response: dict = None):
        super().__init__(message, status_code, response)

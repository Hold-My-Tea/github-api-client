from .client import GitHubAPIClient
from .exceptions import (
    GitHubAPIError,
    RepositoryNotFoundError,
    RateLimitError,
    AuthenticationError,
    ValidationError
)

__all__ = [
    'GitHubAPIClient',
    'GitHubAPIError',
    'RepositoryNotFoundError',
    'RateLimitError',
    'AuthenticationError',
    'ValidationError',
]
__version__ = '0.1.0'

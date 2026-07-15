import os
import pytest
import time
from dotenv import load_dotenv
from github_api_client import GitHubAPIClient


load_dotenv()

# Read configuration from environment
TOKEN = os.getenv('GITHUB_TOKEN')
OWNER = os.getenv('GITHUB_USERNAME', 'Hold-My-Tea')
WAIT_TIME = int(os.getenv('GITHUB_API_WAIT', '1'))


__all__ = [
    'github_wait_time',
    'client',
    'test_repo_name',
    'cleanup_repo',
]


@pytest.fixture(scope="session")
def github_wait_time():
    """Return configured wait time for GitHub API."""
    return WAIT_TIME


@pytest.fixture(scope="function")
def client():
    """Create GitHubAPIClient instance for testing."""
    if not TOKEN:
        pytest.skip("GITHUB_TOKEN not set in environment")
    return GitHubAPIClient(TOKEN, OWNER)


@pytest.fixture
def test_repo_name():
    """Generate unique test repository name."""
    return f"test-repo-{int(time.time())}"


@pytest.fixture
def cleanup_repo(client, test_repo_name, github_wait_time):
    """
        Automatically cleanup test repository after test execution.
        Handles cases where repository may have already been deleted.
        """
    yield test_repo_name
    try:
        time.sleep(github_wait_time)
        client.delete_repo(test_repo_name)
    except Exception as e:
        print(f"Cleanup warning: {e}")

"""
Test suite for GitHubAPIClient.
Contains both positive and negative test cases.
"""

import pytest
import time
import allure
from github_api_client import RepositoryNotFoundError, ValidationError


@allure.epic("GitHub API Client")
@allure.feature("Repository CRUD Operations")
class TestGitHubAPIClient:
    """Positive test cases for GitHubAPIClient."""

    @allure.story("Client Initialization")
    @allure.title("Initialize client with valid credentials")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.smoke
    @pytest.mark.positive
    def test_initialization(self, client):
        """Test client initialization with valid credentials."""
        with allure.step("Check client attributes"):
            assert client.owner is not None
            assert client.token is not None
            assert client.headers is not None

        with allure.step("Check authorization header"):
            assert 'Authorization' in client.headers
            assert client.headers['Authorization'] == f"Bearer {client.token}"

    @allure.story("Repository Creation")
    @allure.title("Create a new repository")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.positive
    def test_create_repo(self, client, test_repo_name, cleanup_repo):
        """Test repository creation with valid parameters."""
        with allure.step(f"Create repository '{test_repo_name}'"):
            repo = client.create_repo(
                test_repo_name,
                "Test repository for unit tests",
                private=True
            )

        with allure.step("Verify repository data"):
            assert repo['name'] == test_repo_name
            assert repo['private'] is True
            assert repo['description'] == "Test repository for unit tests"
            assert repo['id'] is not None
            assert repo['html_url'] is not None

            # Attach repository URL to report
            allure.attach(
                repo['html_url'],
                name="Repository URL",
                attachment_type=allure.attachment_type.TEXT
            )

    @allure.story("Repository Retrieval")
    @allure.title("Get repository by name")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.positive
    def test_get_repo(self, client, test_repo_name, cleanup_repo, github_wait_time):
        """Test retrieving a repository by name."""
        with allure.step(f"Create repository '{test_repo_name}'"):
            client.create_repo(test_repo_name, "Test repo for get")
            time.sleep(github_wait_time)

        with allure.step(f"Retrieve repository '{test_repo_name}'"):
            repo = client.get_repo(test_repo_name)

        with allure.step("Verify repository data"):
            assert repo['name'] == test_repo_name
            assert repo['owner']['login'] == client.owner
            assert repo['description'] == "Test repo for get"

    @allure.story("Repository Update")
    @allure.title("Update repository (description and visibility)")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.positive
    def test_update_repo(self, client, test_repo_name, cleanup_repo, github_wait_time):
        """Test full repository update (description and visibility)."""
        with allure.step(f"Create repository '{test_repo_name}'"):
            client.create_repo(test_repo_name, "Original description", private=True)
            time.sleep(github_wait_time)

        with allure.step("Update description and visibility"):
            updated = client.update_repo(
                test_repo_name,
                {
                    "description": "Updated description",
                    "private": False
                }
            )

        with allure.step("Verify updates"):
            assert updated['description'] == "Updated description"
            assert updated['private'] is False

    @allure.story("Repository Update")
    @allure.title("Partial update (only description)")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.positive
    def test_update_repo_partial(self, client, test_repo_name, cleanup_repo, github_wait_time):
        """Test partial repository update (only description field)."""
        with allure.step(f"Create repository '{test_repo_name}'"):
            client.create_repo(test_repo_name, "Original description", private=True)
            time.sleep(github_wait_time)

        with allure.step("Update only description"):
            updated = client.update_repo(
                test_repo_name,
                {"description": "Partial update"}
            )

        with allure.step("Verify only description changed"):
            assert updated['description'] == "Partial update"
            assert updated['private'] is True  # Should remain unchanged

    @allure.story("Repository Deletion")
    @allure.title("Delete repository")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.positive
    def test_delete_repo(self, client, test_repo_name, github_wait_time):
        """Test repository deletion."""
        with allure.step(f"Create repository '{test_repo_name}'"):
            client.create_repo(test_repo_name, "Test for delete")
            time.sleep(github_wait_time)

        with allure.step("Delete repository"):
            result = client.delete_repo(test_repo_name)
            assert result is True

        with allure.step("Verify deletion"):
            time.sleep(github_wait_time)
            assert client.repo_exists(test_repo_name) is False

    @allure.story("Repository Existence Check")
    @allure.title("Check if repository exists")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.positive
    def test_repo_exists(self, client, test_repo_name, cleanup_repo, github_wait_time):
        """Test checking repository existence."""
        with allure.step("Check non-existent repository"):
            assert client.repo_exists(test_repo_name) is False

        with allure.step(f"Create repository '{test_repo_name}'"):
            client.create_repo(test_repo_name, "Test for exists")
            time.sleep(github_wait_time)

        with allure.step("Check existing repository"):
            assert client.repo_exists(test_repo_name) is True

    @allure.story("Repository Listing")
    @allure.title("Get all repositories")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.positive
    def test_get_all_repos(self, client):
        """Test retrieving all repositories."""
        with allure.step("Get all repositories (limit 5)"):
            repos = client.get_all_repos(per_page=5)

        with allure.step("Verify response"):
            assert isinstance(repos, list)
            if repos:
                assert 'name' in repos[0]
                assert 'id' in repos[0]
                assert 'owner' in repos[0]
            else:
                allure.attach(
                    "No repositories found in account",
                    name="Info",
                    attachment_type=allure.attachment_type.TEXT
                )

    @allure.story("Repository Creation")
    @allure.title("Create multiple repositories")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.positive
    def test_create_multiple_repos(self, client, github_wait_time):
        """
        Test creating multiple repositories in sequence.
        Verifies that each repository is created successfully and cleanup works.
        """
        import random
        repo_names = []
        repo_count = 3
        base_timestamp = int(time.time())

        with allure.step(f"Create {repo_count} repositories"):
            for i in range(repo_count):
                name = f"test-repo-{base_timestamp}-{i}-{random.randint(1000, 9999)}"

                # ✅ Cleanup if exists
                if client.repo_exists(name):
                    client.delete_repo(name)
                    time.sleep(github_wait_time)

                repo_names.append(name)
                repo = client.create_repo(name, f"Test repo {i}", private=True)
                assert repo['name'] == name
                time.sleep(github_wait_time)

    @allure.story("Repository Deletion")
    @allure.title("Delete non-existent repository")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.positive
    def test_delete_nonexistent_repo(self, client):
        """Test deleting a non-existent repository returns False."""
        with allure.step("Attempt to delete non-existent repository"):
            result = client.delete_repo("nonexistent-repo-12345")

        with allure.step("Verify returns False"):
            assert result is False


@allure.epic("GitHub API Client")
@allure.feature("Error Handling")
class TestGitHubAPIClientErrors:
    """Negative test cases for error handling."""

    @allure.story("Error Handling")
    @allure.title("Get non-existent repository raises RepositoryNotFoundError")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.negative
    def test_get_nonexistent_repo(self, client):
        """Test retrieving non-existent repository raises RepositoryNotFoundError."""
        with allure.step("Attempt to get non-existent repository"):
            with pytest.raises(RepositoryNotFoundError):
                client.get_repo("nonexistent-repo-12345")

    @allure.story("Error Handling")
    @allure.title("Create repository with empty name raises ValidationError")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.negative
    def test_create_repo_empty_name(self, client):
        """Test creating repository with empty name raises ValidationError."""
        with allure.step("Attempt to create repository with empty name"):
            with pytest.raises(ValidationError):
                client.create_repo("")

    @allure.story("Error Handling")
    @allure.title("Create repository with too long name raises ValidationError")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.negative
    def test_create_repo_too_long(self, client):
        """Test creating repository with name exceeding 100 characters raises ValidationError."""
        long_name = "a" * 101  # GitHub max is 100 characters
        with allure.step(f"Attempt to create repository with {len(long_name)} characters"):
            with pytest.raises(ValidationError):
                client.create_repo(long_name)

    @allure.story("Error Handling")
    @allure.title("Update non-existent repository raises RepositoryNotFoundError")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.negative
    def test_update_repo_nonexistent(self, client):
        """Test updating non-existent repository raises RepositoryNotFoundError."""
        with allure.step("Attempt to update non-existent repository"):
            with pytest.raises(RepositoryNotFoundError):
                client.update_repo("nonexistent-repo-12345", {"description": "test"})


@allure.epic("GitHub API Client")
@allure.feature("Performance")
class TestPerformance:
    """Performance tests."""

    @allure.story("Performance")
    @allure.title("Repository creation should complete within time limit")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.performance
    def test_create_repo_performance(self, client, test_repo_name, cleanup_repo):
        """
        Test that repository creation is fast enough.
        Performance threshold: 5 seconds for creation.
        """
        with allure.step("Measure creation time"):
            start_time = time.time()
            client.create_repo(test_repo_name, "Performance test", private=True)
            duration = time.time() - start_time

        with allure.step("Check duration is within limit"):
            allure.attach(
                f"Creation time: {duration:.3f} seconds",
                name="Duration",
                attachment_type=allure.attachment_type.TEXT
            )
            assert duration < 5.0, f"Creation took {duration:.2f}s, expected < 5s"

    @allure.story("Performance")
    @allure.title("Repository retrieval should complete within time limit")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.performance
    def test_get_repo_performance(self, client, test_repo_name, cleanup_repo, github_wait_time):
        """
        Test that repository retrieval is fast enough.
        Performance threshold: 3 seconds for retrieval.
        """
        # Create repo first
        client.create_repo(test_repo_name, "Performance test for get", private=True)
        time.sleep(github_wait_time)

        with allure.step("Measure retrieval time"):
            start_time = time.time()
            client.get_repo(test_repo_name)
            duration = time.time() - start_time

        with allure.step("Check duration is within limit"):
            allure.attach(
                f"Retrieval time: {duration:.3f} seconds",
                name="Duration",
                attachment_type=allure.attachment_type.TEXT
            )
            assert duration < 3.0, f"Retrieval took {duration:.2f}s, expected < 3s"

    @allure.story("Performance")
    @allure.title("Repository update should complete within time limit")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.performance
    def test_update_repo_performance(self, client, test_repo_name, cleanup_repo, github_wait_time):
        """
        Test that repository update is fast enough.
        Performance threshold: 3 seconds for update.
        """
        # Create repo first
        client.create_repo(test_repo_name, "Original description", private=True)
        time.sleep(github_wait_time)

        with allure.step("Measure update time"):
            start_time = time.time()
            client.update_repo(test_repo_name, {"description": "Updated description"})
            duration = time.time() - start_time

        with allure.step("Check duration is within limit"):
            allure.attach(
                f"Update time: {duration:.3f} seconds",
                name="Duration",
                attachment_type=allure.attachment_type.TEXT
            )
            assert duration < 3.0, f"Update took {duration:.2f}s, expected < 3s"

    @allure.story("Performance")
    @allure.title("Repository deletion should complete within time limit")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.performance
    def test_delete_repo_performance(self, client, test_repo_name, github_wait_time):
        """
        Test that repository deletion is fast enough.
        Performance threshold: 3 seconds for deletion.
        """
        # Create repo first
        client.create_repo(test_repo_name, "Performance test for delete", private=True)
        time.sleep(github_wait_time)

        with allure.step("Measure deletion time"):
            start_time = time.time()
            client.delete_repo(test_repo_name)
            duration = time.time() - start_time

        with allure.step("Check duration is within limit"):
            allure.attach(
                f"Deletion time: {duration:.3f} seconds",
                name="Duration",
                attachment_type=allure.attachment_type.TEXT
            )
            assert duration < 3.0, f"Deletion took {duration:.2f}s, expected < 3s"

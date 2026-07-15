"""
Basic usage example for GitHubAPIClient.
Demonstrates how to create, read, update, and delete repositories.
"""

import os
import time
from dotenv import load_dotenv
from github_api_client import GitHubAPIClient

# Load environment variables
load_dotenv()


def main():
    """Demonstrate basic CRUD operations."""

    # Initialize client
    token = os.getenv('GITHUB_TOKEN')
    owner = os.getenv('GITHUB_USERNAME', 'Hold-My-Tea')

    if not token:
        print("❌ GITHUB_TOKEN not found in .env file")
        return

    client = GitHubAPIClient(token, owner)

    # Generate unique repository name
    repo_name = f"example-repo-{int(time.time())}"

    print(f"🚀 Creating repository: {repo_name}")

    # 1. CREATE
    repo = client.create_repo(repo_name, "Example repository", private=True)
    print(f"✅ Created: {repo['name']}")
    print(f"  URL: {repo['html_url']}")

    time.sleep(2)

    # 2. READ
    repo_data = client.get_repo(repo_name)
    print(f"📖 Retrieved: {repo_data['name']}")

    # 3. UPDATE
    client.update_repo(repo_name, {"description": "Updated description"})
    print(f"✏️ Updated description")

    time.sleep(2)

    # 4. DELETE
    client.delete_repo(repo_name)
    print(f"🗑️ Deleted: {repo_name}")

    print("🎉 Example completed!")


if __name__ == "__main__":
    main()
# GitHub API Client

A professional Python client for GitHub REST API with full CRUD operations for repositories.

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## Features

- Full CRUD operations — Create, Read, Update, Delete repositories
- Type hints — Better IDE support and code quality
- Error handling — Custom exceptions for different error scenarios
- Logging — Built-in logging for debugging and monitoring
- Clean OOP design — Easy to extend and maintain
- Allure reports — Beautiful test reports with Allure
- Test coverage — 19 tests with positive, negative, and performance scenarios

---

## Requirements

- Python 3.8+
- GitHub Personal Access Token with scopes: repo and delete_repo

---

## Installation

### 1. Clone the repository

git clone https://github.com/Hold-My-Tea/github-api-client.git
cd github-api-client

### 2. Create virtual environment (recommended)

python -m venv venv
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate     # Windows

### 3. Install dependencies

pip install -r requirements.txt

### 4. Install package in development mode

pip install -e .

---

## Configuration

### 1. Create .env file

Copy .env.example to .env:

cp .env.example .env

### 2. Add your GitHub credentials

Open .env and add your data:

GITHUB_TOKEN=your_github_personal_access_token_here
GITHUB_USERNAME=your_github_username_here

### 3. How to get a GitHub token

1. Go to GitHub -> Settings -> Developer settings
2. Select Personal access tokens -> Tokens (classic)
3. Click Generate new token -> Generate new token (classic)
4. Select scopes: repo (full access) and delete_repo
5. Copy the token and add it to .env

---

## Quick Start

from github_api_client import GitHubAPIClient
from dotenv import load_dotenv
import os

load_dotenv()

client = GitHubAPIClient(
    token=os.getenv('GITHUB_TOKEN'),
    owner=os.getenv('GITHUB_USERNAME')
)

# Create a repository
repo = client.create_repo("my-test-repo", "My test repository", private=True)
print(f"Created: {repo['name']}")

# Get repository
repo_data = client.get_repo("my-test-repo")
print(f"Retrieved: {repo_data['name']}")

# Update repository
client.update_repo("my-test-repo", {"description": "Updated description!"})
print(f"Updated description")

# Delete repository
client.delete_repo("my-test-repo")
print(f"Deleted")

---

## Examples

### Basic CRUD Example

Run the full example:

python examples/basic_usage.py

### Advanced Usage

from github_api_client import GitHubAPIClient

client = GitHubAPIClient(token="your_token", owner="your_username")

# Get all repositories
repos = client.get_all_repos(per_page=10)
for repo in repos:
    print(f"- {repo['name']} ({repo['stargazers_count']} star)")

# Check if repository exists
if client.repo_exists("my-repo"):
    print("Repository exists!")
else:
    print("Repository not found")

# Update multiple fields
client.update_repo(
    "my-repo",
    description="New description",
    private=False,
    has_wiki=False
)

---

## Running Tests

### Install development dependencies

pip install -r requirements-dev.txt

### Run all tests

pytest tests/ -v

### Run specific test categories

pytest -m smoke       # Quick sanity checks
pytest -m positive    # Positive test cases
pytest -m negative    # Negative test cases
pytest -m performance # Performance tests

### Generate Allure report

pytest tests/ --alluredir=allure-results
allure serve allure-results

---

## Project Structure

📁 github_api_client/
├── 📁 src/
│   └── 📁 github_api_client/
│       ├── 📄 __init__.py          # Package initialization
│       ├── 📄 client.py            # GitHubAPIClient
│       └── 📄 exceptions.py        # Custom exceptions
├── 📁 tests/
│   ├── 📄 __init__.py
│   ├── 📄 conftest.py              # Pytest fixtures
│   └── 📄 test_client.py           # 19 test cases
├── 📁 examples/
│   └── 📄 basic_usage.py           # Basic CRUD example
├── 📄 .env.example                  # Environment variables template
├── 📄 .gitignore                    # Ignored files
├── 📄 LICENSE                       # MIT License
├── 📄 pytest.ini                    # Pytest configuration
├── 📄 README.md                     # This file
├── 📄 requirements.txt              # Production dependencies
├── 📄 requirements-dev.txt          # Development dependencies
└── 📄 setup.py                      # Package installation

---

## Error Handling

The client handles various error scenarios with custom exceptions:

from github_api_client.exceptions import (
    RepositoryNotFoundError,
    RateLimitError,
    AuthenticationError,
    ValidationError
)

try:
    repo = client.get_repo("nonexistent-repo")
except RepositoryNotFoundError:
    print("Repository not found")
except RateLimitError:
    print("Rate limit exceeded, please wait")
except AuthenticationError:
    print("Invalid token")
except ValidationError as e:
    print(f"Validation failed: {e.response}")

---

## Test Coverage

- Positive tests: Client initialization, create, get, update, delete, exists, get_all, multiple repos, delete non-existent
- Negative tests: Get non-existent, create with empty/too long name, update non-existent
- Performance tests: Create, get, update, delete speed tests
- Total: 19 tests

---

## Contributing

1. Fork the repository
2. Create a feature branch (git checkout -b feature/amazing-feature)
3. Commit your changes (git commit -m 'Add amazing feature')
4. Push to the branch (git push origin feature/amazing-feature)
5. Open a Pull Request

---

## License

Distributed under the MIT License. See LICENSE for more information.

---

## Author

- GitHub: @Hold-My-Tea

---

## Acknowledgments

- GitHub REST API Documentation
- Requests Library
- Pytest
- Allure Framework

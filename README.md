# 🧪 GitHub API Client

![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python)
![Pytest](https://img.shields.io/badge/Pytest-7.4.0-green?logo=pytest)
![Allure](https://img.shields.io/badge/Allure-2.24.0-red?logo=allure)
![Requests](https://img.shields.io/badge/Requests-2.31.0-orange)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 📋 About

**GitHub API Client** is a Python client for GitHub REST API with full CRUD operations for repositories. The project demonstrates a clean approach to test automation, maintainable code structure, and modern testing practices.

### ✨ Key Features

- ✅ Full CRUD for repositories (Create, Read, Update, Delete)
- ✅ Clean OOP design — easy to extend and maintain
- ✅ Custom exceptions for different error scenarios
- ✅ Built-in logging for debugging and monitoring
- ✅ 19 tests with Allure reporting
- ✅ Environment variables support via .env
- ✅ Allure Reports integration for detailed test results

## 🛠 Tech Stack

| Component | Purpose |
|-----------|---------|
| **Python 3.8+** | Main programming language |
| **Pytest** | Testing framework |
| **Requests** | HTTP client for API interactions |
| **Allure** | Test reporting system |
| **python-dotenv** | Configuration management |

## 📁 Project Structure

```

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
├── 📄 pytest.ini                    # Pytest configuration
├── 📄 README.md                     # This file
├── 📄 requirements.txt              # Production dependencies
├── 📄 requirements-dev.txt          # Development dependencies
└── 📄 setup.py                      # Package installation

```
## 🚀 Quick Start


```bash
# Clone the repository
git clone https://github.com/Hold-My-Tea/github-api-client.git
cd github-api-client

# Create virtual environment
python -m venv venv
source venv/bin/activate      # for Linux/Mac
# venv\Scripts\activate       # for Windows

# Install dependencies
pip install -r requirements.txt

# Install package in development mode
pip install -e .

# Configure environment
cp .env.example .env


```
## ⚙️ Configuration

The .env file is not stored in the repository — this is a security best practice. Tokens and credentials are added locally.
```
env
GITHUB_TOKEN=your_github_personal_access_token_here
GITHUB_USERNAME=your_github_username_here
```
## 🧪 Running Tests

```
# Basic run
pytest

# With verbose output
pytest -v

# By markers
pytest -m smoke       # Quick sanity checks
pytest -m positive    # Positive test cases
pytest -m negative    # Negative test cases
pytest -m performance # Performance tests

# With Allure report
pytest --alluredir=allure-results
allure serve allure-results
```

### 📊 Test Coverage

| Category | Tests |
|----------|-------|
| **Positive** | Initialization, create, get, update, delete, exists, get_all, multiple repos |
| **Negative** | Get non-existent, create with empty/too long name, update non-existent |
| **Performance** | Create, get, update, delete speed tests |
| **Total** | **19** tests |

## 📬 Contacts
- Author: Oksana Maier 
- GitHub: [@Hold-My-Tea](https://github.com/Hold-My-Tea) 
- Project: [Hold-My-Tea/github-api-client](https://github.com/Hold-My-Tea/github-api-client)


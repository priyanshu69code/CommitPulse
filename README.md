# CommitPulse �

**CommitPulse** is an innovative Django-based application that automatically transforms your daily GitHub commits into engaging social media content. It monitors your assigned repositories, analyzes git diffs from daily commits, feeds them to AI for content generation, and automatically posts the generated content to LinkedIn and Twitter.

> ⚠️ **Note**: This project is currently under active development. Features and functionality may change as we continue to build and improve the platform.

## 🚀 Features

- **Automated Commit Monitoring**: Tracks daily commits on assigned GitHub repositories
- **Git Diff Analysis**: Extracts and analyzes code changes from commits
- **AI-Powered Content Generation**: Uses AI to create engaging posts from technical changes
- **Multi-Platform Publishing**: Automatically posts to LinkedIn and Twitter
- **GitHub Integration**: Seamless connection with GitHub using Personal Access Tokens
- **User Management**: Custom user authentication system with email-based login
- **Repository Assignment**: Select specific repositories to monitor for commits
- **RESTful API**: Well-structured API endpoints for all functionalities
- **Secure Authentication**: JWT-based authentication with Django REST Framework
- **PostgreSQL Database**: Robust database support for production environments

## 🛠️ Tech Stack

- **Backend**: Django 5.2.3 + Django REST Framework
- **Database**: PostgreSQL (with SQLite for development)
- **Authentication**: Django REST Framework SimpleJWT
- **GitHub API**: Custom GitHub wrapper for commit monitoring and diff extraction
- **AI Integration**: AI content generation from code changes (implementation in progress)
- **Social Media APIs**: LinkedIn and Twitter API integration (under development)
- **Containerization**: Docker & Docker Compose
- **Package Management**: uv (Python package manager)

## 🔄 How It Works

1. **Repository Assignment**: Users assign GitHub repositories to monitor
2. **Daily Commit Monitoring**: The system checks for new commits daily
3. **Diff Extraction**: Git diffs are extracted from recent commits
4. **AI Content Generation**: Commits and diffs are processed by AI to create engaging content
5. **Social Media Publishing**: Generated content is automatically posted to LinkedIn and Twitter
6. **Analytics & Tracking**: Monitor post performance and engagement (planned feature)

## 📋 Prerequisites

Before you begin, ensure you have the following installed:
- Python 3.13 or higher
- Docker and Docker Compose (for development database)
- Git
- A GitHub Personal Access Token
- LinkedIn API credentials (for social media posting)
- Twitter API credentials (for social media posting)
- AI API access (OpenAI, Claude, or similar - for content generation)

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/CommitPulse.git
cd CommitPulse
```

### 2. Set up Environment Variables
Create a `.env` file in the root directory:
```env
# Django Configuration
SECRET_KEY=your-django-secret-key-here
DEBUG=True
DATABASE_URL=postgresql://dev_user:dev_password@localhost:5432/dev_db

# GitHub API
GITHUB_TOKEN=your-github-personal-access-token

# AI API Configuration (Choose one or configure multiple)
OPENAI_API_KEY=your-openai-api-key
CLAUDE_API_KEY=your-claude-api-key

# Social Media APIs
LINKEDIN_CLIENT_ID=your-linkedin-client-id
LINKEDIN_CLIENT_SECRET=your-linkedin-client-secret
TWITTER_API_KEY=your-twitter-api-key
TWITTER_API_SECRET=your-twitter-api-secret
TWITTER_ACCESS_TOKEN=your-twitter-access-token
TWITTER_ACCESS_TOKEN_SECRET=your-twitter-access-token-secret
```

### 3. Start the Development Database
```bash
docker-compose -f docker-compose-dev.yml up -d
```

### 4. Install Dependencies
```bash
pip install uv
uv sync
```

### 5. Run Database Migrations
```bash
cd backend
python manage.py migrate
```

### 6. Create a Superuser
```bash
python manage.py createsuperuser
```

### 7. Start the Development Server
```bash
python manage.py runserver
```

The application will be available at `http://localhost:8000`

## 📚 API Endpoints

### Authentication
- `POST /api/token/` - Obtain JWT token
- `POST /api/token/refresh/` - Refresh JWT token

### User Management
- `GET /api/user/profile/` - Get user profile
- `PUT /api/user/profile/` - Update user profile

### GitHub Integration
- `GET /api/bot/` - Bot view with GitHub data
- `GET /api/bot/profile/` - Get GitHub user profile
- `GET /api/bot/repos/` - Get user's GitHub repositories

### Repository Management (In Development)
- `POST /api/repos/assign/` - Assign repository for monitoring
- `GET /api/repos/monitored/` - Get list of monitored repositories
- `DELETE /api/repos/unassign/{id}/` - Remove repository from monitoring

### Commit Processing (In Development)
- `GET /api/commits/daily/` - Get daily commits from monitored repos
- `POST /api/commits/process/` - Manually trigger commit processing
- `GET /api/commits/diffs/{commit_id}/` - Get diff for specific commit

### Content Generation (Planned)
- `POST /api/content/generate/` - Generate content from commits
- `GET /api/content/drafts/` - Get generated content drafts
- `POST /api/content/publish/` - Publish content to social media

### Social Media Integration (Planned)
- `GET /api/social/linkedin/status/` - Check LinkedIn connection status
- `GET /api/social/twitter/status/` - Check Twitter connection status
- `GET /api/social/posts/` - Get published posts history

## 🏗️ Project Structure

```
CommitPulse/
├── backend/                    # Django backend application
│   ├── config/                # Django project configuration
│   ├── user/                  # User management app
│   ├── core/                  # Core utilities and models
│   │   └── utils/
│   │       └── github_rapper.py  # GitHub API wrapper for commits/diffs
│   ├── bot/                   # GitHub integration and processing app
│   └── manage.py              # Django management script
├── docker-compose-dev.yml     # Development database setup
├── pyproject.toml            # Python project configuration
├── uv.lock                   # Dependency lock file
└── README.md                 # This file
```

## 🚧 Development Status

This project is currently in active development. Here's what's implemented and what's planned:

### ✅ Completed Features
- [x] User authentication and management
- [x] GitHub API integration
- [x] Repository fetching
- [x] Basic commit data retrieval
- [x] JWT-based authentication
- [x] Database models and migrations

### 🔨 In Progress
- [ ] Daily commit monitoring system
- [ ] Git diff extraction and analysis
- [ ] AI integration for content generation
- [ ] Content template system

### 📋 Planned Features
- [ ] LinkedIn API integration
- [ ] Twitter API integration
- [ ] Automated posting scheduler
- [ ] Content approval workflow
- [ ] Post analytics and tracking
- [ ] Custom content templates
- [ ] Multi-repository monitoring
- [ ] Webhook support for real-time processing

## 🔧 Key Components

### GitHub API Wrapper
The project includes a sophisticated GitHub API wrapper (`github_rapper.py`) that follows SOLID principles:
- **Authentication Strategies**: Support for Personal Access Tokens
- **Commit Monitoring**: Daily commit tracking and analysis
- **Diff Extraction**: Retrieval of git diffs from commits
- **Repository Management**: Handling of assigned repositories
- **Rate Limiting**: Built-in support for GitHub API rate limits

### AI Content Generation (In Development)
- **Diff Analysis**: Parse and understand code changes
- **Content Templates**: Customizable templates for different types of posts
- **Context Awareness**: Generate relevant content based on commit messages and changes
- **Multi-format Output**: Support for LinkedIn and Twitter post formats

### Social Media Integration (Planned)
- **LinkedIn Publishing**: Automated posting to LinkedIn profiles/pages
- **Twitter Publishing**: Automated tweeting of generated content
- **Cross-platform Scheduling**: Coordinated posting across platforms
- **Analytics Integration**: Track engagement and performance

### User Model
Custom user model with email-based authentication and social media token storage:
- Email as primary identifier
- GitHub token management
- Social media credentials storage (encrypted)
- Repository assignment tracking

## 🔐 Security Features

- JWT-based authentication
- Secure GitHub token storage
- Environment variable configuration
- CORS protection
- SQL injection prevention through Django ORM

## 🧪 Testing

Run the test suite:
```bash
cd backend
python manage.py test
```

## 📈 Usage Examples

### Setting Up Repository Monitoring
1. Obtain a GitHub Personal Access Token from GitHub Settings
2. Create a user account through the API or admin panel
3. Store the GitHub token using the user management endpoints
4. Assign repositories for daily monitoring
5. Configure AI and social media API credentials

### Example Workflow (When Fully Implemented)
```python
# 1. Assign a repository for monitoring
POST /api/repos/assign/
{
    "repo_name": "username/awesome-project",
    "monitor_daily": true
}

# 2. The system will automatically:
# - Check for new commits daily
# - Extract git diffs
# - Generate AI content
# - Post to LinkedIn and Twitter

# 3. View generated content
GET /api/content/drafts/
```

### Manual Content Generation (Planned)
```python
# Generate content from specific commits
POST /api/content/generate/
{
    "commit_ids": ["abc123", "def456"],
    "platforms": ["linkedin", "twitter"],
    "template": "feature_update"
}
```

## 🤝 Contributing

We welcome contributions to CommitPulse! Please follow the setup guide below to get started with development.

---

## 🛠️ Development Setup Guide

### Prerequisites for Contributors

- Python 3.13+
- Docker & Docker Compose
- Git
- Code editor (VS Code recommended)
- GitHub account and Personal Access Token

### Step-by-Step Setup

#### 1. Fork and Clone
```bash
# Fork the repository on GitHub, then clone your fork
git clone https://github.com/YOUR-USERNAME/CommitPulse.git
cd CommitPulse

# Add upstream remote
git remote add upstream https://github.com/ORIGINAL-OWNER/CommitPulse.git
```

#### 2. Development Environment Setup
```bash
# Install uv package manager
curl -LsSf https://astral.sh/uv/install.sh | sh
# or
pip install uv

# Create and activate virtual environment
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
uv sync
```

#### 3. Database Setup
```bash
# Start PostgreSQL using Docker
docker-compose -f docker-compose-dev.yml up -d

# Verify database is running
docker ps
```

#### 4. Environment Configuration
```bash
# Create .env file
cp .env.example .env  # If example exists, otherwise create manually

# Edit .env with your settings
# Django Configuration
SECRET_KEY=your-super-secret-django-key-here
DEBUG=True
DATABASE_URL=postgresql://dev_user:dev_password@localhost:5432/dev_db

# GitHub API
GITHUB_TOKEN=your-github-personal-access-token

# AI API Configuration
OPENAI_API_KEY=your-openai-api-key  # Or other AI service

# Social Media APIs (for future implementation)
LINKEDIN_CLIENT_ID=your-linkedin-client-id
LINKEDIN_CLIENT_SECRET=your-linkedin-client-secret
TWITTER_API_KEY=your-twitter-api-key
TWITTER_API_SECRET=your-twitter-api-secret
```

#### 5. Django Setup
```bash
cd backend

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files (if needed)
python manage.py collectstatic --noinput
```

#### 6. Verify Installation
```bash
# Run tests
python manage.py test

# Start development server
python manage.py runserver

# In another terminal, test the API
curl http://localhost:8000/api/bot/
```

### Development Workflow

#### 1. Create Feature Branch
```bash
git checkout -b feature/your-feature-name
```

#### 2. Make Changes
- Follow Django best practices
- Write tests for new functionality
- Update documentation as needed
- Follow PEP 8 style guidelines

#### 3. Testing
```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test user
python manage.py test bot
python manage.py test core

# Check code coverage (if coverage.py is installed)
coverage run --source='.' manage.py test
coverage report
```

#### 4. Code Quality
```bash
# Install development dependencies
uv add --dev black flake8 isort

# Format code
black .
isort .

# Check linting
flake8 .
```

#### 5. Commit Changes
```bash
git add .
git commit -m "feat: add new feature description"

# Follow conventional commit format:
# feat: new feature
# fix: bug fix
# docs: documentation changes
# style: code style changes
# refactor: code refactoring
# test: test changes
# chore: maintenance tasks
```

#### 6. Push and Create PR
```bash
git push origin feature/your-feature-name
```
Then create a Pull Request on GitHub.

### Development Guidelines

#### Code Style
- Follow PEP 8 for Python code
- Use meaningful variable and function names
- Add docstrings to classes and functions
- Keep functions small and focused

#### Database Migrations
```bash
# Create new migration
python manage.py makemigrations app_name

# Apply migrations
python manage.py migrate

# Check migration status
python manage.py showmigrations
```

#### Adding New Dependencies
```bash
# Add new package
uv add package_name

# Add development dependency
uv add --dev package_name

# Update lock file
uv lock
```

#### Environment Variables
- Never commit sensitive data
- Add new environment variables to `.env.example`
- Document required variables in this README
- Include API keys for:
  - GitHub Personal Access Token
  - AI service APIs (OpenAI, Claude, etc.)
  - Social media APIs (LinkedIn, Twitter)
  - Database credentials

### Troubleshooting

#### Common Issues

1. **Database Connection Error**
   ```bash
   # Check if PostgreSQL container is running
   docker ps

   # Restart database container
   docker-compose -f docker-compose-dev.yml restart
   ```

2. **Migration Issues**
   ```bash
   # Reset migrations (destructive)
   python manage.py migrate app_name zero
   python manage.py makemigrations app_name
   python manage.py migrate
   ```

3. **Import Errors**
   ```bash
   # Verify virtual environment is activated
   which python

   # Reinstall dependencies
   uv sync --refresh
   ```

4. **GitHub API Rate Limiting**
   - Check your token permissions
   - Implement proper error handling
   - Consider caching responses
   - Monitor daily API usage for commit monitoring

5. **AI API Integration Issues**
   ```bash
   # Test AI API connection
   python manage.py shell
   # Test your AI service integration
   ```

6. **Social Media API Setup**
   - Verify API credentials
   - Check OAuth flow implementation
   - Test posting permissions

### Getting Help

- Check existing issues on GitHub
- Join our community discussions
- Read Django and DRF documentation
- Follow the project's code style

### Pull Request Guidelines

1. **Before submitting:**
   - Ensure all tests pass
   - Update documentation
   - Add tests for new features
   - Follow commit message conventions

2. **PR Description should include:**
   - Clear description of changes
   - Link to related issues
   - Screenshots (if UI changes)
   - Testing instructions
   - Note if feature is complete or in-progress (given the development status)

3. **Review Process:**
   - Maintainers will review within 48 hours
   - Address feedback promptly
   - Keep PR scope focused
   - Mark WIP (Work in Progress) features clearly

### Development Priorities

Given the current development status, contributions are especially welcome in these areas:

1. **High Priority**
   - Daily commit monitoring implementation
   - Git diff extraction and parsing
   - AI content generation integration
   - Content template system

2. **Medium Priority**
   - LinkedIn API integration
   - Twitter API integration
   - Automated scheduling system
   - Content approval workflow

3. **Future Enhancements**
   - Analytics and tracking
   - Webhook support
   - Multi-repository management
   - Custom content templates

Thank you for contributing to CommitPulse! 🚀

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Django and Django REST Framework communities
- GitHub API documentation
- All contributors and maintainers

## 📞 Support

For support, please open an issue on GitHub or contact the maintainers.

---

**Happy Coding!** 🎉

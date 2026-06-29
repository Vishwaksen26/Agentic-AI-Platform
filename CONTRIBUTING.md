# Contributing to AgentForge AI

Thank you for your interest in contributing to AgentForge! We welcome contributions from the community, whether it's bug fixes, feature additions, documentation improvements, or other enhancements.

## Code of Conduct

This project adheres to a Code of Conduct. By participating, you are expected to uphold this code. Please report unacceptable behavior to support@agentforge.ai.

## How to Contribute

### Reporting Bugs

Before creating a bug report, check the issue list as you might find one that covers your problem. If you find a bug, create an issue with:

- **Title**: Clear and descriptive
- **Description**: Detailed description of the bug
- **Steps**: How to reproduce the issue
- **Expected**: What you expected to happen
- **Actual**: What actually happened
- **Environment**: OS, Python/Node version, etc.

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, include:

- **Title**: Clear and descriptive
- **Description**: Detailed description of the suggested enhancement
- **Rationale**: Why this would be useful
- **Examples**: Examples of how this would work

### Pull Requests

1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature/amazing-feature`
3. **Make** your changes
4. **Commit**: Follow conventional commit messages
5. **Push**: `git push origin feature/amazing-feature`
6. **Open** a Pull Request

#### Pull Request Guidelines

- Follow the existing code style
- Include tests for new functionality
- Update documentation as needed
- Link related issues in the PR description
- Keep PR focused on a single concern
- Ensure all checks pass

## Development Setup

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt
```

### Frontend

```bash
cd frontend
npm install
```

## Code Style

### Python

- Follow PEP 8
- Use type hints on all functions
- Docstrings on public classes and methods
- Max line length: 100 characters

### TypeScript/JavaScript

- Use ESLint and Prettier
- Type all functions and variables
- Follow React best practices
- Use meaningful variable names

## Commit Messages

Use conventional commit format:

```
<type>(<scope>): <subject>

<body>

<footer>
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

Example:
```
feat(auth): add JWT token refresh endpoint

This allows users to refresh their access tokens
using a refresh token without re-logging in.

Closes #123
```

## Testing

### Backend Tests

```bash
cd backend
pytest tests/

# With coverage
pytest --cov=backend tests/
```

### Frontend Tests

```bash
cd frontend
npm test

# With coverage
npm test -- --coverage
```

## Documentation

- Keep README.md up to date
- Add docstrings to functions
- Document complex logic with comments
- Update CHANGELOG.md for notable changes

## Questions?

- Open an issue for questions
- Check existing discussions
- Email support@agentforge.ai

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to AgentForge AI! 🚀

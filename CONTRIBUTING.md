# Contributing Guidelines

## Commit Message Convention

This project follows the [Conventional Commits](https://www.conventionalcommits.org/) specification for commit messages.

### Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- `feat`: A new feature
- `fix`: A bug fix
- `docs`: Documentation only changes
- `style`: Code style changes (formatting, missing semicolons, etc.)
- `refactor`: Code refactoring without changing functionality
- `perf`: Performance improvements
- `test`: Adding or updating tests
- `chore`: Maintenance tasks (dependencies, build config, etc.)
- `ci`: CI/CD changes
- `build`: Build system changes

### Examples

```
feat(api): add Alpha Vantage API integration

- Implement real-time gold price fetching
- Add error handling for API rate limits
- Include timestamp and timezone information

Closes #123
```

```
fix(preprocessing): replace deprecated fillna method

- Replace fillna(method='bfill') with bfill()
- Update to modern pandas syntax
- Maintain backward compatibility
```

```
docs(readme): update API configuration section

- Document Alpha Vantage API key setup
- Add usage examples
- Update data source descriptions
```

## Versioning

This project follows [Semantic Versioning](https://semver.org/):
- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

Version is tracked in the `VERSION` file and `CHANGELOG.md`.

## Code Standards

- Follow PEP 8 for Python code
- Add docstrings to all functions
- Include error handling where appropriate
- Write clear, descriptive variable names
- Add comments for complex logic

## Pull Request Process

1. Create a feature branch from `main`
2. Make your changes following commit conventions
3. Update `CHANGELOG.md` if needed
4. Ensure all code works in Google Colab
5. Submit a pull request with a clear description


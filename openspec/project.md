# Project Context

## Purpose
Recipe Manager is a Python application for managing, organizing, and storing recipes. The project enables users to:
- Store and organize recipe collections
- Search and filter recipes
- Manage recipe metadata (ingredients, instructions, tags, etc.)
- Potentially support meal planning and shopping list generation

## Tech Stack
- **Language**: Python 3.12
- **Package Management**: uv
- **Framework**: Django
- **Database**: SQLite
- **Testing**: pytest
- **Code Quality**: ruff, mypy

## Project Conventions

### Code Style
- Follow PEP 8 style guidelines
- Use type hints where appropriate
- Maximum line length: 79
- Use descriptive variable and function names (snake_case)
- Class names use PascalCase
- Constants use UPPER_SNAKE_CASE
- Prefer f-strings for string formatting
- Use docstrings for public functions, classes, and modules (Google or NumPy style)

### Architecture Patterns
- **Django Apps**: Organize functionality into Django apps (e.g., `recipes/`, `users/`, `meal_planning/`). Each app should be focused on a single domain concern
- **MVT Pattern**: Follow Django's Model-View-Template architecture:
  - **Models**: Define data structure and business logic in `models.py`
  - **Views**: Handle request/response logic (prefer class-based views for reusability)
  - **Templates**: Separate presentation logic in templates directory
- **Project Structure**: Keep project-level code minimal; most code should live in apps
- **Settings Management**: Use environment variables for sensitive settings (django-environ or python-decouple). Split settings into base, development, production modules
- **URL Routing**: Define URLs at app level (`urls.py` in each app), include in project `urls.py`
- **Models Best Practices**:
  - Use Django ORM for database operations (avoid raw SQL unless necessary)
  - Define `__str__` methods for models
  - Use `Meta` classes for model metadata (ordering, verbose names, etc.)
  - Leverage model relationships (ForeignKey, ManyToMany, OneToOne) appropriately
  - Use migrations for all schema changes (`python manage.py makemigrations`, `python manage.py migrate`)
- **Views Best Practices**:
  - Prefer class-based views (CBVs) for common patterns (ListView, DetailView, CreateView, UpdateView, DeleteView)
  - Use function-based views for custom logic that doesn't fit CBV patterns
  - Keep views thin; move business logic to models, managers, or service classes
  - Use Django's built-in authentication and permissions decorators/mixins
- **Forms**: Use ModelForms when forms map directly to models; custom forms for complex validation
- **Static Files & Media**: Use Django's static files framework; configure MEDIA_ROOT and MEDIA_URL for user uploads
- **Admin Interface**: Register models in `admin.py` with appropriate list_display, list_filter, search_fields
- **Error Handling**: Use Django's exception classes (Http404, PermissionDenied); create custom exceptions when needed
- **Security**: Leverage Django's built-in security features (CSRF protection, SQL injection prevention, XSS protection)
- **Middleware**: Use middleware sparingly; prefer app-level solutions when possible

### Testing Strategy
- Write unit tests for business logic and utility functions
- Use pytest as the testing framework
- Aim for meaningful test coverage (focus on critical paths)
- Use fixtures for test data setup
- Mock external dependencies (databases, APIs) in tests
- Tests should be fast, isolated, and repeatable

### Git Workflow
- **Branching**: Use feature branches for new work (`feature/`, `fix/`, `refactor/`)
- **Commits**: Write clear, descriptive commit messages
  - Use imperative mood ("Add recipe search" not "Added recipe search")
  - Reference issue numbers if applicable
  - Keep commits focused and atomic
- **Main Branch**: `master` contains production-ready code
- Use conventional commits format: `type(scope): description`

## Domain Context
- **Recipe**: A collection of ingredients, instructions, and metadata (name, description, tags, servings, prep time, cook time, etc.)
- **Ingredient**: A component of a recipe with quantity, unit, and name
- **Tag/Category**: Labels for organizing recipes (e.g., "vegetarian", "dessert", "quick-meals")
- **Collection**: A user-defined grouping of recipes
- Consider supporting recipe scaling (adjusting ingredient quantities for different serving sizes)
- Consider nutritional information tracking
- Consider meal planning and shopping list features


## Important Constraints
- Minimum Python version: Python 3.10
- Database choice may affect deployment and scalability
- Consider data privacy and user data storage requirements
- Consider authentication and authorization needs


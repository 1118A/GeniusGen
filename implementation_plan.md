# Implementation Plan - GeniusGen Platform

GeniusGen is a social media platform designed for students to showcase real, live projects. This plan outlines the architecture, database schema, and UI/UX strategy for building a production-ready application.

## User Review Required

> [!IMPORTANT]
> - **Tech Stack**: We will use Django with Django REST Framework (DRF) for the backend and a modern frontend approach (HTML5, Vanilla CSS with HSL variables, and Component-driven JavaScript).
> - **Database**: We will start with SQLite for development as requested, but the configuration will be PostgreSQL-ready.
> - **Authentication**: We will use Django's Session-based authentication for simplicity and security.

## Proposed Changes

### 1. Backend Architecture (Django)
We will initialize a Django project `geniusgen` and create modular apps:

- **`accounts`**: Custom user management and public profiles.
- **`posts`**: Core project sharing functionality (CRUD, likes, comments, collaboration).
- **`quizzes`**: Admin-managed MCQs and student attempts.
- **`notifications`**: Alerts for engagement and quizzes.
- **`dashboard`**: Admin metrics and analytics.

### 2. Database Schema

#### `accounts.User`
- Standard fields + `bio`, `avatar`, `is_student`, `is_admin`.

#### `posts.Post`
- `title`, `description`, `tech_stack` (Comma separated or JSON), `live_link`, `github_repo`, `image`, `author` (FK), `collaborators` (M2M to Users).

#### `posts.Comment` & `posts.Like`
- Relationships to `Post` and `User`.

#### `quizzes.Quiz`, `Question`, `Result`
- MCQs with timers and tracking.

### 3. Frontend Design (UI/UX)
- **Aesthetics**: Modern dark/light mode, smooth CSS transitions, glassmorphism.
- **Tech**: Vanilla JS for logic, modern CSS for layout (Grid/Flex).
- **Key Views**:
    - **Landing/Feed**: Interactive project masonry or grid.
    - **Post Create**: Multi-step or streamlined form with link validation.
    - **Admin Dashboard**: Visual stats and quiz manager.

### 4. Modular Development Steps

#### [NEW] Accounts Implementation
- Setup Django project and `accounts` app.
- Implement Custom User and Auth views.

#### [NEW] Posts Implementation
- Post model, views, and frontend feed.
- Like and Comment functionality.

#### [NEW] Quizzes implementation
- Quiz models and Admin controls.
- Student attempt logic and timer.

#### [NEW] Dashboard & Polish
- UI/UX polish with animations.
- Final testing and validation.

## Verification Plan

### Automated Tests
- Django tests for API endpoints.
- Form validation tests.

### Manual Verification
- Testing the project creation flow.
- Verifying the quiz timer and submission.
- Checking mobile responsiveness.

## Open Questions
- Do you have a preferred color scheme (e.g., Deep Purple / Electric Blue or Modern Minimalist White)?
- Should project collaborators be able to edit the post, or only the primary author?

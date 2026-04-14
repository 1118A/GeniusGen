<div align="center">

# ⚡ GeniusGen

**The student project showcase platform — share real work, discover real talent.**

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)](https://python.org)
[![Django](https://img.shields.io/badge/Django-6.0-092E20?style=flat&logo=django&logoColor=white)](https://djangoproject.com)
[![License](https://img.shields.io/badge/License-MIT-6C63FF?style=flat)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-43E97B?style=flat)](CONTRIBUTING.md)

</div>

---

## 📌 Overview

GeniusGen is a public social media platform built exclusively for students to showcase **real, recently completed projects**. Every post must include a working live link — no mockups, no fake demos.

> Built with Django · Glassmorphism UI · Dark Mode · Real-time notifications · Quiz system

---

## ✨ Features

### 👤 For Students
| Feature | Details |
|---------|---------|
| 📝 **Post Projects** | Title, description, tech stack, live link, GitHub repo, screenshot |
| 🔥 **Feed** | Browse all projects — sort by Latest or Trending |
| 🔍 **Search** | Filter by keywords or tech stack (React, Django, ML…) |
| ❤️ **Engage** | Like and bookmark projects (AJAX — no page reload) |
| 💬 **Comments** | Comment on any project |
| 👥 **Collaborators** | Tag teammates on group projects |
| 🧠 **Quizzes** | Attempt timed MCQ quizzes with countdown timer |
| 🔔 **Notifications** | Get alerted on likes, comments, new quizzes |
| 🔖 **Bookmarks** | Save projects to revisit later |
| 🌙 **Dark Mode** | System-wide toggle, saved to localStorage |

### 🛡️ For Admins
| Feature | Details |
|---------|---------|
| 📊 **Dashboard** | Chart.js analytics: users, posts, likes per day |
| 📝 **Quiz Builder** | Create MCQ quizzes with dynamic question/choice adding |
| 📢 **Broadcast** | Notify all users when a new quiz is published |
| 🗂️ **Django Admin** | Full model management with inline editing |

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python · Django 6 · Django REST Framework |
| Database | SQLite (dev) · PostgreSQL (prod-ready) |
| Frontend | HTML5 · Vanilla CSS · Vanilla JavaScript |
| Charts | Chart.js (CDN) |
| Auth | Django Session Auth · Role-based (student/admin) |
| Media | Pillow (image uploads) |

---

## 🚀 Quick Start

### 1. Clone the repo
```bash
git clone https://github.com/1118A/GeniusGen.git
cd GeniusGen
```

### 2. Create & activate virtual environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Apply database migrations
```bash
python manage.py migrate
```

### 5. Create an admin user
```bash
python manage.py createsuperuser
```

### 6. Run the development server
```bash
python manage.py runserver
```

Open **http://127.0.0.1:8000** in your browser.

---

## 📁 Project Structure

```
GeniusGen/
├── accounts/           # Auth, profiles, follow system
│   ├── models.py       # Custom User model
│   ├── views.py        # signup, login, profile, follow
│   ├── forms.py        # SignupForm, LoginForm, ProfileEditForm
│   └── urls.py
├── posts/              # Project feed, CRUD, likes, bookmarks
│   ├── models.py       # Post, Comment, Like, Bookmark
│   ├── views.py        # Feed, detail, create, search, AJAX
│   ├── forms.py        # PostForm, CommentForm
│   └── urls.py
├── quizzes/            # Quiz builder and attempt engine
│   ├── models.py       # Quiz, Question, Choice, QuizResult
│   ├── views.py        # Create, attempt, score, leaderboard
│   ├── forms.py        # QuizForm, QuestionForm, ChoiceForm
│   └── urls.py
├── notifications/      # Alert system
│   ├── models.py       # Notification model
│   ├── views.py        # List, mark-read, unread count API
│   └── utils.py        # create_notification(), notify_all_users()
├── dashboard/          # Admin analytics
│   └── views.py        # Metrics + Chart.js data
├── templates/          # HTML templates (18 files)
│   ├── base.html       # Navbar, sidebar, dark mode, toasts
│   ├── accounts/
│   ├── posts/
│   ├── quizzes/
│   ├── notifications/
│   └── dashboard/
├── static/
│   ├── css/main.css    # Full design system + dark mode
│   └── js/main.js      # Dark mode, AJAX, quiz timer, polling
├── geniusgen/          # Django project config
│   ├── settings.py
│   └── urls.py
├── manage.py
├── requirements.txt
└── .gitignore
```

---

## 🔑 Default Admin

After `createsuperuser`, log in at `/admin/` and set `role = admin` in the User admin to access the dashboard and quiz builder.

Or run this one-liner after migrations:
```bash
python manage.py shell -c "
from accounts.models import User
User.objects.create_superuser(
    username='admin', email='admin@geniusgen.com',
    password='admin123', role='admin',
    first_name='Admin', last_name='User'
)
print('Done')
"
```

---

## 🌐 URL Reference

| URL | Description |
|-----|-------------|
| `/` | Public feed (Latest / Trending) |
| `/search/` | Search projects |
| `/post/create/` | Create a new project post |
| `/post/<id>/` | Project detail page |
| `/accounts/signup/` | Register |
| `/accounts/login/` | Login |
| `/accounts/profile/<username>/` | User profile |
| `/accounts/profile/edit/` | Edit own profile |
| `/quizzes/` | Quiz list |
| `/quizzes/create/` | Admin — create quiz |
| `/quizzes/<id>/` | Take a quiz |
| `/quizzes/<id>/results/` | Quiz results + leaderboard |
| `/notifications/` | Notification list |
| `/bookmarks/` | Saved posts |
| `/dashboard/` | Admin analytics dashboard |
| `/admin/` | Django admin panel |

---

## 🚢 Deployment

### Environment variables (production)
Create a `.env` file:
```env
SECRET_KEY=your-long-random-secret-key
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=postgresql://user:pass@host:5432/geniusgen
```

### Collect static files
```bash
python manage.py collectstatic
```

### Run with Gunicorn
```bash
pip install gunicorn
gunicorn geniusgen.wsgi:application --bind 0.0.0.0:8000
```

---

## 🛡️ Security Features

- ✅ CSRF protection on all forms & AJAX requests
- ✅ SQL injection prevention via Django ORM
- ✅ XSS protection via Django template auto-escaping  
- ✅ Password hashing (PBKDF2 + SHA256)
- ✅ Secure auth redirects with `@login_required`
- ✅ Role-based access control (student vs admin)
- ✅ URL validation on live_link field

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---

<div align="center">
Built with ❤️ for students, by students.
</div>

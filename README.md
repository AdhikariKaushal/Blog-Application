# 📝 Django Blog Application

A full-featured blog platform built with **Django**, featuring user authentication, a rich-text editor, categories & tags, full-text search, comments, email sharing, RSS/sitemap feeds, and a documented **REST API**.


---

## ✨ Features

**Blog**
- Create, edit, and delete your own posts (only the author can modify a post)
- Draft / Published status — only published posts are public
- "My Posts" dashboard for each logged-in user
- Rich-text editing with **TinyMCE**
- Featured image upload for every post
- SEO-friendly URLs (`/blog/2026/8/14/my-post-slug/`)
- Pagination on the post list

**Organisation & Discovery**
- Categories and tags (via `django-taggit`)
- Filter posts by tag or category
- Full-text search using **PostgreSQL** (`SearchVector`, `SearchRank`, `TrigramSimilarity`)
- Similar posts suggestions based on shared tags
- Custom template tags: total posts, latest posts, most commented posts

**Community**
- Signup / login / logout
- Comment system (moderation via an `active` flag in admin)
- Share a post by email

**Extras**
- RSS feed of latest posts
- XML sitemap
- REST API with search, authentication, and permissions
- Auto-generated API docs (Swagger UI & ReDoc) via `drf-spectacular`

---

## 🛠️ Tech Stack

| Area | Tools |
|---|---|
| Backend | Python 3.12, Django 6 |
| Database | PostgreSQL (`psycopg2-binary`) |
| API | Django REST Framework, drf-spectacular |
| Editor | django-tinymce |
| Tags | django-taggit |
| Images | Pillow |
| Config | python-decouple (`.env`) |
| Frontend | Django templates + CSS |

---

## 📁 Project Structure

```
Blog Application/
├── mysite/        # Project settings & root URLs
├── blog/          # Posts, categories, tags, search, auth views, feeds, sitemap
├── comments/      # Comment model & form
├── api/           # DRF serializers, views, and routes
├── media/         # Uploaded post images (not tracked in Git)
├── manage.py
└── requirements.txt
```

---

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/<your-username>/<your-repo-name>.git
cd <your-repo-name>
```

### 2. Create and activate a virtual environment
```bash
python -m venv my_env

# Windows
my_env\Scripts\activate

# macOS / Linux
source my_env/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up PostgreSQL
The project uses PostgreSQL-only features (full-text search & trigram similarity), so SQLite won't work.

```sql
CREATE DATABASE blog;
CREATE USER blog WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE blog TO blog;
ALTER DATABASE blog OWNER TO blog;
\c blog
CREATE EXTENSION IF NOT EXISTS pg_trgm;
```

### 5. Configure environment variables
Copy `.env.example` to `.env` and fill in your values:

```env
SECRET_KEY=your-django-secret-key
DB_PASSWORD=your-database-password

EMAIL_HOST=smtp.gmail.com
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
EMAIL_PORT=587
EMAIL_USE_TLS=True
```

> For Gmail, use an [App Password] not your normal password.

### 6. Run migrations and create an admin user
```bash
python manage.py migrate
python manage.py createsuperuser
```

### 7. Start the server
```bash
python manage.py runserver
```

Open **http://127.0.0.1:8000/blog/** 🎉

---

## 🔗 Main URLs

| URL | Description |
|---|---|
| `/blog/` | Post list |
| `/blog/new/` | Create a post |
| `/blog/my-posts/` | Your posts |
| `/blog/tag/<slug>/` | Posts by tag |
| `/blog/category/<slug>/` | Posts by category |
| `/blog/feed/` | RSS feed |
| `/blog/signup/` | Register |
| `/accounts/login/` | Login |
| `/admin/` | Django admin |
| `/sitemap.xml` | Sitemap |

---

## 🔌 REST API

| Method | Endpoint | Description | Auth |
|---|---|---|---|
| GET | `/api/posts/` | List published posts (supports `?search=`) | Public |
| POST | `/api/posts/` | Create a post | Required |
| GET | `/api/posts/<id>/` | Retrieve a post | Public |
| PUT/PATCH | `/api/posts/<id>/` | Update a post (author only) | Required |
| DELETE | `/api/posts/<id>/` | Delete a post (author only) | Required |
| GET | `/api/posts/<post_id>/comments/` | List active comments | Public |
| POST | `/api/posts/<post_id>/comments/` | Add a comment | Public |

**Interactive docs:**
- Swagger UI → `/api/docs/`
- ReDoc → `/api/redoc/`
- OpenAPI schema → `/api/schema/`

---

## 🧩 Data Models

- **Post** — title, slug, author, category, body (HTML), image, tags, status, publish/created/updated dates
- **Category** — name, slug
- **Comment** — post, name, email, body, active flag, timestamps

---

## 🔮 Possible Improvements

- Token/JWT authentication for the API
- Automated tests for views and API endpoints
- Docker setup for easier deployment
- Comment replies and user profiles
- Deployment guide (Render / Railway / VPS)

---

## 👤 Author

**Kaushal Adhikari**

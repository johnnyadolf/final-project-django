# Django Final Project

This Django application provides a course management system with user authentication and course enrollment features. It is deployed on Render and uses Supabase as the database provider.

## 🚀 Live Demo

[Visit the live application](https://django-johnnyadolf.onrender.com/)

## 🛠 Tech Stack

- Django 4.x
- Python 3.x
- Supabase (PostgreSQL)
- Bootstrap 5
- Render (Hosting)

## 📋 Prerequisites

- Python 3.x
- pip
- virtualenv (recommended)
- Supabase account
- Render account

## ⚙️ Local Development Setup

1. Clone the repository:

```bash
git clone <repository-url>
cd final-project-django
```

2. Create and activate virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On macOS
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Set up environment variables:

```bash
cp .env.example .env
```

Edit `.env` with your Supabase credentials:

```
DATABASE_URL=your_supabase_connection_string
SECRET_KEY=your_django_secret_key
DEBUG=True
```

5. Run migrations:

```bash
python manage.py migrate
```

6. Start development server:

```bash
python manage.py runserver
```

## 🚀 Deployment on Render

1. Create a new Web Service on Render
2. Connect your GitHub repository
3. Configure the following:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn myproject.wsgi:application`
   - Environment Variables:
     - `DATABASE_URL` (from Supabase)
     - `SECRET_KEY`
     - `DEBUG=False`
     - `ALLOWED_HOSTS`

## 📁 Media Files

Media files (course images) are stored in the `media/` directory. For production, configure Render's persistent disk:

1. Add a persistent disk in Render dashboard
2. Mount it to `/media` path
3. Update your environment variables:

```
MEDIA_URL=/media/
MEDIA_ROOT=/media
```

## 🔐 Database Management

This project uses Supabase PostgreSQL database:

1. Create a new project in Supabase
2. Get the connection string from Database Settings
3. Update `DATABASE_URL` in your environment variables
4. Run migrations on deployment

## 📝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

# Django Online Course Platform

A Django-based online course platform with assessment features, deployed on Microsoft Azure.

## 🌐 Live Demo

**Application URL**: [https://django-final-project-app.azurewebsites.net/onlinecourse/](https://django-final-project-app.azurewebsites.net/onlinecourse/)

**Admin Panel**: [https://django-final-project-app.azurewebsites.net/admin/](https://django-final-project-app.azurewebsites.net/admin/)

## 📋 Project Overview

This is a Django web application for managing online courses with integrated assessment functionality. The platform allows users to:

- Browse and enroll in courses
- Take assessments and quizzes
- View course materials and content
- Track progress and results
- Administrative management through Django admin

## 🛠️ Technology Stack

- **Backend**: Django 4.2.3
- **Runtime**: Python 3.9
- **Database**: SQLite3 (development) / Azure-compatible for production
- **Static Files**: WhiteNoise middleware
- **Web Server**: Gunicorn
- **Cloud Platform**: Microsoft Azure App Service
- **Version Control**: Git/GitHub

## 🏗️ Architecture

### Project Structure
```
final-project-django/
├── myproject/                 # Django project settings
│   ├── settings.py           # Main configuration file
│   ├── urls.py              # URL routing
│   └── wsgi.py              # WSGI application
├── onlinecourse/             # Main application
│   ├── models.py            # Database models
│   ├── views.py             # View logic
│   ├── urls.py              # App-specific URLs
│   └── templates/           # HTML templates
├── static/                   # Static files (CSS, JS, images)
├── requirements.txt          # Python dependencies
├── runtime.txt              # Python version specification
├── startup.sh               # Azure deployment script
├── Procfile                 # Process configuration
└── manage.py                # Django management script
```

## 🚀 Deployment on Azure

This application is deployed on **Microsoft Azure App Service** using the **FREE tier**.

### Azure Resources
- **Resource Group**: `django-final-project-rg`
- **Location**: West Europe (optimal for Switzerland)
- **App Service Plan**: `django-final-plan` (F1 Free tier)
- **Web App**: `django-final-project-app`
- **Runtime Stack**: Python 3.9 on Linux

### Deployment Configuration

#### Production Settings
- **DEBUG**: Disabled in production
- **ALLOWED_HOSTS**: Configured for Azure domain
- **Static Files**: Managed by WhiteNoise middleware
- **Security**: Environment variables for sensitive data

#### Environment Variables
```bash
DEBUG=False
ALLOWED_HOSTS=django-final-project-app.azurewebsites.net,localhost,127.0.0.1
SCM_DO_BUILD_DURING_DEPLOYMENT=true
```

## 💻 Local Development

### Prerequisites
- Python 3.9 or higher
- pip (Python package manager)
- Git

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/johnnyadolf/final-project-django.git
   cd final-project-django
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

6. **Collect static files**
   ```bash
   python manage.py collectstatic --noinput
   ```

7. **Start development server**
   ```bash
   python manage.py runserver
   ```

8. **Access the application**
   - Main app: http://localhost:8000/onlinecourse/
   - Admin panel: http://localhost:8000/admin/

## 📦 Dependencies

### Core Dependencies
- `Django==4.2.3` - Web framework
- `Pillow==10.0.0` - Image processing
- `gunicorn==20.1.0` - WSGI HTTP Server
- `whitenoise==6.5.0` - Static file serving
- `jinja2==3.0` - Template engine

### Development Dependencies
- `wheel==0.41.1` - Package building
- `click==8.0.4` - Command line interface

See `requirements.txt` for complete list.

## 🗄️ Database Schema

### ER Diagram
For reference, here's the ER diagram design for the assessment feature:

![Onlinecourse ER Diagram](https://github.com/ibm-developer-skills-network/final-cloud-app-with-database/blob/master/static/media/course_images/onlinecourse_app_er.png)

### Key Models
- **Course**: Course information and metadata
- **Lesson**: Individual lessons within courses
- **Question**: Assessment questions
- **Choice**: Multiple choice options
- **Submission**: User assessment submissions
- **User**: Django's built-in user model for authentication

## 🔧 Configuration

### Settings Overview
The application uses environment-based configuration:

- **Development**: Uses local SQLite database, DEBUG=True
- **Production**: Uses environment variables, DEBUG=False, WhiteNoise for static files

### Key Configuration Files
- `myproject/settings.py` - Main Django settings
- `requirements.txt` - Python package dependencies
- `runtime.txt` - Python version specification
- `startup.sh` - Azure deployment automation script
- `Procfile` - Process type declarations

## 🌟 Features

### For Students
- Course browsing and enrollment
- Interactive lessons and content
- Assessment taking with immediate feedback
- Progress tracking
- User authentication and profiles

### For Administrators
- Course content management
- User management
- Assessment creation and management
- Analytics and reporting (via Django admin)

## 🔒 Security Features

- Environment-based secret key management
- CSRF protection enabled
- Secure cookie configuration
- XSS protection headers
- SQL injection prevention through Django ORM

## 📱 Responsive Design

The application is designed to work across different devices:
- Desktop computers
- Tablets
- Mobile phones

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Create a Pull Request

## 📝 License

This project is licensed under the terms specified in the `LICENSE` file.

## 🆘 Support

For questions or issues:
1. Check the existing GitHub issues
2. Create a new issue with detailed description
3. Include steps to reproduce any bugs

## 📊 Deployment Status

- ✅ **Production**: Deployed on Azure App Service
- ✅ **Status**: Running
- ✅ **Health Check**: Operational
- ✅ **SSL**: Enabled (Azure managed)
- ✅ **Domain**: django-final-project-app.azurewebsites.net

---

**Last Updated**: September 2025  
**Deployed on**: Microsoft Azure App Service (Free Tier)  
**Repository**: https://github.com/johnnyadolf/final-project-django

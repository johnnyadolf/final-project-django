# Azure Deployment Guide

## Prerequisites
- Azure CLI installed (`az --version` to check)
- Git repository initialized and committed
- Azure subscription with appropriate permissions

## Deployment Steps

### 1. Login to Azure
```bash
az login
```

### 2. Create Resource Group
```bash
az group create --name django-rg --location "East US"
```

### 3. Create App Service Plan
```bash
az appservice plan create --name django-plan --resource-group django-rg --sku B1 --is-linux
```

### 4. Create Web App
```bash
az webapp create --resource-group django-rg --plan django-plan --name YOUR-APP-NAME --runtime "PYTHON|3.9" --deployment-local-git
```

### 5. Configure Environment Variables
```bash
az webapp config appsettings set --resource-group django-rg --name YOUR-APP-NAME --settings \
    DEBUG=False \
    SECRET_KEY='your-secret-key-here' \
    ALLOWED_HOSTS='YOUR-APP-NAME.azurewebsites.net' \
    DJANGO_SETTINGS_MODULE='myproject.settings'
```

### 6. Set Startup Command
```bash
az webapp config set --resource-group django-rg --name YOUR-APP-NAME --startup-file "startup.sh"
```

### 7. Deploy Code
```bash
# Add Azure remote
git remote add azure https://YOUR-APP-NAME.scm.azurewebsites.net/YOUR-APP-NAME.git

# Deploy
git push azure main
```

## Testing Checklist

After deployment, test these URLs and functions:

### Basic Routing
- [ ] `https://YOUR-APP-NAME.azurewebsites.net/` → Should redirect to course list
- [ ] `https://YOUR-APP-NAME.azurewebsites.net/onlinecourse/` → Course list page
- [ ] `https://YOUR-APP-NAME.azurewebsites.net/admin/` → Django admin login

### User Authentication
- [ ] Registration: `https://YOUR-APP-NAME.azurewebsites.net/onlinecourse/registration/`
- [ ] Login: `https://YOUR-APP-NAME.azurewebsites.net/onlinecourse/login/`
- [ ] Logout functionality

### Course Functionality
- [ ] Course detail pages work
- [ ] Course enrollment works
- [ ] Exam submission works
- [ ] Exam results display correctly

### Static Files
- [ ] CSS files load correctly
- [ ] Bootstrap styling appears properly
- [ ] No 404 errors for static assets

## Common Issues & Troubleshooting

### 1. Static Files Not Loading
- Check WhiteNoise configuration in settings.py
- Verify STATIC_URL and STATIC_ROOT settings
- Run `python manage.py collectstatic` locally first

### 2. Database Issues
- SQLite database will be created in /tmp/ directory
- Data will be lost on app restart (consider PostgreSQL for production)

### 3. CSRF Issues
- Verify CSRF_TRUSTED_ORIGINS includes your domain
- Check that {% csrf_token %} is in all forms

### 4. Application Won't Start
- Check logs: `az webapp log tail --resource-group django-rg --name YOUR-APP-NAME`
- Verify startup.sh has execute permissions
- Check requirements.txt for missing dependencies

## Monitoring Commands

```bash
# View logs
az webapp log tail --resource-group django-rg --name YOUR-APP-NAME

# Check app status
az webapp show --resource-group django-rg --name YOUR-APP-NAME --query "state"

# Restart app
az webapp restart --resource-group django-rg --name YOUR-APP-NAME
```

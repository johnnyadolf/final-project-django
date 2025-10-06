#!/bin/bash
set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Banner
echo -e "${BLUE}"
echo "╔══════════════════════════════════════════════╗"
echo "║   Azure Deployment Script for Django App    ║"
echo "║          Django Online Course                ║"
echo "╚══════════════════════════════════════════════╝"
echo -e "${NC}"

# Check if Azure CLI is installed
if ! command -v az &> /dev/null; then
    echo -e "${RED}Error: Azure CLI is not installed!${NC}"
    echo "Install it with: brew install azure-cli"
    exit 1
fi

echo -e "${GREEN}✓ Azure CLI found${NC}"

# Check if logged in to Azure
if ! az account show &> /dev/null; then
    echo -e "${YELLOW}Please login to Azure...${NC}"
    az login
fi

echo -e "${GREEN}✓ Logged in to Azure${NC}"

# Configuration
echo ""
echo -e "${BLUE}=== Configuration ===${NC}"
echo ""

# Generate unique app name
DEFAULT_APP_NAME="django-course-$(whoami)-$RANDOM"

read -p "Enter App Name (default: $DEFAULT_APP_NAME): " APP_NAME
APP_NAME=${APP_NAME:-$DEFAULT_APP_NAME}

# Make app name lowercase and remove invalid characters
APP_NAME=$(echo "$APP_NAME" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9-]/-/g')

read -p "Enter Resource Group Name (default: myDjangoRG): " RESOURCE_GROUP
RESOURCE_GROUP=${RESOURCE_GROUP:-myDjangoRG}

read -p "Enter Azure Location (default: eastus): " LOCATION
LOCATION=${LOCATION:-eastus}

echo ""
echo -e "${YELLOW}Selected Configuration:${NC}"
echo "  App Name: $APP_NAME"
echo "  Resource Group: $RESOURCE_GROUP"
echo "  Location: $LOCATION"
echo "  App URL: https://${APP_NAME}.azurewebsites.net"
echo ""

read -p "Continue with this configuration? (yes/no): " CONFIRM
if [[ ! "$CONFIRM" =~ ^[Yy][Ee]?[Ss]?$ ]]; then
    echo -e "${RED}Deployment cancelled.${NC}"
    exit 1
fi

# Generate SECRET_KEY
echo ""
echo -e "${BLUE}=== Generating SECRET_KEY ===${NC}"
SECRET_KEY=$(python3 -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')
echo -e "${GREEN}✓ SECRET_KEY generated${NC}"

# Database configuration
echo ""
echo -e "${BLUE}=== Database Configuration ===${NC}"
echo ""
echo "Choose your database option:"
echo "1) Supabase (Recommended - Free forever, 500MB)"
echo "2) ElephantSQL (Free tier - 20MB)"
echo "3) Neon (Free tier - 0.5GB)"
echo "4) I'll provide my own DATABASE_URL"
echo "5) Skip for now (use SQLite temporarily)"
echo ""

read -p "Select option (1-5): " DB_OPTION

case $DB_OPTION in
    1)
        echo ""
        echo -e "${YELLOW}Supabase Setup:${NC}"
        echo "1. Go to https://supabase.com/"
        echo "2. Sign up and create a new project"
        echo "3. Go to Project Settings → Database"
        echo "4. Copy the 'Connection string' under 'Connection pooling'"
        echo ""
        read -p "Enter your Supabase DATABASE_URL: " DATABASE_URL
        ;;
    2)
        echo ""
        echo -e "${YELLOW}ElephantSQL Setup:${NC}"
        echo "1. Go to https://www.elephantsql.com/"
        echo "2. Sign up and create a new 'Tiny Turtle' instance (free)"
        echo "3. Copy the URL from the details page"
        echo ""
        read -p "Enter your ElephantSQL URL: " DATABASE_URL
        ;;
    3)
        echo ""
        echo -e "${YELLOW}Neon Setup:${NC}"
        echo "1. Go to https://neon.tech/"
        echo "2. Sign up and create a new project"
        echo "3. Copy the connection string"
        echo ""
        read -p "Enter your Neon DATABASE_URL: " DATABASE_URL
        ;;
    4)
        echo ""
        read -p "Enter your DATABASE_URL: " DATABASE_URL
        ;;
    5)
        echo -e "${YELLOW}Warning: Using SQLite is not recommended for production!${NC}"
        DATABASE_URL=""
        ;;
    *)
        echo -e "${RED}Invalid option. Using SQLite (not recommended for production).${NC}"
        DATABASE_URL=""
        ;;
esac

# Create Resource Group
echo ""
echo -e "${BLUE}=== Creating Resource Group ===${NC}"
if az group show --name $RESOURCE_GROUP &> /dev/null; then
    echo -e "${YELLOW}Resource group $RESOURCE_GROUP already exists${NC}"
else
    az group create --name $RESOURCE_GROUP --location $LOCATION
    echo -e "${GREEN}✓ Resource group created${NC}"
fi

# Create App Service Plan (F1 - Free tier)
echo ""
echo -e "${BLUE}=== Creating App Service Plan (Free Tier) ===${NC}"
az appservice plan create \
  --name "${APP_NAME}-plan" \
  --resource-group $RESOURCE_GROUP \
  --location $LOCATION \
  --sku F1 \
  --is-linux
echo -e "${GREEN}✓ App Service Plan created${NC}"

# Create Web App
echo ""
echo -e "${BLUE}=== Creating Web App ===${NC}"
az webapp create \
  --resource-group $RESOURCE_GROUP \
  --plan "${APP_NAME}-plan" \
  --name $APP_NAME \
  --runtime "PYTHON:3.9"
echo -e "${GREEN}✓ Web App created${NC}"

# Configure App Settings
echo ""
echo -e "${BLUE}=== Configuring Environment Variables ===${NC}"

if [ -z "$DATABASE_URL" ]; then
    # No database URL provided
    az webapp config appsettings set \
      --resource-group $RESOURCE_GROUP \
      --name $APP_NAME \
      --settings \
        SECRET_KEY="$SECRET_KEY" \
        DEBUG="False" \
        ALLOWED_HOSTS="${APP_NAME}.azurewebsites.net" \
        CSRF_TRUSTED_ORIGINS="https://${APP_NAME}.azurewebsites.net" \
        SCM_DO_BUILD_DURING_DEPLOYMENT="true" \
        WEBSITE_HTTPLOGGING_RETENTION_DAYS="7" \
      --output none
else
    # Database URL provided
    az webapp config appsettings set \
      --resource-group $RESOURCE_GROUP \
      --name $APP_NAME \
      --settings \
        SECRET_KEY="$SECRET_KEY" \
        DATABASE_URL="$DATABASE_URL" \
        DEBUG="False" \
        ALLOWED_HOSTS="${APP_NAME}.azurewebsites.net" \
        CSRF_TRUSTED_ORIGINS="https://${APP_NAME}.azurewebsites.net" \
        SCM_DO_BUILD_DURING_DEPLOYMENT="true" \
        WEBSITE_HTTPLOGGING_RETENTION_DAYS="7" \
      --output none
fi

echo -e "${GREEN}✓ Environment variables configured${NC}"

# Configure Startup Command
echo ""
echo -e "${BLUE}=== Configuring Startup Command ===${NC}"
az webapp config set \
  --resource-group $RESOURCE_GROUP \
  --name $APP_NAME \
  --startup-file "startup.sh" \
  --output none
echo -e "${GREEN}✓ Startup command configured${NC}"

# Enable Application Logging
echo ""
echo -e "${BLUE}=== Enabling Application Logging ===${NC}"
az webapp log config \
  --name $APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --application-logging filesystem \
  --detailed-error-messages true \
  --failed-request-tracing true \
  --web-server-logging filesystem \
  --output none
echo -e "${GREEN}✓ Logging enabled${NC}"

# Setup Git Deployment
echo ""
echo -e "${BLUE}=== Setting up Git Deployment ===${NC}"

# Check if git is initialized
if [ ! -d .git ]; then
    echo "Initializing git repository..."
    git init
    git add .
    git commit -m "Initial commit for Azure deployment"
fi

# Get deployment URL
DEPLOY_URL=$(az webapp deployment source config-local-git \
  --name $APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --query url --output tsv)

# Check if azure remote already exists
if git remote | grep -q "^azure$"; then
    echo "Updating azure remote..."
    git remote set-url azure "$DEPLOY_URL"
else
    echo "Adding azure remote..."
    git remote add azure "$DEPLOY_URL"
fi

echo -e "${GREEN}✓ Git deployment configured${NC}"

# Deploy to Azure
echo ""
echo -e "${BLUE}=== Deploying to Azure ===${NC}"
echo -e "${YELLOW}This may take 5-10 minutes...${NC}"
echo ""

# Get current branch
CURRENT_BRANCH=$(git branch --show-current)
if [ -z "$CURRENT_BRANCH" ]; then
    CURRENT_BRANCH="main"
fi

echo "Pushing to Azure (branch: $CURRENT_BRANCH)..."
if git push azure $CURRENT_BRANCH:master -f; then
    echo -e "${GREEN}✓ Code deployed successfully${NC}"
else
    echo -e "${RED}Deployment encountered an error. Check logs with:${NC}"
    echo "az webapp log tail --name $APP_NAME --resource-group $RESOURCE_GROUP"
    exit 1
fi

# Wait for deployment to complete
echo ""
echo "Waiting for deployment to complete..."
sleep 30

# Check deployment status
echo ""
echo -e "${BLUE}=== Checking Deployment ===${NC}"
APP_URL="https://${APP_NAME}.azurewebsites.net"
HEALTH_URL="${APP_URL}/onlinecourse/health/"

echo "Testing health endpoint: $HEALTH_URL"
for i in {1..10}; do
    if curl -s -o /dev/null -w "%{http_code}" "$HEALTH_URL" | grep -q "200\|503"; then
        echo -e "${GREEN}✓ Application is responding${NC}"
        break
    fi
    echo "Waiting for app to start... ($i/10)"
    sleep 10
done

# Final output
echo ""
echo -e "${GREEN}"
echo "╔══════════════════════════════════════════════╗"
echo "║          Deployment Successful! 🎉           ║"
echo "╚══════════════════════════════════════════════╝"
echo -e "${NC}"
echo ""
echo -e "${BLUE}Your Application Details:${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo -e "${GREEN}App URL:${NC}        $APP_URL"
echo -e "${GREEN}Admin Panel:${NC}    ${APP_URL}/admin/"
echo -e "${GREEN}Health Check:${NC}   $HEALTH_URL"
echo ""
echo -e "${BLUE}Resource Details:${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo -e "${GREEN}App Name:${NC}       $APP_NAME"
echo -e "${GREEN}Resource Group:${NC} $RESOURCE_GROUP"
echo -e "${GREEN}Location:${NC}       $LOCATION"
echo ""
echo -e "${BLUE}Next Steps:${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "1. Create admin user:"
echo "   ${YELLOW}az webapp ssh --name $APP_NAME --resource-group $RESOURCE_GROUP${NC}"
echo "   ${YELLOW}python manage.py createsuperuser${NC}"
echo ""
echo "2. View logs:"
echo "   ${YELLOW}az webapp log tail --name $APP_NAME --resource-group $RESOURCE_GROUP${NC}"
echo ""
echo "3. Open your app:"
echo "   ${YELLOW}az webapp browse --name $APP_NAME --resource-group $RESOURCE_GROUP${NC}"
echo ""
echo "4. Update your app:"
echo "   ${YELLOW}git push azure main${NC}"
echo ""
echo -e "${BLUE}Useful Commands:${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Restart app:  ${YELLOW}az webapp restart --name $APP_NAME --resource-group $RESOURCE_GROUP${NC}"
echo "Stop app:     ${YELLOW}az webapp stop --name $APP_NAME --resource-group $RESOURCE_GROUP${NC}"
echo "Start app:    ${YELLOW}az webapp start --name $APP_NAME --resource-group $RESOURCE_GROUP${NC}"
echo "Delete all:   ${YELLOW}az group delete --name $RESOURCE_GROUP --yes${NC}"
echo ""
echo -e "${GREEN}Deployment script completed successfully!${NC}"
echo ""

# Save deployment info to file
cat > deployment_info.txt << EOF
Azure Deployment Information
============================

Deployment Date: $(date)

Application Details:
- App Name: $APP_NAME
- Resource Group: $RESOURCE_GROUP
- Location: $LOCATION
- App URL: $APP_URL
- Admin URL: ${APP_URL}/admin/
- Health Check: $HEALTH_URL

Azure Commands:
- View logs: az webapp log tail --name $APP_NAME --resource-group $RESOURCE_GROUP
- SSH access: az webapp ssh --name $APP_NAME --resource-group $RESOURCE_GROUP
- Restart: az webapp restart --name $APP_NAME --resource-group $RESOURCE_GROUP
- Delete: az group delete --name $RESOURCE_GROUP --yes

Git Commands:
- Update app: git push azure main
- View remotes: git remote -v

Notes:
- Free tier (F1) has 60 CPU minutes/day limit
- App will sleep if limit exceeded
- Upgrade to B1 tier ($13/month) for always-on

EOF

echo -e "${GREEN}✓ Deployment info saved to deployment_info.txt${NC}"
echo ""

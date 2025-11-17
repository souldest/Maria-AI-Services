#!/bin/bash
# create-containerapps.sh
# Script zum Erstellen/Updaten von Azure Container Apps für Backend und Frontend
# Nutzt GitHub Secrets für ACR-Login und Credentials
# Vorher müssen die Secrets ACR_USERNAME, ACR_PASSWORD in GitHub Actions gesetzt werden

set -e

# ==== Parameter ====
RESOURCE_GROUP="maria-ai-service-001_group"
ENV_NAME="maria-ai-env"
LOCATION="westeurope"

BACKEND_APP="forecast-backend-app"
FRONTEND_APP="forecast-frontend-app"

ACR_NAME="${ACR_USERNAME}"  # GitHub Secret
ACR_USERNAME="${ACR_USERNAME}" # GitHub Secret
ACR_PASSWORD="${ACR_PASSWORD}" # GitHub Secret

BACKEND_IMAGE="$ACR_NAME.azurecr.io/forecast-backend:latest"
FRONTEND_IMAGE="$ACR_NAME.azurecr.io/forecast-frontend:latest"

# ==== ACR Login ====
echo "Login to Azure Container Registry..."
echo "$ACR_PASSWORD" | docker login "$ACR_NAME.azurecr.io" -u "$ACR_USERNAME" --password-stdin

# ==== Backend Container App ====
if az containerapp show --name "$BACKEND_APP" --resource-group "$RESOURCE_GROUP" &>/dev/null; then
    echo "Backend Container App existiert bereits. Updating image..."
    az containerapp update \
        --name "$BACKEND_APP" \
        --resource-group "$RESOURCE_GROUP" \
        --image "$BACKEND_IMAGE" \
        --environment "$ENV_NAME"
else
    echo "Erstelle Backend Container App..."
    az containerapp create \
        --name "$BACKEND_APP" \
        --resource-group "$RESOURCE_GROUP" \
        --environment "$ENV_NAME" \
        --image "$BACKEND_IMAGE" \
        --target-port 8000 \
        --ingress 'external'
fi

# ==== Frontend Container App ====
if az containerapp show --name "$FRONTEND_APP" --resource-group "$RESOURCE_GROUP" &>/dev/null; then
    echo "Frontend Container App existiert bereits. Updating image..."
    az containerapp update \
        --name "$FRONTEND_APP" \
        --resource-group "$RESOURCE_GROUP" \
        --image "$FRONTEND_IMAGE" \
        --environment "$ENV_NAME"
else
    echo "Erstelle Frontend Container App..."
    az containerapp create \
        --name "$FRONTEND_APP" \
        --resource-group "$RESOURCE_GROUP" \
        --environment "$ENV_NAME" \
        --image "$FRONTEND_IMAGE" \
        --target-port 8501 \
        --ingress 'external'
fi

echo "✅ Backend und Frontend Container Apps sind bereit."

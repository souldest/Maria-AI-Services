#!/bin/bash
set -e

# -----------------------------
# Variablen
# -----------------------------
ACR_NAME="mariaairegistry001"
BACKEND_APP="forecast-backend-app"
FRONTEND_APP="forecast-frontend-app"
RESOURCE_GROUP="maria-ai-service-001_group"
ENVIRONMENT="maria-ai-env"

# GitHub Secrets in der Shell verfügbar machen:
# export ACR_PASSWORD="..." (nur lokal zum Testen)
# export ACR_USERNAME=$ACR_NAME

# -----------------------------
# Docker Login
# -----------------------------
echo "Login to ACR..."
echo $ACR_PASSWORD | docker login $ACR_NAME.azurecr.io -u $ACR_NAME --password-stdin

# -----------------------------
# Build Docker Images
# -----------------------------
echo "Building backend image..."
docker build -t $ACR_NAME.azurecr.io/$BACKEND_APP:latest ./backend

echo "Building frontend image..."
docker build -t $ACR_NAME.azurecr.io/$FRONTEND_APP:latest ./frontend

# -----------------------------
# Push Docker Images to ACR
# -----------------------------
echo "Pushing backend image..."
docker push $ACR_NAME.azurecr.io/$BACKEND_APP:latest

echo "Pushing frontend image..."
docker push $ACR_NAME.azurecr.io/$FRONTEND_APP:latest

# -----------------------------
# Create or Update Container Apps
# -----------------------------
echo "Creating or updating backend container app..."
az containerapp up \
    --name $BACKEND_APP \
    --resource-group $RESOURCE_GROUP \
    --environment $ENVIRONMENT \
    --image $ACR_NAME.azurecr.io/$BACKEND_APP:latest \
    --target-port 8000 \
    --ingress external \
    --cpu 0.5 --memory 1.0Gi

echo "Creating or updating frontend container app..."
az containerapp up \
    --name $FRONTEND_APP \
    --resource-group $RESOURCE_GROUP \
    --environment $ENVIRONMENT \
    --image $ACR_NAME.azurecr.io/$FRONTEND_APP:latest \
    --target-port 8501 \
    --ingress external \
    --cpu 0.5 --memory 1.0Gi

echo "✅ All done! Container Apps are ready."

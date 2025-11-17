#!/bin/bash
# create-containerapps.sh
# Script to create/update Azure Container Apps for backend and frontend
# Expects ACR credentials and app/environment names to be set as environment variables

set -e

# Required environment variables:
# ACR_NAME, BACKEND_APP, FRONTEND_APP, RESOURCE_GROUP, ENVIRONMENT_NAME, ACR_PASSWORD

if [ -z "$ACR_NAME" ] || [ -z "$BACKEND_APP" ] || [ -z "$FRONTEND_APP" ] || [ -z "$RESOURCE_GROUP" ] || [ -z "$ENVIRONMENT_NAME" ] || [ -z "$ACR_PASSWORD" ]; then
  echo "One or more required environment variables are not set."
  echo "Please set ACR_NAME, BACKEND_APP, FRONTEND_APP, RESOURCE_GROUP, ENVIRONMENT_NAME, and ACR_PASSWORD"
  exit 1
fi

# Login to Azure Container Registry
echo "Logging into ACR $ACR_NAME..."
echo "$ACR_PASSWORD" | docker login "$ACR_NAME.azurecr.io" -u "$ACR_NAME" --password-stdin

# Create/Update Backend Container App
if az containerapp show --name "$BACKEND_APP" --resource-group "$RESOURCE_GROUP" &>/dev/null; then
  echo "Backend Container App exists. Updating image..."
else
  echo "Creating Backend Container App..."
  az containerapp create \
    --name "$BACKEND_APP" \
    --resource-group "$RESOURCE_GROUP" \
    --image "$ACR_NAME.azurecr.io/$BACKEND_APP:latest" \
    --environment "$ENVIRONMENT_NAME" \
    --ingress 'external' \
    --target-port 8000
fi

# Update Backend image
az containerapp update \
  --name "$BACKEND_APP" \
  --resource-group "$RESOURCE_GROUP" \
  --image "$ACR_NAME.azurecr.io/$BACKEND_APP:latest"

# Create/Update Frontend Container App
if az containerapp show --name "$FRONTEND_APP" --resource-group "$RESOURCE_GROUP" &>/dev/null; then
  echo "Frontend Container App exists. Updating image..."
else
  echo "Creating Frontend Container App..."
  az containerapp create \
    --name "$FRONTEND_APP" \
    --resource-group "$RESOURCE_GROUP" \
    --image "$ACR_NAME.azurecr.io/$FRONTEND_APP:latest" \
    --environment "$ENVIRONMENT_NAME" \
    --ingress 'external' \
    --target-port 8501
fi

# Update Frontend image
az containerapp update \
  --name "$FRONTEND_APP" \
  --resource-group "$RESOURCE_GROUP" \
  --image "$ACR_NAME.azurecr.io/$FRONTEND_APP:latest"

echo "✅ Container Apps are ready."

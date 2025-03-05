#!/bin/bash

cd /sandbox/project/

echo "🏗️ Running Ant build..."
ant compile || { echo "❌ Build failed!"; exit 1; }

echo "🚀 Deploying to WebLogic..."
ant deploy || { echo "❌ Deployment failed!"; exit 1; }

echo "✅ Build and deployment completed!"

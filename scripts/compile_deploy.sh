#!/bin/bash

cd /sandbox/project/src_eclipse/TCSWeb

echo "🏗️ Running Ant build..."
ant package-war-wls || { echo "❌ Build failed!"; exit 1; }

# Note: Deployment target is part of package-war-wls in TCSWeb's build.xml
echo "✅ Build and deployment completed!"

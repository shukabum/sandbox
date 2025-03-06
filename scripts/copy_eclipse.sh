#!/bin/bash

# Create necessary directories
mkdir -p /sandbox/project/src

# Copy src_eclipse contents to project/src
cp -r /sandbox/input/src_eclipse/* /sandbox/project/src/

# Set proper permissions
chmod -R 755 /sandbox/project/src/

echo "✅ Copied src_eclipse files to project directory" 
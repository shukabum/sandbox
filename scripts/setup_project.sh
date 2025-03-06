#!/bin/bash

# Create necessary directories
mkdir -p /sandbox/project/src_eclipse/TCSWeb/{src,WebContent,build,lib/provided,lib_module/ext}



# Set proper permissions
chmod -R 755 /sandbox/project/src_eclipse/

# Create build.properties if it doesn't exist
if [ ! -f "/sandbox/project/src_eclipse/TCSWeb/build.properties" ]; then
    cat > "/sandbox/project/src_eclipse/TCSWeb/build.properties" << 'EOF'
provided.dir=lib/provided
ext.dir=lib_module/ext
build.dir=./build
source.dir=./src
generator.dir=./generator
output.dir=${build.dir}/classes
javac.debug=off
web.dir=./WebContent
war.name=TCSWeb.war
war2.name=TCSWebMnt.war
war3.name=TCSWebITA.war
war4.name=TCSWebITAPre.war
war5.name=TCSWebITASub.war
war6.name=TCSWebITAPreSub.war
EOF
    echo "✅ Created build.properties file"
fi 
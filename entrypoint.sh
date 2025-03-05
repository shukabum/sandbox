#!/bin/bash

exec > >(tee -a /sandbox/logs/sandbox.log) 2>&1

echo "🚀 Sandbox Started!"

cd /sandbox/project

# Apply LLM changes
echo "🛠️ Applying LLM-suggested changes..."
python3 /sandbox/scripts/apply_changes.py

# Validate the modified code
echo "✅ Validating the code..."
python3 /sandbox/scripts/validate_code.py

# Create build.xml if it doesn't exist
if [ ! -f "build.xml" ]; then
    echo "📝 Creating build.xml..."
    cat > build.xml << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<project name="sandbox" default="compile">
    <!-- Define properties -->
    <property name="src.dir" value="src"/>
    <property name="build.dir" value="build"/>
    <property name="classes.dir" value="${build.dir}/classes"/>

    <!-- Clean target -->
    <target name="clean">
        <delete dir="${build.dir}"/>
    </target>

    <!-- Initialize target -->
    <target name="init">
        <mkdir dir="${build.dir}"/>
        <mkdir dir="${classes.dir}"/>
    </target>

    <!-- Compile target -->
    <target name="compile" depends="init">
        <javac srcdir="${src.dir}" destdir="${classes.dir}" includeantruntime="false"/>
    </target>

    <!-- Deploy target -->
    <target name="deploy" depends="compile">
        <echo>Deployment step - configure as needed</echo>
    </target>
</project>
EOF
fi

# Compile & Deploy
echo "🏗️ Compiling and deploying..."
/sandbox/scripts/compile_deploy.sh

echo "🎯 Process Complete!"

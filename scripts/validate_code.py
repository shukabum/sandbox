import subprocess
import os
import json

def validate_file_syntax(file_path):
    if file_path.endswith('.java'):
        # Check Java syntax
        result = subprocess.run(['javac', '-d', '/tmp', file_path], 
                              capture_output=True, text=True)
        return result.returncode == 0, result.stderr
    
    elif file_path.endswith('.xhtml'):
        # Basic XML validation
        try:
            import xml.etree.ElementTree as ET
            ET.parse(file_path)
            return True, ""
        except ET.ParseError as e:
            return False, str(e)
    
    elif file_path.endswith('.css'):
        # Basic CSS validation (check for matching braces)
        with open(file_path, 'r') as f:
            content = f.read()
            if content.count('{') != content.count('}'):
                return False, "Mismatched braces in CSS"
    return True, ""

def analyze_dependencies(file_path):
    """Scan file for import statements and dependencies"""
    dependencies = []
    if file_path.endswith('.java'):
        with open(file_path, 'r') as f:
            for line in f:
                if line.strip().startswith('import'):
                    dependencies.append(line.strip().split()[1].rstrip(';'))
    return dependencies

def validate_java_with_classpath(file_path, classpath):
    """Validate Java file with dependencies"""
    result = subprocess.run(
        ['javac', '-cp', classpath, file_path],
        capture_output=True, 
        text=True
    )
    return result.returncode == 0, result.stderr

print("🔍 Validating modified files...")

# Read changes.json to know which files to validate
with open("/sandbox/input/changes.json") as f:
    changes = json.load(f)["changes"]

all_valid = True
for change in changes:
    file_path = os.path.join("/sandbox/project", change["path"].lstrip("/"))
    print(f"Checking {file_path}...")
    is_valid, error = validate_file_syntax(file_path)
    if not is_valid:
        print(f"❌ Validation failed for {file_path}: {error}")
        all_valid = False

if not all_valid:
    print("❌ Code validation failed!")
    exit(1)

# Finally run the ant build
print("🔍 Running full build validation...")
result = subprocess.run(["ant", "package-war-wls"], cwd="/sandbox/project/src_eclipse/TCSWeb", capture_output=True, text=True)

if result.returncode == 0:
    print("✅ Code validation successful!")
else:
    print("❌ Build validation failed!\n", result.stderr)
    exit(1)

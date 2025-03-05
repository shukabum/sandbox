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
result = subprocess.run(["ant", "compile"], cwd="/sandbox/project/", capture_output=True, text=True)

if result.returncode == 0:
    print("✅ Code validation successful!")
else:
    print("❌ Build validation failed!\n", result.stderr)
    exit(1)

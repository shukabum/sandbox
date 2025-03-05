import json
import os
import re

JSON_FILE = "/sandbox/input/changes.json"
PROJECT_DIR = "/sandbox/project/"

def format_css_content(content, indent_level=0):
    """Format CSS content with proper indentation"""
    indent = "    " * indent_level
    formatted = []
    for line in content:
        # Don't indent closing braces
        if line.strip() == "}":
            formatted.append("}\n")
        else:
            formatted.append(f"{indent}{line}\n")
    return formatted

def format_java_content(content):
    """Format Java content with proper indentation and ensure one statement per line"""
    formatted = []
    for line in content:
        # Split multiple statements on the same line (looking for semicolons not in strings)
        statements = re.split(r';(?=(?:[^"]*"[^"]*")*[^"]*$)', line.strip())
        for stmt in statements:
            if stmt.strip():  # If statement is not empty
                # Add proper indentation (8 spaces for statements inside methods)
                formatted_stmt = f"        {stmt.strip()};"
                formatted.append(f"{formatted_stmt}\n")
    return formatted

def format_xml_content(content):
    """Format XML/XHTML content with proper indentation"""
    formatted = []
    for line in content:
        # Preserve existing indentation for XML/XHTML
        if not line.strip().startswith('<'):
            line = f"    {line.strip()}"
        formatted.append(f"{line}\n")
    return formatted

def apply_change(file_path, change):
    try:
        # Create directories if they don't exist
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        # Read existing file or create new one
        try:
            with open(file_path, "r") as f:
                lines = f.readlines()
        except FileNotFoundError:
            lines = []

        content = change["content"]
        
        # Format content based on file type
        if file_path.endswith('.css'):
            content = format_css_content(content)
        elif file_path.endswith('.java'):
            content = format_java_content(content)
        elif file_path.endswith('.xhtml') or file_path.endswith('.xml'):
            content = format_xml_content(content)
        
        if change["change"] == "REPLACE":
            # Ensure we have enough lines to replace
            while len(lines) < change["end-line"]:
                lines.append('\n')
            lines[change["start-line"] - 1 : change["end-line"]] = content
        
        elif change["change"] == "INSERT":
            # For Java files, ensure we're not concatenating lines
            if file_path.endswith('.java'):
                # Ensure we have enough lines
                while len(lines) < change["start-line"]:
                    lines.append('\n')
                # Insert each formatted line separately
                for i, line in enumerate(reversed(content)):
                    lines.insert(change["start-line"] - 1, line)
            elif file_path.endswith('.css'):
                # CSS specific handling
                for i in range(len(lines) - 1, -1, -1):
                    if lines[i].strip() == "}":
                        lines.insert(i + 1, "\n")
                        lines[i + 2:i + 2] = content
                        break
                else:
                    if lines and not lines[-1].endswith('\n'):
                        lines.append('\n')
                    lines.extend(content)
            else:
                # Default insert behavior
                while len(lines) < change["start-line"]:
                    lines.append('\n')
                lines.insert(change["start-line"] - 1, "".join(content))
        
        elif change["change"] == "DELETE":
            if change["start-line"] <= len(lines):
                del lines[change["start-line"] - 1 : change["end-line"]]

        # Ensure file ends with exactly one newline
        while lines and not lines[-1].strip():
            lines.pop()
        lines.append('\n')

        # Write changes back to file
        with open(file_path, "w") as f:
            f.writelines(lines)
            
        return True, None
    except Exception as e:
        return False, str(e)

def main():
    try:
        with open(JSON_FILE, "r") as file:
            changes = json.load(file)["changes"]

        success = True
        for change in changes:
            file_path = os.path.join(PROJECT_DIR, change["path"].lstrip("/"))
            print(f"Applying changes to {file_path}...")
            ok, error = apply_change(file_path, change)
            if not ok:
                print(f"❌ Failed to apply change to {file_path}: {error}")
                success = False
                break

        if success:
            print("✅ Changes applied successfully!")
        else:
            print("❌ Some changes failed to apply")
            exit(1)

    except Exception as e:
        print(f"❌ Error processing changes: {str(e)}")
        exit(1)

if __name__ == "__main__":
    main()

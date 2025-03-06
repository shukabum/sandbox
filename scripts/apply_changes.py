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

def detect_indentation(lines):
    """Detect the indentation style from existing file content"""
    if not lines:
        return 4  # Default to 4 spaces
    
    # Look for lines with indentation
    indent_sizes = []
    for i in range(1, len(lines)):
        curr_line = lines[i].rstrip('\n')
        prev_line = lines[i-1].rstrip('\n')
        
        # Skip empty lines
        if not curr_line.strip() or not prev_line.strip():
            continue
            
        curr_indent = len(curr_line) - len(curr_line.lstrip())
        prev_indent = len(prev_line) - len(prev_line.lstrip())
        
        if curr_indent > prev_indent:
            indent_sizes.append(curr_indent - prev_indent)
    
    if indent_sizes:
        # Find the most common indent size
        return max(set(indent_sizes), key=indent_sizes.count)
    return 4  # Default to 4 spaces

def preserve_indent_for_replace(original_lines, content, start_line, end_line):
    """Preserve the indentation when replacing content"""
    # If no original lines, simply return content
    if not original_lines or start_line <= 0:
        return [line + "\n" for line in content]
        
    # Find the indentation of the line before start_line
    base_indent = ""
    if start_line > 1:
        prev_line_idx = start_line - 2  # -2 because start_line is 1-based
        while prev_line_idx >= 0:
            prev_line = original_lines[prev_line_idx]
            if prev_line.strip():
                # Get the whitespace at the beginning of the line
                base_indent = re.match(r'^\s*', prev_line).group(0)
                break
            prev_line_idx -= 1
    
    # Determine indentation in existing lines that are being replaced
    existing_indents = []
    for line_idx in range(max(0, start_line - 1), min(len(original_lines), end_line)):
        line = original_lines[line_idx]
        if line.strip():
            indent_match = re.match(r'^\s*', line)
            if indent_match:
                existing_indents.append(indent_match.group(0))
    
    # If we have existing indentation patterns, use them to guide new content
    indent_size = detect_indentation(original_lines)
    
    formatted_lines = []
    for i, line in enumerate(content):
        stripped = line.strip()
        if not stripped:
            formatted_lines.append('\n')
            continue
        
        # Calculate proper indentation
        indent = base_indent
        
        # If it's a closing tag or has decreasing nesting level
        if stripped.startswith('</'):
            # Use the indentation of the matching opening tag if available
            tag_name = stripped[2:].split()[0].split('>')[0]
            for j in range(i-1, -1, -1):
                if content[j].strip().startswith(f'<{tag_name}') and not content[j].strip().endswith('/>'):
                    line_indent = re.match(r'^\s*', content[j]).group(0)
                    indent = line_indent
                    break
        elif i < len(existing_indents):
            # Use existing indentation pattern if available
            indent = existing_indents[i]
        elif i > 0:
            # Otherwise base indentation on previous content
            prev_line = content[i-1].strip()
            if prev_line.startswith('<') and not prev_line.startswith('</') and not prev_line.endswith('/>'):
                # Previous line opened a tag, increase indent
                prev_indent = re.match(r'^\s*', content[i-1]).group(0)
                indent = prev_indent + ' ' * indent_size
            
        formatted_lines.append(f"{indent}{stripped}\n")
    
    return formatted_lines

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
        
        # Format content based on file type for non-REPLACE operations
        if change["change"] != "REPLACE":
            if file_path.endswith('.css'):
                content = format_css_content(content)
            elif file_path.endswith('.java'):
                content = format_java_content(content)
        
        if change["change"] == "REPLACE":
            # For REPLACE, use special handling to maintain indentation
            if file_path.endswith('.xhtml') or file_path.endswith('.xml') or file_path.endswith('.jsf'):
                formatted_content = preserve_indent_for_replace(
                    lines, content, change["start-line"], change["end-line"]
                )
            elif file_path.endswith('.css'):
                formatted_content = format_css_content(content)
            elif file_path.endswith('.java'):
                formatted_content = format_java_content(content)
            else:
                # For other file types, keep original content with newlines
                formatted_content = [line + "\n" for line in content]
                
            # Ensure we have enough lines to replace
            while len(lines) < change["end-line"]:
                lines.append('\n')
            lines[change["start-line"] - 1 : change["end-line"]] = formatted_content
        
        elif change["change"] == "ADD" or change["change"] == "INSERT":
            # Handle special case where start-line and end-line are -1
            if change["start-line"] == -1 and change["end-line"] == -1:
                if file_path.endswith('.css'):
                    # For CSS files, add at the end with a newline before
                    if lines and not lines[-1].endswith('\n'):
                        lines.append('\n')
                    lines.extend(content)
                else:
                    # For other files, just append content
                    lines.extend(content)
            else:
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
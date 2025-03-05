# Sandbox


## Project Structure

```
sandbox/
│── input/                 # Directory for input files (JSON change definitions, code files)
│   ├── changes.json       # Defines code modifications in JSON format
│   ├── sample_project/    # Example SVN-based project for testing
│── logs/                  # Logs execution progress
│── scripts/               # Helper scripts for applying and validating changes
│── docker-compose.yml     # Docker Compose configuration
│── Dockerfile             # Defines the sandbox container
│── README.md              # Documentation
```

## Setup and Installation

### 1. Clone the Repository
```bash
git clone https://github.com/TejasGupta-27/sandbox
cd sandbox
```

### 2. Build and Start the Docker Container
```bash
docker-compose up --build
```
This will:
- Build the sandbox environment
- Start the container and initialize the validation pipeline

## Usage

### 1. Define Code Changes
Modify the `input/changes.json` file to specify the changes you want to apply.

#### Example `changes.json`
```json
{
  "changes": [
    {
      "path": "/src/com/example/Main.java",
      "start-line": 5,
      "end-line": 5,
      "change": "INSERT",
      "description": "Add debug statement",
      "content": [
        "System.out.println(\"Debug: Message\");"
      ]
    }
  ]
}
```
- **`path`**: File location relative to the project root
- **`start-line` / `end-line`**: Specifies where the modification should be applied
- **`change`**: `INSERT | DELETE | REPLACE`
- **`description`**: Brief explanation of the change
- **`content`**: Code to be inserted or modified

### 2. Execute Changes
Once `changes.json` is updated, the sandbox will:
- **Apply the changes to the specified files**
- **Validate syntax and formatting**
- **Compile the code (if applicable)**
- **Deploy if all checks pass**


This will display:
- **Change application status**
- **Validation errors (if any)**
- **Compilation and test results**

## Example Workflow

1. Place your project inside the `project/` directory.
2. Define changes in `changes.json`.
3. Run the pipeline (`docker-compose up`).
4. Check logs for validation results.
5. If successful, the modified code will be ready for deployment.

## Docker Environment Details

- **Base Image:** `openjdk:11` (for Java projects)
- **Version Control:** Uses **SVN** for source management
- **Build Tool:** Uses **Apache Ant** (instead of Maven)
- **Deployment Server:** WebLogic




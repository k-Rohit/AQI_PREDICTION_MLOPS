import os

# Define the directory structure
directories = [
    'data/raw',
    'data/processed',
    'data/output',
    'notebooks',
    'scripts',
    'ml_pipelines',
    'config',
    'models',
    'ci_cd',
    'logs'
]

# Define the files to be created
files = [
    'Dockerfile',
    'requirements.txt',
    'README.md',
    'LICENSE',
    '.gitignore',
    'config/config.yaml'
]

def create_directories():
    """Create directories as per the defined structure."""
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"Created directory: {directory}")

def create_files():
    """Create empty files as per the defined structure."""
    for file in files:
        file_path = os.path.join(file)
        with open(file_path, 'w') as f:
            pass  # Create an empty file
        print(f"Created file: {file_path}")

if __name__ == "__main__":
    create_directories()
    create_files()
    print("Directory structure and files created successfully!")

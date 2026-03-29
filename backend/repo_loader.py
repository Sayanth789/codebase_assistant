import tempfile
import pathlib
from git import Repo
import os

# Supported code file extensions
SUPPORTED_EXTENSIONS = ('.py', '.c', '.cpp', '.ipynb')

def load_repo(source: str):
    """
    Load code files from a source.
    source: GitHub repo URL (ending with .git) OR local folder path.
    Returns a list of pathlib.Path objects for all code files.
    """
    # Check if the source is a local folder
    if os.path.isdir(source):
        repo_path = pathlib.Path(source)
    # Check if source is a Git URL
    elif source.startswith("http://") or source.startswith("https://"):
        temp_dir = tempfile.mkdtemp()
        try:
            print(f"Cloning repo {source} into {temp_dir}...")
            Repo.clone_from(source, temp_dir)
        except Exception as e:
            raise ValueError(f"Failed to clone repo: {e}")
        repo_path = pathlib.Path(temp_dir)
    else:
        # Invalid input
        raise ValueError(f"Source {source} is neither a valid folder nor a Git URL")

    # Recursively find code files
    code_files = [f for f in repo_path.rglob('*') if f.suffix in SUPPORTED_EXTENSIONS]

    if not code_files:
        raise FileNotFoundError(f"No code files found in {source}")

    print(f"Found {len(code_files)} code files in {repo_path}")
    return code_files
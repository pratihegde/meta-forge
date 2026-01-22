"""File management utilities"""
import os
import zipfile
from pathlib import Path
from typing import List
import shutil
from context.models import GeneratedFile


def write_files_to_disk(files: List[GeneratedFile], project_dir: Path) -> Path:
    """
    Write generated files to disk
    Returns: Path to the project directory
    """
    # Create project directory
    project_dir.mkdir(parents=True, exist_ok=True)
    
    for file in files:
        # Sanitize path: strip leading slashes and drive letters
        clean_path = file.path.lstrip('/\\').split(':')[-1].lstrip('/\\')
        file_path = project_dir / clean_path
        
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(file.content)
    
    return project_dir


def create_zip_archive(project_dir: Path, output_path: Path) -> Path:
    """
    Create a ZIP archive of the project
    Returns: Path to the ZIP file
    """
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(project_dir):
            for file in files:
                file_path = Path(root) / file
                arcname = file_path.relative_to(project_dir.parent)
                zipf.write(file_path, arcname)
    
    return output_path


def cleanup_old_projects(output_dir: Path, keep_recent: int = 5):
    """
    Clean up old project directories, keeping only the most recent ones
    """
    if not output_dir.exists():
        return
    
    # Get all project directories sorted by modification time
    projects = sorted(
        [d for d in output_dir.iterdir() if d.is_dir()],
        key=lambda x: x.stat().st_mtime,
        reverse=True
    )
    
    # Remove old projects
    for project in projects[keep_recent:]:
        shutil.rmtree(project, ignore_errors=True)


def get_file_icon(language: str) -> str:
    """Get an icon/emoji for a file type"""
    icons = {
        "python": "🐍",
        "javascript": "📜",
        "html": "🌐",
        "css": "🎨",
        "json": "📋",
        "txt": "📄",
        "md": "📝"
    }
    return icons.get(language.lower(), "📄")

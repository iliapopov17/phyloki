import shutil
from pathlib import Path

# Get the path to the current directory (same location as the script)
current_dir = Path(__file__).resolve().parent
pycache_dir = current_dir / "__pycache__"

# Check if __pycache__ exists and remove it
if pycache_dir.exists() and pycache_dir.is_dir():
    shutil.rmtree(pycache_dir)
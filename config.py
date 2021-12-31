import os
from pathlib import Path
import tempfile
import json

app_dir = Path(os.path.dirname(os.path.realpath(__file__)))
config_file = app_dir / "config.json"

local_config = {}
with config_file.open("r", encoding="utf-8") as f:
    local_config = json.load(f)

TEMPFOLDER: Path = Path(tempfile.gettempdir())

files_folder = app_dir / "files"


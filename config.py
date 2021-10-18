import os
from pathlib import Path
import tempfile
import tempfile
from dotenv import load_dotenv
load_dotenv()

app_dir = Path(os.path.dirname(os.path.realpath(__file__)))

SECRETKEY: str = os.getenv("SECRETKEY") or ""

TEMPFOLDER: Path = Path(tempfile.gettempdir())

files_folder = app_dir / "files"

dongle_ids: list[str] = ["1d6b:0003"]

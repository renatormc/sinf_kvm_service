import os
from pathlib import Path
import tempfile
from dotenv import load_dotenv
load_dotenv()

app_dir = Path(os.path.dirname(os.path.realpath(__file__)))

TOKEN: str = os.getenv("TOKEN") or ""
PORT: str = os.getenv("PORT") or ""

TEMPFOLDER: Path = Path(tempfile.gettempdir())

files_folder = app_dir / "files"

fixed_usbs_filepath = app_dir / "fixed_usbs.json"

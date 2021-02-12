import os
from pathlib import Path
import tempfile
import tempfile
from dotenv import load_dotenv
load_dotenv()

app_dir = Path(os.path.dirname(os.path.realpath(__file__)))

SECRET_KEY = os.getenv("SINFKEY")

TEMPFOLDER = Path(tempfile.gettempdir())

files_folder = app_dir / "files"

dongle_vendors = ["1d6b:0003"]
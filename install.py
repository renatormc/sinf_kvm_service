import subprocess
from pathlib import Path
import os

user = os.getenv("SUDO_USER")
dir_ = os.getcwd()
pipenv_path = subprocess.getoutput("which pipenv")

text = f"""[Unit]
Description=Sinf KVM Service
After=network.target

[Service]
User={user}
Group={user}
WorkingDirectory={dir_}
ExecStart={pipenv_path} run gunicorn --workers 3 --bind 0.0.0.0:8002 app:app

[Install]
WantedBy=multi-user.target"""

path = Path("/etc/systemd/system/sinf_kvm_service.service")
path.write_text(text)
subprocess.run("sudo systemctl enable sinf_kvm_service --now", shell=True)
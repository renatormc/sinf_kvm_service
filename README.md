# KVM Service

Api para gerenciamento de máquinas virtuais em host com qemu-kvm

# Como instalar

## Clonar projeto e criar virtual env

```bash
git clone https://github.com/renatormc/sinf_kvm_service
sudo apt install virtualenv python3-pip python3.8-dev
virtualenv venv --python=python=3
```

## Criar arquivo .env e colocar o seguinte conteúdo


```bash
SINFKEY=chave_secreta
```

## Criar o arquivo que define o serviço

```bash
sudo nano /etc/systemd/system/sinf_kvm_service.service
```

Colocar os seguinte conteúdo:

```
[Unit]
Description=Sinf KVM Service
After=network.target

[Service]
User=sinf
Group=sinf
WorkingDirectory=/home/sinf/apps/sinf_kvm_service
ExecStart=/home/sinf/apps/sinf_kvm_service/venv/bin/gunicorn --workers 3 --bind 0.0.0.0:8002 app:app

[Install]
WantedBy=multi-user.target
```

Iniciar e habilitar o serviço

```bash
sudo systemctl start sinf_kvm_service
sudo systemctl enable sinf_kvm_service

```
# KVM Service

Api para gerenciamento de máquinas virtuais em host com qemu-kvm

# Como instalar

## Clonar projeto e criar virtual env

```bash
git clone https://github.com/renatormc/sinf_kvm_service
sudo apt install virtualenv python3-pip python3.8-dev
virtualenv venv --python=python=3
```

## Renomear o arquivo config-example.json para config.json


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
User=renato
Group=renato
WorkingDirectory=/home/renato/src/sinf_kvm_service
ExecStart=/home/renato/.pyenv/shims/pipenv run gunicorn --workers 3 --bind 0.0.0.0:8002 app:app

[Install]
WantedBy=multi-user.target
```

Para usar com interface gráfica apenas
```
Unit]
Description=Sinf KVM Service
After=graphical.target

[Service]
Type=simple
User=renato
Group=renato
Environment=DISPLAY=:1
WorkingDirectory=/home/renato/src/sinf_kvm_service
ExecStart=/home/renato/.pyenv/shims/pipenv run gunicorn --workers 3 --bind 0.0.0.0:8002 app:app

[Install]
WantedBy=graphical.target
```

Iniciar e habilitar o serviço

```bash
sudo systemctl enable sinf_kvm_service --now

```


# Autenticação

Para a autentição é necessário passar o token jwt no cabeçalho de nome Authorization precedido da palavra Bearer  

ex: 

```
Bearer eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkJydW5vIiwiaWF0IjoxNTE2MjM5MDIyfQ.YDN0wJHLzyzmqdwycv4wgh-RMBwQR4C_0uehWmo_77ZrAB46YnPYmzJJ2Lb36GyyDXDwRP9Bt759hcVmUiGWEg
```

# Endpoints

## Listar vms rodando no servidor

```
METHOD: GET
https://10.129.3.84:8002/list-running-vms
```

## Fazer snapshot dos dispositivos já conectados


```
METHOD: GET
https://10.129.3.84:8002/snapshot-devices
```

Será retornado um id que identificará o snapshot  


## Verificar quais novos dispositivos foram conectados após o snapshot

```
METHOD: GET
https://10.129.3.84:8002/new-devices/<id>
```
sendo:
id: o id que identifica o snapshot  

## Conectar usb

```
METHOD: GET
https://10.129.3.84:8002/attach-usb/<id>/<vm>
```

sendo,   
id: o identificador do dispositivo no formato vendor:product  
vm: O nome da máquina virtual na qual o dispositivo deverá ser conectado  


## Desconectar usb

```
METHOD: GET
https://10.129.3.84:8002/detach-usb/<id>/<vm>
```

sendo,  
id: o identificador do dispositivo no formato vendor:product  
vm: O nome da máquina virtual na qual o dispositivo deverá ser desconectado  

## Conectar disco

```
METHOD: GET
https://10.129.3.84:8002/attach-disk/<name>/<vm>
```

sendo,  
name: O nome do disco a ser conectado na vm (sdc, sdd, sdb, etc)  
vm: O nome da máquina virtual na qual o disco deverá ser conectado  

## Desconectar disco

```
METHOD: GET
https://10.129.3.84:8002/dettach-disk/<name>/<vm>
```

sendo,  
name: O nome do disco (sdc, sdd, sdb, etc)  
vm: O nome da máquina virtual da qual o disco deverá ser desconectado  

# .env 
```
TOKEN=token
PORT=8000
```

# Dependencies

```
sudo apt installxdotool
```
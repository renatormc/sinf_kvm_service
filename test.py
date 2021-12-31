from helpers import libvirt

a = [{
    "kname": "sda",
    "label": "",
    "model": "ATA CT240BX500SSD1",
    "name": "sda",
    "vendor": "ATA CT240BX500SSD1"
}]

b = {
    "label": "",
    "name": "sda",
    "vendor": "ATA CT240BX500SSD1",
    "kname": "sda",
    "model": "ATA CT240BX500SSD1",
}

print(b in a)
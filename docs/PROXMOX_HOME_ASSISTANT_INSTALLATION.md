# Home Assistant installation from scratch

## I. Proxmox

### 1. Download Proxmox image
* https://www.proxmox.com/en/downloads
* Check 3TB drive/softwares/proxmox_images

### 2. Create bootable USB
* USB might disconnect randomly. Try switching ports, unplug/replug USB during testing loop
* FQDN: pve.yoshi-assistant.local
	** Changable later (normal Linux hostname change)
* Static IP: 192.168.1.254

### 3. Wait until installation done then reboot
* Remove the boot USB before rebooting

### 4. Login via web browser from a different PC for testing
* https://192.168.1.254:8006

### Others
See this video: https://www.youtube.com/watch?v=kqZNFD0JNBc
* Disable subcription message
* Update repository
Or just
```bash
bash -c "$(curl -fsSL https://raw.githubusercontent.com/community-scripts/ProxmoxVE/main/tools/pve/post-pve-install.sh)"
```


## II. Home Assistant

### 1. Setup
https://forum.proxmox.com/threads/guide-install-home-assistant-os-in-a-vm.143251/
Or
```bash
bash -c "$(curl -fsSL https://raw.githubusercontent.com/community-scripts/ProxmoxVE/main/vm/haos-vm.sh)"
```
Then navigate to http://homeassistant.local:8123


### Initial config
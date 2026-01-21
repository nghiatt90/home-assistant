# Jellyfin Media Server on Proxmox LXC

A guide to setting up Jellyfin in a Proxmox LXC container with external USB storage.

## Architecture Overview

```
Proxmox Host
├── /mnt/media  (External HDD, mounted on host)
│
├── LXC: Jellyfin
│   └── /media → bind mount from /mnt/media
│
├── VM: Home Assistant (optional)
└── Samba (host) → PC file access
```

**Key principle**: Media disk stays on the HOST. Container accesses it via bind mount.

---

## Part 1: Mount External Drive on Proxmox Host

### 1.1 Identify the Drive

```bash
lsblk -o NAME,SIZE,FSTYPE,MOUNTPOINT,MODEL
blkid
```

Note the UUID (e.g., `UUID="<DRIVE-UUID>"`).

### 1.2 Install NTFS Support (if NTFS)

```bash
apt update && apt install -y ntfs-3g
```

### 1.3 Create Mount Point and Media Group

```bash
mkdir -p /mnt/media
groupadd media
```

### 1.4 Configure Persistent Mount

Edit `/etc/fstab`:

```bash
nano /etc/fstab
```

**For NTFS:**
```
UUID=<DRIVE-UUID>  /mnt/media  ntfs-3g  rw,noatime,uid=0,gid=media,umask=002,allow_other  0  0
```

**For ext4:**
```
UUID=<DRIVE-UUID>  /mnt/media  ext4  defaults,noatime  0  2
```

### 1.5 Validate Mount

```bash
mount -a
df -h | grep media
ls -lah /mnt/media
```

Reboot and verify mount persists.

---

## Part 2: Configure SMB Share (PC Access)

### 2.1 Install Samba

```bash
apt install -y samba
```

### 2.2 Create Samba User

```bash
useradd -M -s /usr/sbin/nologin <SMB-USERNAME>
smbpasswd -a <SMB-USERNAME>
smbpasswd -e <SMB-USERNAME>
usermod -aG media <SMB-USERNAME>
```

### 2.3 Configure Share

Edit `/etc/samba/smb.conf`, add at bottom:

```ini
[Media]
   path = /mnt/media
   browseable = yes
   read only = no
   valid users = <SMB-USERNAME>
   force user = root
   force group = root
   create mask = 0664
   directory mask = 0775
```

### 2.4 Restart Samba

```bash
systemctl restart smbd nmbd
```

### 2.5 Access from Client

**Linux (Nautilus):** `smb://<PROXMOX-IP>/Media`

**Linux (CLI):**
```bash
sudo apt install -y cifs-utils
sudo mkdir -p /mnt/media-server
sudo mount -t cifs //<PROXMOX-IP>/Media /mnt/media-server \
  -o username=<SMB-USERNAME>,vers=3.1.1,uid=$(id -u),gid=$(id -g)
```

---

## Part 3: Create Jellyfin LXC Container

### 3.1 Create Container via Proxmox UI

| Setting | Value |
|---------|-------|
| Template | `debian-12-standard` |
| Unprivileged | Yes |
| Cores | 2 |
| Memory | 4096 MB |
| Swap | 512-1024 MB |
| Disk | 8-16 GiB on `local-lvm` |
| Network | vmbr0, DHCP, IPv6: None |

**Do NOT start the container yet.**

### 3.2 Add Bind Mount

On the Proxmox host, edit the container config (replace `<CT-ID>` with your container ID):

```bash
nano /etc/pve/lxc/<CT-ID>.conf
```

Add at the bottom:

```ini
mp0: /mnt/media,mp=/media,backup=0
```

Verify:

```bash
grep mp0 /etc/pve/lxc/<CT-ID>.conf
```

### 3.3 Start Container

```bash
pct start <CT-ID>
pct enter <CT-ID>
```

### 3.4 Verify Media Access Inside Container

```bash
ls -ld /media
ls /media
```

---

## Part 4: Install Jellyfin in Container

All commands below run **inside the container**.

### 4.1 Update System

```bash
apt update && apt upgrade -y
```

### 4.2 Install Prerequisites

```bash
apt install -y curl gnupg apt-transport-https
```

### 4.3 Install Jellyfin

```bash
curl -fsSL https://repo.jellyfin.org/install-debuntu.sh | bash
```

### 4.4 Verify Service

```bash
systemctl status jellyfin
```

### 4.5 Verify Jellyfin Can Access Media

```bash
id jellyfin
sudo -u jellyfin ls /media
```

If permission denied, create matching group inside container:

```bash
groupadd -g 1000 media
usermod -aG media jellyfin
systemctl restart jellyfin
```

---

## Part 5: Configure Jellyfin

### 5.1 Access Web UI

Open browser: `http://<CT-IP>:8096`

### 5.2 Initial Setup

1. Select language
2. Create admin user
3. Add libraries:

| Type | Path |
|------|------|
| Movies | `/media/Movies` |
| TV Shows | `/media/TV` |

**Important:** Use `/media/...` paths (container), NOT `/mnt/media/...` (host).

### 5.3 Verify Logs

```bash
journalctl -u jellyfin --no-pager -n 50
```

Should not contain "Permission denied" errors.

---

## Part 6: Client Access

### LG TV (webOS)
- Install Jellyfin from LG Content Store
- Server: `http://<CT-IP>:8096`

### Android/iOS
- Install Jellyfin app
- Same server address

### Browser
- Direct access: `http://<CT-IP>:8096`

---

## Recommended Folder Structure

```
/mnt/media
├── Movies
│   ├── Movie Name (2023)
│   │   └── Movie Name (2023).mkv
│   └── Another Movie (2019).mp4
└── TV
    └── Show Name (2020)
        ├── Season 01
        │   └── Show Name - S01E01.mkv
        └── Season 02
```

---

## Troubleshooting

### Container can't access /media
```bash
# On host: check mount
mount | grep media

# Inside container: check group
id jellyfin
# Should include 'media' group
```

### SMB share empty on client
```bash
# Client: check if mounted
mount | grep cifs

# Remount if needed
sudo mount -t cifs //<PROXMOX-IP>/Media /mnt/media-server \
  -o username=<SMB-USERNAME>,vers=3.1.1,uid=$(id -u),gid=$(id -g)
```

### USB drive disconnects
```bash
# On host: disable power management
echo on > /sys/block/sda/device/power/control
```

---

## Quick Reference

| Component | Location |
|-----------|----------|
| Host media mount | `/mnt/media` |
| Container media path | `/media` |
| Jellyfin config | `/var/lib/jellyfin` (inside container) |
| Jellyfin web UI | `http://<CT-IP>:8096` |
| SMB share | `smb://<PROXMOX-IP>/Media` |
| Container config | `/etc/pve/lxc/<CT-ID>.conf` |

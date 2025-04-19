# Raspberry Pi Setup with Ubuntu Server

This guide covers installing **Ubuntu Server** on a Raspberry Pi using the official imager.

## Prerequisites
- Raspberry Pi (4/5 recommended)
- MicroSD card (16GB+)
- Power supply (USB-C for Pi 4/5)
- Ethernet cable (or Wi-Fi)
- Computer for flashing

---

## 1. Prepare Installation Media
1. Download [Raspberry Pi Imager](https://www.raspberrypi.com/software/)
2. Install on your computer

---

## 2. Create Bootable SD Card
### Using Raspberry Pi Imager:
1. Insert microSD card
2. Open Raspberry Pi Imager
3. Click "Choose OS" → "Other general-purpose OS" → "Ubuntu Server"
4. Select your SD card under "Storage"
5. Configure:
   - Set hostname (e.g., `my-pi-server`)
   - Enable SSH (password or public key)
   - Set username/password
   - Configure Wi-Fi if needed
6. Click "Write" and wait for completion

---

## 3. First Boot
1. Insert SD card into Pi
2. Connect:
   - Ethernet cable (recommended for first boot)
   - Monitor/keyboard (optional)
   - Power last
3. Wait 5-10 minutes for initial setup

---

## 4. Connect via SSH
### Find your Pi's IP:
```bash
arp -a | grep -i "dc:a6:32\|b8:27:eb"  # Common Pi MAC prefixes
```

### Connect
```bash
ssh username@ip-address
# Default if using Ubuntu Server image directly:
# User: ubuntu
# Password: ubuntu (change on first login)
```
Or
```bash
ssh username@hostname.local
```

### Basic Setup
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install common tools
sudo apt install -y \
  git curl tmux htop \
  ufw net-tools

# Setup firewall
sudo ufw allow ssh
sudo ufw enable
```

---

## Useful Links
- [Ubuntu Server for Raspberry Pi](https://ubuntu.com/download/raspberry-pi)
- [Raspberry Pi Imager](https://www.raspberrypi.com/software/)
- [Ubuntu Server Documentation](https://ubuntu.com/server/docs)
- [Raspberry Pi Networking Guide](https://www.raspberrypi.com/documentation/computers/configuration.html#networking)
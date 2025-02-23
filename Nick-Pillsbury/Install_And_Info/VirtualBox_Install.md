# Setting Up VirtualBox and Ubuntu VM

This guide walks through installing VirtualBox and setting up an Ubuntu Virtual Machine (VM).

---

## Prerequisites

Ensure your system meets the following requirements:

- **Operating System**: Windows, macOS, or Linux
- **RAM**: 4+ GB (8+ GB recommended for better performance)
- **Disk Space**: 20+ GB available
- **Processor**: Supports virtualization (VT-x/AMD-V enabled in BIOS)

---

## Step 1: Install VirtualBox

### Download VirtualBox

1. Visit the [VirtualBox Downloads](https://www.virtualbox.org/wiki/Downloads) page.
2. Download the installer for your OS (Windows, macOS, or Linux).
### Install VirtualBox
- **Windows**: Run the `.exe` file and follow the installation wizard.

---

## Step 2: Download Ubuntu ISO

1. Go to the [Ubuntu Downloads](https://ubuntu.com/download/desktop) page.
2. Download the latest **Ubuntu Desktop** ISO file.

---

## Step 3: Create a New Virtual Machine
1. Open **VirtualBox** and click **New**.
2. Set the name (e.g., `Ubuntu VM`), type as **Linux**, and version as **Ubuntu (64-bit)**.
3. Allocate memory (RAM): **2+ GB (4+ GB recommended)**.
4. Choose **Create a virtual hard disk now** → **VDI (VirtualBox Disk Image)** → **Dynamically allocated**.
5. Set disk size: **20+ GB**.

---

## Step 4: Install Ubuntu on Virtual Machine

1. Select the created VM and click **Settings**.
2. Under **Storage**, click **Empty**, then **Choose a disk file**, and select the Ubuntu ISO.
3. Under **System**, ensure **Enable EFI** is checked (if required).
4. Click **Start** to boot the VM and install Ubuntu.
5. Follow the Ubuntu installation wizard:
   - Select language, keyboard layout, and installation type.
   - Create a username and password.
   - Choose **Erase disk and install Ubuntu** (if no custom partitions are needed).
   - Click **Install Now** and wait for installation to complete.
6. After installation, restart the VM and remove the installation ISO.

---

## Step 5: Install VirtualBox Guest Additions (Optional but Recommended)

1. Start the Ubuntu VM.
2. In the VirtualBox menu, click **Devices** → **Insert Guest Additions CD Image**.
3. Open a terminal and run:
   ```bash
   sudo apt update && sudo apt install -y build-essential dkms linux-headers-$(uname -r)
   sudo mount /dev/cdrom /mnt
   sudo /mnt/VBoxLinuxAdditions.run
   ```
4. Restart the VM to apply changes.

---

## Special Notes

- Ensure **virtualization (VT-x/AMD-V) is enabled** in your BIOS for best performance.
- Adjust VM settings like CPU and RAM allocation in **Settings > System** for better performance.
- Take **VM snapshots** before making major changes to easily restore the system.

---

## Links

[VirtualBox Official Site](https://www.virtualbox.org/) [Ubuntu Official Downloads](https://ubuntu.com/download/desktop) [VirtualBox Guest Additions Guide](https://www.virtualbox.org/manual/ch04.html)


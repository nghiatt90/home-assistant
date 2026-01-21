# ESP32 Bluetooth Proxy setup

1. Plugin the device and confirm the port number `/dev/ttyACM0` or `/dev/ttyACM1`
2. Edit `secrets.yaml` with correct wifi credentials
3. Run ESPHome `uv run esphome run esp32.yaml --device /dev/ttyACM1
4. Wait till the device restarts and connect to Wifi
5. On Home Assistant, the new device should show up automatically. Add with ESPHome
6. Check under Bluetooth to see the device shows up as Bluetooth device.

# Bluetooth dongle passthrough problem

Source: https://forum.proxmox.com/threads/pve-7-4-home-assistant-intel-ax200-bluetooth-issues.126014/
>  you can blacklist btusb to stop Proxmox initializing the device before Home Assistant OS. Add a the line `blacklist btusb` to `/etc/modprobe.d/pve-blacklist.conf`. Finally, reboot and bluetooth should work perfectly from now on.

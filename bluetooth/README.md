# ESP32 Bluetooth Proxy setup

1. Plugin the device and confirm the port number `/dev/ttyACM0` or `/dev/ttyACM1`
2. Edit `secrets.yaml` with correct wifi credentials
3. Run ESPHome `uv run esphome run esp32.yaml --device /dev/ttyACM1
4. Wait till the device restarts and connect to Wifi
5. On Home Assistant, the new device should show up automatically. Add with ESPHome
6. Check under Bluetooth to see the device shows up as Bluetooth device.

# Smart Home System Summary

## Network infrastructure

Home network is centered around **Google Nest Wifi**, spanning **three floors** with a mix of wired and wireless backhaul. The ISP router provides upstream connectivity only, while all local routing and IP management are handled by Nest Wifi.

## Diagram

                    ┌──────────────────────────┐
                    │  ISP Router NURO SGP200W │
                    │        (upstream)        │
                    │       192.168.1.1        │
                    │  2F – center location    │
                    └─────────────┬────────────┘
                                  │
                    ┌─────────────▼────────────┐
                    │  Google Nest Wifi Router │
                    │       (Main / NAT)       │
                    │       192.168.86.1       │
                    │  2F – living / center    │
                    └─────────────┬────────────┘
                                  │
          ┌───────────────────────┼────────────────────────┐
          │                                                │
┌─────────▼─────────┐                            ┌─────────▼─────────┐
│  Nest Wifi Point  │                            │   Ethernet Run    │
│  3F – coverage    │                            │   (wall socket)   │
│  (wireless mesh)  │                            │   to 1F corner    │
└───────────────────┘                            └─────────┬─────────┘
                                                           │
                                   ┌───────────────────────┼────────────────────────┐
						           │                                                |
						 ┌─────────▼─────────┐                       ┌──────────────▼──────────────┐
						 │  Nest Wifi Point  │                       │     Physical Ethernet Hub   │
						 │  1F – coverage    │                       │      (unmanaged switch)     │
						 │  (wireless mesh)  │                       │     1F – corner location    │
						 └───────────────────┘                       └──────────────┬──────────────┘
						                                                            │
						                                             ┌──────────────▼──────────────┐
						                                             │      Intel NUC (Proxmox)    │
						                                             │        192.168.86.253       │
						                                             │         1F – near hub       │
						                                             └──────────────┬──────────────┘
						                                                            │
						                                             ┌──────────────▼──────────────┐
						                                             │   Home Assistant VM (HAOS)  │
						                                             │       192.168.86.252        │
						                                             │    (on Proxmox, bridged)    │
						                                             └─────────────────────────────┘



---

# Devices

## Connected devices (confirmed)

### Core / Infrastructure

- ISP router (NURO SGP200W, upstream only)
- Google Nest Wifi
  - 1× main router (2F)
  - 2× mesh points (1F, 3F)
- Physical Ethernet hub (1F)
- Intel NUC running **Proxmox**
- Home Assistant (VM on Proxmox)

### Smart home / HA-integrated

- **Daikin air conditioners**
  - 1× Urusara with Wi-Fi
  - 4× legacy units controlled via SwitchBot IR
- **SwitchBot ecosystem**
  - 5× SwitchBot Ceiling Light Pro (BLE + IR)
  - SwitchBot smart lock
  - SwitchBot door sensor / keypad
  - SwitchBot Cloud integration enabled
- **Cameras**
  - 1x Reolink RLC-811A camera (PoE): entrance
- **Media**
  - LG Smart TV (webOS)
  - 2× Google Nest Mini speakers

### Planned devices

- **Zigbee ecosystem**
  - Coordinator: SMLIGHT SLZB-06M (PoE / Ethernet, centrally placed on 2F)
  - Climate sensors: SONOFF SNZB-02D (LCD)
  - Motion / presence sensors: SONOFF SNZB-06P
  - Zigbee repeaters: IKEA INSPELNING smart plugs
- **SwitchBot Hub Mini**
  - For improved BLE and IR responsiveness, especially on upper floors
- **Indoor Wi-Fi cameras**
  - Reolink E1 Zoom ×2


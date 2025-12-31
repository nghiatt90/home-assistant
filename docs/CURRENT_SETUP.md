# Smart Home System Summary

## Network infrastructure

Home network is centered around **Google Nest Wifi**, spanning **three floors** with a mix of wired and wireless backhaul. The ISP router provides upstream connectivity only, while all local routing and IP management are handled by Nest Wifi.

## Diagram

```mermaid
flowchart TB
    %% ISP & Core Network
    ISP[ISP Router<br/>NURO SGP200W<br/>192.168.1.1<br/>(Upstream only)]
    NestRouter[Google Nest Wifi Router<br/>Main / NAT<br/>192.168.86.1<br/>2F – Living center]

    ISP --> NestRouter

    %% Mesh & Wired Distribution
    Nest3F[Nest Wifi Point<br/>3F – Wireless Mesh]
    Nest1F[Nest Wifi Point<br/>1F – Wireless Mesh]

    NestRouter --> Nest3F
    NestRouter -->|Ethernet (wall run)| Switch1F

    Switch1F[Unmanaged Ethernet Switch<br/>1F – Corner]

    Switch1F --> Nest1F
    Switch1F --> NUC

    %% Compute
    NUC[Intel NUC<br/>Proxmox Host<br/>192.168.86.253]

    NUC --> HA[Home Assistant OS VM<br/>192.168.86.252<br/>(Bridged Network)]

    %% Smart Home Devices
    HA --> Daikin[Daikin ACs<br/>Urusara (Wi-Fi)]
    HA --> SwitchBot[SwitchBot Cloud<br/>Lights / Lock / IR]
    HA --> ReolinkPoE[Reolink RLC-811A<br/>PoE Camera]
    HA --> LGTV[LG webOS TV]
    HA --> NestAudio[Google Nest Mini ×2]

    %% Planned Zigbee
    Zigbee[Zigbee Coordinator<br/>SMLIGHT SLZB-06M<br/>PoE / Ethernet<br/>2F Central]
    HA --> Zigbee

    Zigbee --> ZigbeeSensors[SONOFF Sensors<br/>Temp / Motion]
    Zigbee --> ZigbeePlugs[IKEA INSPELNING<br/>Repeaters]

    %% Planned Cameras
    HA --> ReolinkIndoor[Reolink E1 Zoom ×2<br/>Wi-Fi Indoor]
```



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


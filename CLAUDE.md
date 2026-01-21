# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This is a **Home Assistant** configuration directory containing YAML configurations and custom Python integrations. Home Assistant is a home automation platform that manages smart home devices, automations, and integrations.

## Project Structure

```
/config/
├── configuration.yaml          # Main HA config - loads other YAML files
├── automations.yaml            # Automation rules
├── scripts.yaml                # Script definitions
├── scenes.yaml                 # Scene definitions
├── binary_sensors.yaml         # Template binary sensors
├── secrets.yaml                # Sensitive values (tokens, passwords)
├── custom_components/          # Python integrations
│   ├── googlefindmy/           # Google Find My Device tracker (~9k lines)
│   ├── hacs/                   # Home Assistant Community Store
│   ├── xiaomi_cloud_map_extractor/
│   └── roborock_custom_map/
├── blueprints/                 # Reusable automation/script templates
├── .storage/                   # HA internal state (entity/device registry)
└── home-assistant_v2.db        # SQLite database (history/stats)
```

## Commands

**Configuration Validation:**
```bash
hass -c /config --check-config
```

**Start Home Assistant:**
```bash
hass -c /config
```

**Reload Configuration (via HA CLI):**
```bash
ha core restart
ha core check
```

## Custom Component Architecture

### GoogleFindMy Integration (`custom_components/googlefindmy/`)

This is the primary custom component. It follows Home Assistant's standard integration pattern:

**Entry Point:** `__init__.py` - `async_setup_entry()` initializes the integration

**Core Pattern - DataUpdateCoordinator:**
- `coordinator.py` - Central polling hub that fetches data from Google's API
- Entities subscribe to coordinator updates via `CoordinatorEntity` base class
- Polling interval configurable (default 5 minutes)

**Platform Entities:**
- `device_tracker.py` - GPS location tracking
- `sensor.py` - Last seen timestamps, diagnostic stats
- `button.py` - Locate device, play/stop sound actions
- `config_flow.py` - Setup UI wizard

**API Modules:**
- `NovaApi/` - Google Nova API wrapper (device list, actions)
- `SpotApi/` - Google Spot API (BLE devices)
- `ProtoDecoders/` - Protobuf response parsing
- `FMDNCrypto/` - Encryption/EID generation
- `Auth/` - OAuth tokens, FCM push notifications

**Services Exposed:**
- `googlefindmy.locate_device`
- `googlefindmy.play_sound`
- `googlefindmy.stop_sound`
- `googlefindmy.refresh_device_urls`
- `googlefindmy.rebuild_registry`

### HACS Integration (`custom_components/hacs/`)

Home Assistant Community Store - manages third-party integrations.

**Key Patterns:**
- `validate/` - Repository validation rules (one file per rule, uses `ActionValidationBase`)
- `repositories/` - Repository type handlers (integration, theme, plugin, etc.)
- `websocket/` - WebSocket API handlers

**Validation Rules:** When adding validation rules to `hacs/validate/`:
- One file per rule
- Use `ActionValidationBase` as base class
- Implement `validate` or `async_validate` methods
- Raise `ValidationException` on failure

## Home Assistant Patterns

**YAML Includes:** Main config uses `!include` and `!include_dir_merge_named` directives to split configuration across files.

**Entity Platforms:** Custom components register platforms (sensor, button, device_tracker) that create entities managed by a coordinator.

**Config Flow:** UI-based setup defined in `config_flow.py` - handles authentication and options.

**Storage:** Integration state persists in `.storage/` as JSON files keyed by domain.

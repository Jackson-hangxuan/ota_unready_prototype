# OTA Firmware Setup Summary

> **⚠️ IMPORTANT: The firmware server hosts version 1.7.6 firmware (.bin file). Devices should have version 1.7.5 installed to trigger the OTA update check.**

> **🔧 CONFIGURATION REQUIRED: Replace all instances of `192.168.1.8` in the configuration files with your actual desktop's IPv4 address. Find your IPv4 with `ipconfig` (Windows) or `ifconfig` (Linux/Mac).**

---

## Quick Start: Configure Your IP Address

**Find your desktop's IPv4 address:**
```powershell
# Windows PowerShell
ipconfig
# Look for "IPv4 Address" under your active network adapter
```

**Update these files with your IPv4 address:**
1. `xiaozhi-server/core/api/ota_handler.py` - Line 53
2. `xiaozhi-server/config.yaml` or `.config.yaml` - WebSocket and vision_explain URLs
3. `test_firmware_ota.py` - Test script URLs (optional, for testing only)

**Replace:** `192.168.1.8` → `YOUR_IPv4_ADDRESS`

---

## What Was Changed

### 1. Created Firmware Server (`firmware_server.py`)
- **Purpose**: Hosts `xiaozhi.bin` firmware file over HTTP
- **Port**: `8003`
- **URL**: `http://192.168.1.8:8003/xiaozhi.bin`
- **Location**: Run on **Windows** (not WSL) to be accessible on network

### 2. Modified OTA Handler
- **File**: `xiaozhi-server/core/api/ota_handler.py`
- **Changes**:
  - Returns firmware URL: `http://192.168.1.8:8003/xiaozhi.bin`
  - Returns firmware version: `1.7.6` (hardcoded)

### 3. Created Test Script (`test_firmware_ota.py`)
- Tests firmware server availability
- Tests OTA endpoint response
- Tests firmware download

---

## Port Configuration

| Service | Port | Protocol | Location |
|---------|------|----------|----------|
| WebSocket | 8000 | WS | WSL (xiaozhi-server) |
| OTA API | 8002 | HTTP | WSL (xiaozhi-server) |
| Firmware Download | 8003 | HTTP | **Windows** (firmware_server.py) |

---

## How to Run

### 1. Start Firmware Server (Windows PowerShell)
```powershell
cd D:\xinnan_server\xiaozhi-esp32-server\main
python firmware_server.py
```

**Expected output:**
```
=== 小智固件服务器 ===
固件文件: D:\xinnan_server\xiaozhi-esp32-server\main\xiaozhi.bin
文件大小: 4023744 bytes
监听地址: 0.0.0.0:8003
下载地址: http://192.168.1.8:8003/xiaozhi.bin
```

### 2. Start Xiaozhi Server (WSL)
```bash
cd xiaozhi-server
python app.py
```

---

## OTA Response Format

```json
{
  "server_time": {
    "timestamp": 1761063913552,
    "timezone_offset": 480
  },
  "firmware": {
    "version": "1.7.6",
    "url": "http://192.168.1.8:8003/xiaozhi.bin"
  },
  "websocket": {
    "url": "ws://192.168.1.8:8000/xiaozhi/v1/"
  }
}
```

---

## Testing

### Test OTA Endpoint (Postman)
- **Method**: `POST`
- **URL**: `http://192.168.1.8:8002/xiaozhi/ota/`
- **Headers**:
  - `Content-Type: application/json`
  - `device-id: test-device-123`
- **Body**:
  ```json
  {
    "application": {
      "version": "1.7.5"
    }
  }
  ```

### Test Firmware Download
```bash
curl -I http://192.168.1.8:8003/xiaozhi.bin
```

### Run Automated Tests
```bash
python test_firmware_ota.py
```

---

## Key Files

```
main/
├── xiaozhi.bin                    # Firmware file (version 1.7.6)
├── firmware_server.py             # Firmware HTTP server
├── test_firmware_ota.py           # Test script
└── xiaozhi-server/
    └── core/api/ota_handler.py    # Modified to return v1.7.6 and URL
```

---

## Important Notes

1. **Run firmware_server.py on Windows** (not WSL) for network accessibility
2. **Device version should be 1.7.5** to receive the 1.7.6 update
3. **Keep both servers running** during OTA operations
4. Firmware version is **hardcoded** in `ota_handler.py` line 56

---

## Troubleshooting

**Problem**: Cannot access `http://192.168.1.8:8003/xiaozhi.bin`
- **Solution**: Ensure firmware_server.py is running on **Windows**, not WSL

**Problem**: OTA returns empty firmware URL
- **Solution**: Restart xiaozhi-server after modifying ota_handler.py

**Problem**: Device doesn't update
- **Solution**: Ensure device firmware version is 1.7.5 (not 1.7.6)


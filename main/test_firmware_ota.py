#!/usr/bin/env python3
"""
测试固件 OTA 功能
Test firmware OTA functionality
"""

import requests
import time

def test_firmware_server():
    """测试固件服务器"""
    print("=" * 50)
    print("1. 测试固件服务器 (端口 8003)")
    print("=" * 50)
    
    try:
        response = requests.get("http://192.168.1.8:8003/xiaozhi.bin", timeout=5)
        if response.status_code == 200:
            print(f"✓ 固件服务器运行正常")
            print(f"  固件大小: {len(response.content)} bytes")
            return True
        else:
            print(f"✗ 固件服务器响应异常: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print(f"✗ 无法连接到固件服务器")
        print(f"  请先运行: python firmware_server.py")
        return False
    except Exception as e:
        print(f"✗ 错误: {e}")
        return False

def test_ota_endpoint():
    """测试 OTA 端点"""
    print("\n" + "=" * 50)
    print("2. 测试 OTA 端点 (端口 8002)")
    print("=" * 50)
    
    headers = {
        "Content-Type": "application/json",
        "device-id": "test-device-12345"
    }
    
    payload = {
        "application": {
            "version": "1.0.0"
        }
    }
    
    try:
        response = requests.post(
            "http://192.168.1.8:8002/xiaozhi/ota/",
            headers=headers,
            json=payload,
            timeout=5
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✓ OTA 端点运行正常")
            print(f"\n响应数据:")
            print(f"  服务器时间: {data['server_time']['timestamp']}")
            print(f"  固件版本: {data['firmware']['version']}")
            print(f"  固件URL: {data['firmware']['url']}")
            print(f"  WebSocket: {data['websocket']['url']}")
            
            # 验证固件 URL
            firmware_url = data['firmware']['url']
            if firmware_url and "8003" in firmware_url:
                print(f"\n✓ 固件URL配置正确!")
                return firmware_url
            else:
                print(f"\n✗ 固件URL不正确: {firmware_url}")
                print(f"  期望: http://192.168.1.8:8003/xiaozhi.bin")
                return None
        else:
            print(f"✗ OTA 端点响应异常: {response.status_code}")
            print(f"  响应: {response.text}")
            return None
            
    except requests.exceptions.ConnectionError:
        print(f"✗ 无法连接到 OTA 服务器")
        print(f"  请先运行: cd xiaozhi-server && python app.py")
        return None
    except Exception as e:
        print(f"✗ 错误: {e}")
        return None

def test_firmware_download(firmware_url):
    """测试固件下载"""
    print("\n" + "=" * 50)
    print("3. 测试固件下载")
    print("=" * 50)
    
    try:
        print(f"下载URL: {firmware_url}")
        response = requests.get(firmware_url, timeout=10)
        
        if response.status_code == 200:
            print(f"✓ 固件下载成功!")
            print(f"  大小: {len(response.content)} bytes")
            print(f"  类型: {response.headers.get('Content-Type')}")
            return True
        else:
            print(f"✗ 固件下载失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ 下载错误: {e}")
        return False

def main():
    """主测试流程"""
    print("\n" + "=" * 50)
    print("小智 OTA 固件测试工具")
    print("=" * 50 + "\n")
    
    # 测试1: 固件服务器
    firmware_ok = test_firmware_server()
    time.sleep(1)
    
    # 测试2: OTA 端点
    firmware_url = test_ota_endpoint()
    time.sleep(1)
    
    # 测试3: 固件下载
    if firmware_url:
        download_ok = test_firmware_download(firmware_url)
    else:
        download_ok = False
    
    # 总结
    print("\n" + "=" * 50)
    print("测试总结")
    print("=" * 50)
    print(f"固件服务器: {'✓ 正常' if firmware_ok else '✗ 异常'}")
    print(f"OTA端点:    {'✓ 正常' if firmware_url else '✗ 异常'}")
    print(f"固件下载:   {'✓ 正常' if download_ok else '✗ 异常'}")
    
    if firmware_ok and firmware_url and download_ok:
        print("\n🎉 所有测试通过! OTA 系统工作正常!")
    else:
        print("\n⚠ 部分测试失败，请检查上述错误信息")
        print("\n启动步骤:")
        print("  1. python firmware_server.py")
        print("  2. cd xiaozhi-server && python app.py")
        print("  3. python test_firmware_ota.py")
    
    print()

if __name__ == "__main__":
    main()


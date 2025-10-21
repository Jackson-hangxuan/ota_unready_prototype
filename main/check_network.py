#!/usr/bin/env python3
"""
网络诊断脚本 - 检查服务器监听状态和网络配置
Network diagnostic script
"""

import socket
import subprocess
import sys

def get_all_ips():
    """获取所有网络接口的IP地址"""
    print("=" * 60)
    print("本机所有IP地址 (All Local IP Addresses)")
    print("=" * 60)
    
    hostname = socket.gethostname()
    print(f"主机名: {hostname}")
    
    try:
        # 获取所有IP地址
        addrs = socket.getaddrinfo(hostname, None)
        ips = set()
        for addr in addrs:
            ip = addr[4][0]
            if ':' not in ip:  # 只显示IPv4
                ips.add(ip)
        
        for ip in sorted(ips):
            print(f"  - {ip}")
    except Exception as e:
        print(f"错误: {e}")

def check_port_listening(port=8003):
    """检查端口是否在监听"""
    print(f"\n" + "=" * 60)
    print(f"检查端口 {port} 是否在监听")
    print("=" * 60)
    
    # 测试本地监听
    test_addresses = [
        ("127.0.0.1", "localhost"),
        ("0.0.0.0", "all interfaces"),
    ]
    
    for addr, desc in test_addresses:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            result = sock.connect_ex((addr, port))
            sock.close()
            
            if result == 0:
                print(f"✓ {desc} ({addr}:{port}) - 可访问")
            else:
                print(f"✗ {desc} ({addr}:{port}) - 无法连接")
        except Exception as e:
            print(f"✗ {desc} ({addr}:{port}) - 错误: {e}")

def check_wsl_network():
    """检查是否在WSL环境中"""
    print(f"\n" + "=" * 60)
    print("检查WSL环境")
    print("=" * 60)
    
    try:
        with open('/proc/version', 'r') as f:
            version = f.read().lower()
            if 'microsoft' in version or 'wsl' in version:
                print("✓ 检测到WSL环境")
                print("\nWSL网络说明:")
                print("  - WSL有独立的网络命名空间")
                print("  - WSL内部IP通常是 172.x.x.x 网段")
                print("  - Windows主机IP是不同的（如 192.168.1.8）")
                print("\n解决方案:")
                print("  1. 在WSL内测试: curl http://localhost:8003/xiaozhi.bin")
                print("  2. 使用WSL IP: 需要从Windows访问WSL的IP")
                print("  3. 端口转发: 使用netsh设置端口转发")
                return True
            else:
                print("✗ 不是WSL环境")
                return False
    except:
        print("✗ 无法确定是否为WSL环境")
        return False

def get_wsl_ip():
    """获取WSL的IP地址"""
    print(f"\n" + "=" * 60)
    print("WSL IP地址")
    print("=" * 60)
    
    try:
        # 获取eth0接口的IP
        result = subprocess.run(['ip', 'addr', 'show', 'eth0'], 
                              capture_output=True, text=True)
        output = result.stdout
        
        # 解析IP地址
        for line in output.split('\n'):
            if 'inet ' in line:
                ip = line.strip().split()[1].split('/')[0]
                print(f"WSL IP: {ip}")
                print(f"\n在Windows PowerShell中运行:")
                print(f"  curl http://{ip}:8003/xiaozhi.bin -Method HEAD")
                return ip
    except Exception as e:
        print(f"无法获取WSL IP: {e}")
    
    return None

def test_local_server():
    """测试本地服务器"""
    print(f"\n" + "=" * 60)
    print("测试本地服务器连接")
    print("=" * 60)
    
    test_urls = [
        "http://localhost:8003/xiaozhi.bin",
        "http://127.0.0.1:8003/xiaozhi.bin",
    ]
    
    try:
        import requests
        for url in test_urls:
            try:
                resp = requests.head(url, timeout=2)
                if resp.status_code == 200:
                    print(f"✓ {url} - 可访问")
                    print(f"  文件大小: {resp.headers.get('Content-Length', 'unknown')} bytes")
                else:
                    print(f"✗ {url} - 状态码: {resp.status_code}")
            except Exception as e:
                print(f"✗ {url} - 错误: {e}")
    except ImportError:
        print("⚠ 未安装requests库，跳过HTTP测试")

def main():
    print("\n" + "=" * 60)
    print("小智固件服务器网络诊断工具")
    print("=" * 60 + "\n")
    
    get_all_ips()
    check_port_listening(8003)
    is_wsl = check_wsl_network()
    
    if is_wsl:
        wsl_ip = get_wsl_ip()
    
    test_local_server()
    
    print("\n" + "=" * 60)
    print("建议 (Recommendations)")
    print("=" * 60)
    
    if is_wsl:
        print("\n您在WSL中运行服务器，有以下选择:")
        print("\n方案1: 在Windows中运行固件服务器（推荐）")
        print("  - 退出WSL")
        print("  - 在Windows PowerShell中运行: python firmware_server.py")
        print("  - 这样可以直接使用 192.168.1.8:8003")
        
        print("\n方案2: 使用WSL IP地址")
        if wsl_ip:
            print(f"  - 修改 ota_handler.py 使用: {wsl_ip}:8003")
        print("  - 注意: WSL IP可能会变化")
        
        print("\n方案3: 设置端口转发（高级）")
        print("  - 在Windows PowerShell (管理员) 中运行:")
        if wsl_ip:
            print(f"    netsh interface portproxy add v4tov4 listenport=8003 listenaddress=0.0.0.0 connectport=8003 connectaddress={wsl_ip}")
    else:
        print("\n如果服务器运行正常但无法访问:")
        print("  1. 检查防火墙设置")
        print("  2. 确认IP地址是否正确")
        print("  3. 尝试使用 localhost:8003 测试")

if __name__ == "__main__":
    main()


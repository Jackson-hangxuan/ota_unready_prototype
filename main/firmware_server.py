#!/usr/bin/env python3
"""
简单的固件文件服务器
Simple firmware file server for xiaozhi.bin
"""

import os
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path

class FirmwareHandler(SimpleHTTPRequestHandler):
    """固件文件处理器"""
    
    def do_GET(self):
        """处理GET请求"""
        # 只允许访问 xiaozhi.bin
        if self.path == '/xiaozhi.bin' or self.path == '/':
            firmware_path = Path(__file__).parent / 'xiaozhi.bin'
            
            if not firmware_path.exists():
                self.send_error(404, "固件文件不存在 (xiaozhi.bin not found)")
                return
            
            # 发送文件
            self.send_response(200)
            self.send_header('Content-Type', 'application/octet-stream')
            self.send_header('Content-Disposition', 'attachment; filename="xiaozhi.bin"')
            self.send_header('Content-Length', str(firmware_path.stat().st_size))
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            with open(firmware_path, 'rb') as f:
                self.wfile.write(f.read())
            
            print(f"✓ 已发送固件文件: xiaozhi.bin ({firmware_path.stat().st_size} bytes)")
        else:
            self.send_error(404, "只允许访问 xiaozhi.bin (Only xiaozhi.bin is available)")
    
    def log_message(self, format, *args):
        """自定义日志格式"""
        print(f"[固件服务器] {self.address_string()} - {format % args}")

def main():
    """启动固件服务器"""
    host = '0.0.0.0'  # 监听所有网卡
    port = 8003
    
    # 检查固件文件是否存在
    firmware_path = Path(__file__).parent / 'xiaozhi.bin'
    if not firmware_path.exists():
        print(f"❌ 错误: 固件文件不存在")
        print(f"   路径: {firmware_path}")
        print(f"   请确保 xiaozhi.bin 文件在当前目录下")
        return
    
    print(f"=== 小智固件服务器 ===")
    print(f"固件文件: {firmware_path}")
    print(f"文件大小: {firmware_path.stat().st_size} bytes")
    print(f"监听地址: {host}:{port}")
    print(f"下载地址: http://192.168.1.8:{port}/xiaozhi.bin")
    print(f"\n服务器启动中...\n")
    
    server = HTTPServer((host, port), FirmwareHandler)
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n\n服务器已停止")
        server.shutdown()

if __name__ == '__main__':
    main()


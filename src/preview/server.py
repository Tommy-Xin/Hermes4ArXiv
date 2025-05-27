#!/usr/bin/env python3
"""
HTML模板预览服务器
在本地启动HTTP服务器来预览邮件模板
"""

import http.server
import socketserver
import webbrowser
import threading
import time
import sys
from pathlib import Path
from preview_template import create_preview

def start_server(port=8000):
    """启动HTTP服务器"""
    
    # 切换到src目录，这样可以访问template_preview.html
    src_dir = Path(__file__).parent
    original_dir = Path.cwd()
    
    try:
        import os
        os.chdir(src_dir)
        
        # 创建服务器
        handler = http.server.SimpleHTTPRequestHandler
        
        # 尝试不同端口
        for attempt_port in range(port, port + 10):
            try:
                with socketserver.TCPServer(("", attempt_port), handler) as httpd:
                    print(f"🌐 HTTP服务器已启动: http://localhost:{attempt_port}")
                    print(f"📄 预览地址: http://localhost:{attempt_port}/template_preview.html")
                    print("🔧 按 Ctrl+C 停止服务器")
                    
                    # 在新线程中打开浏览器
                    def open_browser():
                        time.sleep(1)  # 等待服务器启动
                        try:
                            webbrowser.open(f"http://localhost:{attempt_port}/template_preview.html")
                            print("✅ 已在浏览器中打开预览")
                        except Exception as e:
                            print(f"⚠️ 无法自动打开浏览器: {e}")
                    
                    if "--no-browser" not in sys.argv:
                        browser_thread = threading.Thread(target=open_browser)
                        browser_thread.daemon = True
                        browser_thread.start()
                    
                    # 启动服务器
                    httpd.serve_forever()
                    
            except OSError as e:
                if "Address already in use" in str(e):
                    print(f"⚠️ 端口 {attempt_port} 已被占用，尝试下一个端口...")
                    continue
                else:
                    raise
        
        print("❌ 无法找到可用端口")
        
    except KeyboardInterrupt:
        print("\n👋 服务器已停止")
    finally:
        os.chdir(original_dir)

def main():
    """主函数"""
    print("🏛️ Hermes4ArXiv 邮件模板预览服务器")
    print("=" * 50)
    
    # 首先生成预览文件
    print("📝 正在生成模板预览...")
    result = create_preview()
    if result is None:
        print("❌ 预览生成失败")
        sys.exit(1)
    
    preview_file, _ = result
    print(f"✅ 预览文件已生成: {preview_file}")
    
    # 启动服务器
    print("\n🚀 启动预览服务器...")
    start_server()

if __name__ == "__main__":
    main() 
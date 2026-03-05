#!/usr/bin/env python3
"""
小红书 MCP 远程客户端
通过 ngrok 隧道连接本地 MCP 服务
"""

import requests
import os
import json
from typing import Optional, List, Dict


class XiaohongshuMCPRemoteClient:
    """小红书 MCP 远程客户端"""
    
    def __init__(self, base_url: Optional[str] = None):
        """
        初始化
        
        Args:
            base_url: MCP 服务地址（通过 ngrok 提供）
        """
        self.base_url = base_url or os.environ.get("XHS_MCP_URL")
        if not self.base_url:
            raise ValueError("需要提供 MCP 服务 URL 或设置 XHS_MCP_URL 环境变量")
        
        # 移除末尾的斜杠
        self.base_url = self.base_url.rstrip('/')
    
    def check_status(self) -> bool:
        """检查 MCP 服务状态"""
        try:
            url = f"{self.base_url}/api/v1/login/status"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                is_logged_in = data.get("data", {}).get("is_logged_in", False)
                
                if is_logged_in:
                    print("✅ MCP 服务已连接且已登录")
                    return True
                else:
                    print("⚠️ MCP 服务已连接但未登录")
                    return False
            else:
                print(f"⚠️ MCP 服务返回错误: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ 连接失败: {e}")
            return False
    
    def publish_note(self, title: str, content: str, images: List[str]) -> Optional[Dict]:
        """
        发布图文笔记
        
        Args:
            title: 标题
            content: 正文
            images: 图片 URL 列表
        """
        print(f"\n📝 正在发布笔记: {title[:30]}...")
        
        try:
            url = f"{self.base_url}/api/v1/note/publish"
            
            data = {
                "title": title,
                "content": content,
                "images": images
            }
            
            response = requests.post(url, json=data, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                if result.get("code") == 0:
                    note_id = result.get("data", {}).get("note_id")
                    print(f"✅ 发布成功!")
                    print(f"   Note ID: {note_id}")
                    return {
                        "note_id": note_id,
                        "url": f"https://www.xiaohongshu.com/explore/{note_id}"
                    }
                else:
                    print(f"❌ 发布失败: {result.get('msg')}")
            else:
                print(f"❌ 请求失败: {response.status_code}")
                print(f"   响应: {response.text[:200]}")
                
        except Exception as e:
            print(f"❌ 错误: {e}")
        
        return None
    
    def upload_image(self, image_path: str) -> Optional[str]:
        """上传图片"""
        try:
            url = f"{self.base_url}/api/v1/image/upload"
            
            with open(image_path, 'rb') as f:
                files = {'file': f}
                response = requests.post(url, files=files, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                if result.get("code") == 0:
                    image_url = result.get("data", {}).get("url")
                    print(f"  ✅ 图片上传成功")
                    return image_url
            
            print(f"  ⚠️ 上传失败: {response.status_code}")
            return None
            
        except Exception as e:
            print(f"  ⚠️ 上传错误: {e}")
            return None


def main():
    """测试"""
    import argparse
    
    parser = argparse.ArgumentParser(description="小红书 MCP 远程客户端")
    parser.add_argument("--url", "-u", help="MCP 服务 URL (或设置 XHS_MCP_URL)")
    parser.add_argument("--check", "-c", action="store_true", help="检查连接状态")
    
    args = parser.parse_args()
    
    url = args.url or os.environ.get("XHS_MCP_URL")
    if not url:
        print("❌ 错误: 需要提供 --url 或设置 XHS_MCP_URL 环境变量")
        return
    
    client = XiaohongshuMCPRemoteClient(url)
    
    if args.check or True:
        client.check_status()


if __name__ == "__main__":
    main()

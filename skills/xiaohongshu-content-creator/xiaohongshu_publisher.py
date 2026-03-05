#!/usr/bin/env python3
"""
小红书发布客户端
使用 Cookie 直接发布笔记
"""

import requests
import json
import os
import re
import time
from typing import Optional, List, Dict
from pathlib import Path


class XiaohongshuPublisher:
    """小红书发布器"""
    
    def __init__(self, cookie: Optional[str] = None):
        """
        初始化
        
        Args:
            cookie: 小红书 Cookie，如果不提供则从环境变量读取
        """
        self.cookie = cookie or os.environ.get("XHS_COOKIE")
        if not self.cookie:
            raise ValueError("需要提供 Cookie 或设置 XHS_COOKIE 环境变量")
        
        self.session = requests.Session()
        self._setup_headers()
    
    def _setup_headers(self):
        """设置请求头"""
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Content-Type": "application/json;charset=utf-8",
            "Origin": "https://www.xiaohongshu.com",
            "Referer": "https://www.xiaohongshu.com/",
            "Cookie": self.cookie
        })
    
    def get_user_info(self) -> Optional[Dict]:
        """获取当前用户信息"""
        try:
            url = "https://edith.xiaohongshu.com/api/sns/web/v1/user/selfinfo"
            response = self.session.get(url, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("code") == 0:
                    user = data.get("data", {})
                    print(f"✅ 登录成功: {user.get('nickname', '未知用户')}")
                    return user
            
            print(f"⚠️ 获取用户信息失败: {response.status_code}")
            return None
            
        except Exception as e:
            print(f"❌ 错误: {e}")
            return None
    
    def publish_note(self, title: str, content: str, images: List[str], 
                     topics: Optional[List[str]] = None) -> Optional[Dict]:
        """
        发布图文笔记
        
        Args:
            title: 标题
            content: 正文内容
            images: 图片路径列表（本地路径或URL）
            topics: 话题标签列表
        
        Returns:
            发布结果
        """
        print(f"\n📝 正在发布笔记: {title[:30]}...")
        
        # 上传图片
        image_urls = []
        for img_path in images:
            if img_path.startswith("http"):
                image_urls.append(img_path)
            else:
                url = self._upload_image(img_path)
                if url:
                    image_urls.append(url)
                time.sleep(0.5)  # 避免请求过快
        
        if not image_urls:
            print("❌ 没有可用的图片")
            return None
        
        # 构建发布数据
        note_data = {
            "title": title,
            "desc": content,
            "images": [{"url": url, "width": 1080, "height": 1440} for url in image_urls],
            "topics": [{"name": t} for t in (topics or [])],
            "type": "normal"
        }
        
        try:
            url = "https://edith.xiaohongshu.com/api/sns/web/v1/note/publish"
            response = self.session.post(url, json=note_data, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("code") == 0:
                    note_id = data.get("data", {}).get("note_id")
                    print(f"✅ 发布成功! Note ID: {note_id}")
                    return {
                        "note_id": note_id,
                        "url": f"https://www.xiaohongshu.com/explore/{note_id}"
                    }
                else:
                    print(f"❌ 发布失败: {data.get('msg')}")
            else:
                print(f"❌ 请求失败: {response.status_code}")
                
        except Exception as e:
            print(f"❌ 错误: {e}")
        
        return None
    
    def _upload_image(self, image_path: str) -> Optional[str]:
        """上传图片到小红书"""
        try:
            # 获取上传凭证
            url = "https://edith.xiaohongshu.com/api/sns/web/v1/upload/obtain"
            response = self.session.get(url, timeout=30)
            
            if response.status_code != 200:
                print(f"  ⚠️ 获取上传凭证失败")
                return None
            
            upload_info = response.json().get("data", {})
            
            # 上传图片
            with open(image_path, 'rb') as f:
                files = {'file': f}
                upload_response = requests.post(
                    upload_info['upload_url'],
                    data=upload_info.get('upload_params', {}),
                    files=files,
                    timeout=60
                )
            
            if upload_response.status_code == 200:
                return upload_info.get('image_url')
            else:
                print(f"  ⚠️ 上传失败: {upload_response.status_code}")
                return None
                
        except Exception as e:
            print(f"  ⚠️ 上传错误: {e}")
            return None
    
    def publish_from_creator(self, story: Dict, copy: Dict, images: List[str]) -> Optional[Dict]:
        """
        从内容创作结果发布
        
        Args:
            story: 故事数据
            copy: 文案数据
            images: 图片路径列表
        
        Returns:
            发布结果
        """
        title = copy.get('title', story.get('title', '无标题'))
        content = copy.get('content', '')
        
        # 提取话题标签
        topics = re.findall(r'#(\w+)', content)
        
        # 清理内容（移除话题标签用于正文）
        clean_content = re.sub(r'#\w+\s*', '', content).strip()
        
        return self.publish_note(title, clean_content, images, topics)


def main():
    """测试发布"""
    import argparse
    
    parser = argparse.ArgumentParser(description="小红书发布工具")
    parser.add_argument("--title", "-t", required=True, help="笔记标题")
    parser.add_argument("--content", "-c", required=True, help="笔记内容")
    parser.add_argument("--images", "-i", nargs="+", required=True, help="图片路径")
    parser.add_argument("--cookie", help="Cookie（或设置 XHS_COOKIE 环境变量）")
    
    args = parser.parse_args()
    
    cookie = args.cookie or os.environ.get("XHS_COOKIE")
    if not cookie:
        print("❌ 错误: 需要提供 Cookie")
        print("   方式1: --cookie 'your_cookie'")
        print("   方式2: export XHS_COOKIE='your_cookie'")
        return
    
    publisher = XiaohongshuPublisher(cookie)
    
    # 验证登录
    user = publisher.get_user_info()
    if not user:
        print("❌ Cookie 无效或已过期")
        return
    
    # 发布
    result = publisher.publish_note(args.title, args.content, args.images)
    
    if result:
        print(f"\n✅ 发布成功!")
        print(f"   链接: {result['url']}")
    else:
        print("\n❌ 发布失败")


if __name__ == "__main__":
    main()

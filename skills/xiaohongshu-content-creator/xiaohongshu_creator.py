#!/usr/bin/env python3
"""
小红书内容创作助手
从想法到发布的完整工作流
"""

import os
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional


class ContentCreator:
    """小红书内容创作器"""
    
    def __init__(self, config_path: Optional[str] = None):
        self.config = self._load_config(config_path)
        self.output_dir = "content-output"
        os.makedirs(self.output_dir, exist_ok=True)
    
    def _load_config(self, config_path: Optional[str]) -> Dict:
        """加载配置"""
        default_config = {
            "story": {"default_length": "medium", "tone": "humorous", "educational": True},
            "comic": {"style": "cartoon", "panels": 4, "size": "1024x1024"},
            "copy": {"style": "casual", "emoji": True, "hashtags": ["#程序员", "#职场", "#搞笑"]},
            "publish": {"auto_publish": False}
        }
        return default_config
    
    def generate_story(self, idea: str, length: str = "medium", 
                      tone: str = "humorous", educational_theme: str = "") -> Dict:
        """生成幽默教育故事"""
        print(f"\n✍️ 正在生成故事: {idea}")
        
        story = self._mock_generate_story(idea, tone, educational_theme)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        story_path = os.path.join(self.output_dir, f"story_{timestamp}.md")
        
        with open(story_path, 'w', encoding='utf-8') as f:
            f.write(f"# {story['title']}\n\n")
            f.write(f"**主题**: {idea}\n**风格**: {tone}\n\n")
            f.write("## 故事\n\n" + story['content'])
            f.write("\n\n## 教育意义\n\n" + story['moral'])
            f.write("\n\n## 漫画分镜\n\n")
            for i, panel in enumerate(story['panels'], 1):
                f.write(f"{i}. {panel}\n")
        
        print(f"✅ 故事已保存: {story_path}")
        return {**story, "path": story_path, "idea": idea}
    
    def _mock_generate_story(self, idea: str, tone: str, theme: str) -> Dict:
        """模拟生成故事"""
        if "程序员" in idea or "产品经理" in idea:
            return {
                "title": "产品经理的'简单'需求",
                "content": """程序员小明正在专心写代码，产品经理小红走过来...

小红："小明，这个按钮能不能改一下？"
小明："可以，怎么改？"
小红："很简单，就改一点点..."

（2小时后）

小红："对了，还要支持夜间模式、多语言、手势操作、语音控制！"

小明："这叫'一点点'？！这得重构整个架构！"

小红："啊？我以为就是改个颜色的事...""",
                "moral": "沟通需求时要明确范围，避免理解偏差。",
                "panels": [
                    "程序员认真coding，产品经理走过来说'有个简单需求'",
                    "产品经理说'就改个按钮颜色'，程序员点头",
                    "需求越加越多，程序员表情逐渐凝固",
                    "程序员崩溃大喊'这叫一点点？！'，产品经理无辜眨眼"
                ]
            }
        elif "减肥" in idea or "健身" in idea:
            return {
                "title": "减肥第一天vs减肥第一周",
                "content": """小王决定开始减肥...

第一天：买了瑜伽垫、哑铃、跑步机、蛋白粉...

第三天："今天太累了，休息一天没关系吧？"

第七天：瑜伽垫用来睡觉还挺舒服的...

朋友："你不是要减肥吗？"
小王："我在研究敌人的战术！""",
                "moral": "制定计划要循序渐进，坚持比强度更重要。",
                "panels": [
                    "主角信心满满，买了一堆健身器材",
                    "主角在跑步机上跑了5分钟，气喘吁吁",
                    "主角躺在瑜伽垫上刷手机",
                    "朋友问'不是减肥吗？'，主角说'在研究美食战术'"
                ]
            }
        else:
            return {
                "title": f"关于{idea}的那些事",
                "content": f"这是一个关于{idea}的有趣故事...",
                "moral": f"从{idea}中我们学到了重要的一课。",
                "panels": [f"场景{i}: {idea}相关画面" for i in range(1, 5)]
            }
    
    def generate_xiaohongshu_copy(self, story: Dict) -> Dict:
        """生成小红书文案"""
        print("\n📝 正在生成小红书文案...")
        
        title = f"{story['title']}...😭"
        
        content = f"""{story['content'][:200]}...

💡 {story['moral']}

👇 你们遇到过这种情况吗？评论区聊聊～

#搞笑 #职场 #内容过于真实 #打工人日常"""
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        copy_path = os.path.join(self.output_dir, f"copy_{timestamp}.md")
        
        with open(copy_path, 'w', encoding='utf-8') as f:
            f.write(f"# {title}\n\n{content}")
        
        print(f"✅ 文案已保存: {copy_path}")
        
        return {"title": title, "content": content, "path": copy_path}
    
    def create_and_publish(self, idea: str, auto_publish: bool = False) -> Dict:
        """完整工作流：生成并发布"""
        print("=" * 60)
        print("🚀 小红书内容创作工作流")
        print("=" * 60)
        
        # 1. 生成故事
        story = self.generate_story(idea)
        
        # 2. 生成漫画提示词
        comic_prompts = []
        for panel in story['panels']:
            prompt = f"Cartoon comic, funny: {panel}. Style: Cute, exaggerated, vibrant colors"
            comic_prompts.append(prompt)
        
        print(f"\n🎨 漫画提示词已生成 ({len(comic_prompts)} 个):")
        for i, p in enumerate(comic_prompts, 1):
            print(f"  格{i}: {p[:50]}...")
        
        # 3. 生成小红书文案
        copy = self.generate_xiaohongshu_copy(story)
        
        # 4. 发布状态
        publish_status = "模拟模式（未实际发布）"
        if auto_publish:
            publish_status = "已启用自动发布（需要配置XHS_COOKIE）"
        
        print("\n" + "=" * 60)
        print("✅ 内容创作完成!")
        print("=" * 60)
        print(f"\n📄 故事: {story['path']}")
        print(f"📝 文案: {copy['path']}")
        print(f"📤 发布: {publish_status}")
        
        return {
            "story": story,
            "copy": copy,
            "comic_prompts": comic_prompts,
            "publish_status": publish_status
        }


def main():
    parser = argparse.ArgumentParser(description="小红书内容创作助手")
    parser.add_argument("--idea", "-i", required=True, help="内容想法/主题")
    parser.add_argument("--publish", "-p", action="store_true", help="自动发布")
    
    args = parser.parse_args()
    
    creator = ContentCreator()
    result = creator.create_and_publish(args.idea, auto_publish=args.publish)
    
    print("\n📝 生成的小红书文案:")
    print("-" * 60)
    print(f"标题: {result['copy']['title']}")
    print(f"\n内容:\n{result['copy']['content']}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
AI 绘画 API 接入模块
支持多个平台: Pollinations(免费), SiliconFlow, OpenAI DALL-E
"""

import os
import sys
import json
import base64
import requests
from pathlib import Path
from typing import Optional, List, Dict
from urllib.parse import quote


class AIImageGenerator:
    """AI 图像生成器"""
    
    def __init__(self, provider: str = "pollinations"):
        """
        初始化
        
        Args:
            provider: pollinations / siliconflow / openai
        """
        self.provider = provider
        self.api_key = None
        
        # 加载 API key
        if provider == "siliconflow":
            self.api_key = os.environ.get("SILICONFLOW_API_KEY")
        elif provider == "openai":
            self.api_key = os.environ.get("OPENAI_API_KEY")
        
        print(f"🎨 初始化 AI 绘画: {provider}")
    
    def generate(self, prompt: str, width: int = 1024, height: int = 1024, 
                 seed: Optional[int] = None, output_path: Optional[str] = None) -> str:
        """
        生成图片
        
        Args:
            prompt: 绘画提示词
            width: 图片宽度
            height: 图片高度
            seed: 随机种子
            output_path: 输出路径
        
        Returns:
            图片路径或 URL
        """
        if self.provider == "pollinations":
            return self._generate_pollinations(prompt, width, height, seed, output_path)
        elif self.provider == "siliconflow":
            return self._generate_siliconflow(prompt, width, height, seed, output_path)
        elif self.provider == "openai":
            return self._generate_openai(prompt, output_path)
        else:
            raise ValueError(f"不支持的 provider: {self.provider}")
    
    def _generate_pollinations(self, prompt: str, width: int, height: int,
                               seed: Optional[int], output_path: Optional[str]) -> str:
        """使用 Pollinations (免费)"""
        print(f"  使用 Pollinations 生成...")
        
        # URL 编码提示词
        encoded_prompt = quote(prompt)
        
        # 构建 URL
        url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width={width}&height={height}"
        
        if seed is not None:
            url += f"&seed={seed}"
        
        url += "&nologo=true"
        
        # 下载图片
        if output_path is None:
            output_path = f"generated_{seed or 'random'}.png"
        
        try:
            response = requests.get(url, timeout=120)
            response.raise_for_status()
            
            with open(output_path, 'wb') as f:
                f.write(response.content)
            
            print(f"  ✅ 图片已保存: {output_path}")
            return output_path
            
        except Exception as e:
            print(f"  ⚠️ Pollinations 失败: {e}")
            print(f"  🔄 尝试备用方案...")
            return self._generate_prompt_file(prompt, output_path)
    
    def _generate_prompt_file(self, prompt: str, output_path: Optional[str]) -> str:
        """备用方案：保存绘画提示词"""
        print("  📝 保存绘画提示词...")
        
        if output_path is None:
            output_path = "generated_prompt.txt"
        else:
            output_path = output_path.replace('.png', '_prompt.txt').replace('.jpg', '_prompt.txt')
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(f"AI 绘画提示词:\n")
            f.write(f"{'='*60}\n")
            f.write(f"{prompt}\n")
            f.write(f"{'='*60}\n\n")
            f.write("建议使用的 AI 绘画工具:\n")
            f.write("1. Pollinations (免费): https://pollinations.ai\n")
            f.write("2. SiliconFlow: https://siliconflow.cn\n")
            f.write("3. Midjourney: https://midjourney.com\n")
        
        print(f"  ✅ 提示词已保存: {output_path}")
        return output_path
    
    def _generate_siliconflow(self, prompt: str, width: int, height: int,
                              seed: Optional[int], output_path: Optional[str]) -> str:
        """使用 SiliconFlow"""
        print(f"  使用 SiliconFlow 生成...")
        
        if not self.api_key:
            print("  ❌ 错误: 需要 SILICONFLOW_API_KEY")
            return None
        
        url = "https://api.siliconflow.cn/v1/images/generations"
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "black-forest-labs/FLUX.1-schnell",
            "prompt": prompt,
            "image_size": f"{width}x{height}"
        }
        
        if seed is not None:
            payload["seed"] = seed
        
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=60)
            response.raise_for_status()
            
            result = response.json()
            image_url = result["images"][0]["url"]
            
            # 下载图片
            if output_path is None:
                output_path = f"generated_{seed or 'random'}.png"
            
            img_response = requests.get(image_url, timeout=30)
            img_response.raise_for_status()
            
            with open(output_path, 'wb') as f:
                f.write(img_response.content)
            
            print(f"  ✅ 图片已保存: {output_path}")
            return output_path
            
        except Exception as e:
            print(f"  ❌ 生成失败: {e}")
            return None
    
    def _generate_openai(self, prompt: str, output_path: Optional[str]) -> str:
        """使用 OpenAI DALL-E"""
        print(f"  使用 OpenAI DALL-E 生成...")
        
        if not self.api_key:
            print("  ❌ 错误: 需要 OPENAI_API_KEY")
            return None
        
        url = "https://api.openai.com/v1/images/generations"
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "dall-e-3",
            "prompt": prompt,
            "size": "1024x1024",
            "quality": "standard",
            "n": 1
        }
        
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=60)
            response.raise_for_status()
            
            result = response.json()
            image_url = result["data"][0]["url"]
            
            # 下载图片
            if output_path is None:
                output_path = "generated_dalle.png"
            
            img_response = requests.get(image_url, timeout=30)
            img_response.raise_for_status()
            
            with open(output_path, 'wb') as f:
                f.write(img_response.content)
            
            print(f"  ✅ 图片已保存: {output_path}")
            return output_path
            
        except Exception as e:
            print(f"  ❌ 生成失败: {e}")
            return None
    
    def generate_comic_strip(self, panels: List[str], output_dir: str = "comics") -> List[str]:
        """
        生成多格漫画
        
        Args:
            panels: 每格的提示词列表
            output_dir: 输出目录
        
        Returns:
            生成的图片路径列表
        """
        print(f"\n🎨 生成 {len(panels)} 格漫画...")
        
        os.makedirs(output_dir, exist_ok=True)
        
        paths = []
        for i, panel_prompt in enumerate(panels, 1):
            print(f"\n  生成第 {i}/{len(panels)} 格...")
            
            # 添加漫画风格前缀
            full_prompt = f"Cartoon comic style, funny illustration: {panel_prompt}. "
            full_prompt += "Style: Cute cartoon, exaggerated expressions, vibrant colors, "
            full_prompt += "clean lines, white background, 4-panel comic layout"
            
            output_path = os.path.join(output_dir, f"panel_{i:02d}.png")
            
            path = self.generate(full_prompt, width=1024, height=1024, 
                                seed=i*100, output_path=output_path)
            
            if path:
                paths.append(path)
        
        print(f"\n✅ 漫画生成完成: {len(paths)}/{len(panels)} 张")
        return paths

    def generate_prompts_only(self, panels: List[str], output_dir: str = "comics") -> List[str]:
        """
        仅生成绘画提示词（当 API 不可用时）
        
        Args:
            panels: 每格的描述
            output_dir: 输出目录
        
        Returns:
            提示词文件路径列表
        """
        print(f"\n📝 生成 {len(panels)} 个绘画提示词...")
        
        os.makedirs(output_dir, exist_ok=True)
        
        paths = []
        for i, panel in enumerate(panels, 1):
            full_prompt = f"Cartoon comic: {panel}. Style: Cute, exaggerated, vibrant colors"
            
            output_path = os.path.join(output_dir, f"panel_{i:02d}_prompt.txt")
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(full_prompt)
            
            paths.append(output_path)
            print(f"  格{i}: {full_prompt[:50]}...")
        
        print(f"\n✅ 提示词已保存到: {output_dir}")
        return paths


def main():
    """测试"""
    import argparse
    
    parser = argparse.ArgumentParser(description="AI 绘画生成器")
    parser.add_argument("--prompt", "-p", required=True, help="绘画提示词")
    parser.add_argument("--provider", "-pr", default="pollinations", 
                       choices=["pollinations", "siliconflow", "openai"],
                       help="API 提供商")
    parser.add_argument("--output", "-o", default="generated.png", help="输出路径")
    
    args = parser.parse_args()
    
    generator = AIImageGenerator(provider=args.provider)
    result = generator.generate(args.prompt, output_path=args.output)
    
    if result:
        print(f"\n✅ 图片已生成: {result}")
    else:
        print("\n❌ 生成失败")


if __name__ == "__main__":
    main()

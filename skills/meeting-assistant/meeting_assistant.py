#!/usr/bin/env python3
"""
Meeting Assistant - OpenClaw Skill
智能会议助手封装
"""

import os
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime

# 确保可以导入 skill 目录下的模块
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from transcribe import AudioTranscriber
    from generate_summary import MeetingSummarizer
    from extract_tasks import TaskExtractor, TaskAutomation
    MODULES_AVAILABLE = True
except ImportError:
    MODULES_AVAILABLE = False
    print("警告: 核心模块未找到，将使用模拟模式")


class MeetingAssistant:
    """智能会议助手主类"""
    
    def __init__(self, whisper_model="base", llm_api="kimi"):
        self.whisper_model = whisper_model
        self.llm_api = llm_api
        
        if MODULES_AVAILABLE:
            self.transcriber = AudioTranscriber(model_size=whisper_model)
            self.summarizer = MeetingSummarizer(api_type=llm_api)
            self.task_extractor = TaskExtractor()
        else:
            self.transcriber = None
            self.summarizer = None
            self.task_extractor = None
    
    def process_meeting(self, audio_path, auto_execute=False):
        """
        处理会议录音完整流程
        
        Args:
            audio_path: 音频文件路径
            auto_execute: 是否自动执行任务
        
        Returns:
            dict: 处理结果
        """
        if not MODULES_AVAILABLE:
            return self._mock_process(audio_path)
        
        print("=" * 70)
        print("🎙️ 智能会议助手 - 开始处理")
        print("=" * 70)
        
        base_name = Path(audio_path).stem
        
        # 步骤1: 语音转文字
        print("\n📍 步骤 1/4: 语音转文字")
        print("-" * 70)
        transcript_result = self.transcriber.transcribe(
            audio_path, 
            output_dir="transcripts"
        )
        
        # 步骤2: 生成会议纪要
        print("\n📍 步骤 2/4: 生成会议纪要")
        print("-" * 70)
        summary_result = self.summarizer.generate_summary(
            transcript_result["text_path"],
            output_dir="summaries"
        )
        
        # 步骤3: 提取任务
        print("\n📍 步骤 3/4: 提取任务")
        print("-" * 70)
        task_result = self.task_extractor.extract_tasks(
            summary_result["summary_path"],
            output_dir="tasks"
        )
        
        # 步骤4: 自动执行
        if auto_execute:
            print("\n📍 步骤 4/4: 自动执行任务")
            print("-" * 70)
            automation = TaskAutomation(task_result["tasks"])
            automation.execute_automation()
        
        # 生成报告
        self._generate_report(base_name, transcript_result, summary_result, task_result)
        
        print("\n" + "=" * 70)
        print("✅ 处理完成!")
        print("=" * 70)
        
        return {
            "meeting": base_name,
            "transcript": transcript_result,
            "summary": summary_result,
            "tasks": task_result
        }
    
    def _mock_process(self, audio_path):
        """模拟处理 - 用于演示"""
        print("\n🎙️ 智能会议助手 (模拟模式)")
        print("=" * 70)
        
        base_name = Path(audio_path).stem
        
        # 创建输出目录
        for dir_name in ["transcripts", "summaries", "tasks", "reports"]:
            os.makedirs(dir_name, exist_ok=True)
        
        # 模拟转录
        transcript_text = """
[00:00] 张三: 大家好，今天我们讨论 Q2 的产品规划。

[00:15] 李四: 我建议我们采用微服务架构，这样可以更好地扩展。

[00:30] 王五: 设计方面，我需要两周时间完成原型。

[00:45] 张三: 好的，那我们就确定采用微服务架构。

[01:00] 李四: 我负责技术方案，下周五前完成文档。

[01:15] 张三: 会议结束，大家按计划执行。
        """.strip()
        
        transcript_path = f"transcripts/{base_name}.txt"
        with open(transcript_path, "w", encoding="utf-8") as f:
            f.write(transcript_text)
        
        print(f"✅ 转录完成: {transcript_path}")
        
        # 模拟会议纪要
        summary = """# 会议纪要 - Q2 产品规划讨论

**会议时间**: 2026-03-05 14:00

## 参会人员
- 张三 (产品经理)
- 李四 (技术负责人)
- 王五 (UI设计师)

## 主要议题
1. Q2 产品技术架构选型
2. 项目时间规划

## 决策事项
- ✅ 采用微服务架构

## 待办任务
| 任务 | 负责人 | 截止日期 |
|------|--------|----------|
| 完成技术方案文档 | 李四 | 2026-03-10 |
| 设计UI原型 | 王五 | 2026-03-12 |
"""
        
        summary_path = f"summaries/{base_name}_summary.md"
        with open(summary_path, "w", encoding="utf-8") as f:
            f.write(summary)
        
        print(f"✅ 纪要生成: {summary_path}")
        
        # 模拟任务
        tasks = [
            {"id": "TASK-001", "title": "完成技术方案文档", "assignee": "李四", "due_date": "2026-03-10"},
            {"id": "TASK-002", "title": "设计UI原型", "assignee": "王五", "due_date": "2026-03-12"}
        ]
        
        tasks_path = f"tasks/{base_name}_tasks.json"
        with open(tasks_path, "w", encoding="utf-8") as f:
            json.dump({"tasks": tasks}, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 任务提取: {tasks_path}")
        print(f"\n📋 共提取 {len(tasks)} 个任务")
        
        return {
            "meeting": base_name,
            "transcript": {"text_path": transcript_path},
            "summary": {"summary_path": summary_path},
            "tasks": {"json_path": tasks_path, "tasks": tasks}
        }
    
    def _generate_report(self, base_name, transcript, summary, tasks):
        """生成处理报告"""
        os.makedirs("reports", exist_ok=True)
        report_path = f"reports/{base_name}_report.md"
        
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(f"# 📊 会议处理报告 - {base_name}\n\n")
            f.write(f"处理时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            f.write("## 📁 生成文件\n\n")
            f.write(f"- 转录文本: `{transcript.get('text_path', 'N/A')}`\n")
            f.write(f"- 会议纪要: `{summary.get('summary_path', 'N/A')}`\n")
            f.write(f"- 任务清单: `{tasks.get('md_path', 'N/A')}`\n\n")
            
            f.write(f"## 📋 提取的任务 ({len(tasks.get('tasks', []))}个)\n\n")
            for task in tasks.get('tasks', []):
                f.write(f"- **{task['title']}** ({task['assignee']})\n")
        
        print(f"\n📄 报告已生成: {report_path}")


def main():
    parser = argparse.ArgumentParser(
        description="智能会议助手 - 语音转文字 → 会议纪要 → 任务自动化",
        prog="meeting-assistant"
    )
    
    parser.add_argument("--input", "-i", required=True,
                       help="会议录音文件路径 (MP3/WAV/M4A)")
    parser.add_argument("--model", "-m", default="base",
                       choices=["tiny", "base", "small", "medium", "large"],
                       help="Whisper 模型大小 (默认: base)")
    parser.add_argument("--api", "-a", default="kimi",
                       choices=["openai", "kimi", "mock"],
                       help="LLM API 类型")
    parser.add_argument("--auto-execute", action="store_true",
                       help="自动执行提取的任务")
    parser.add_argument("--language", "-l", default="zh",
                       help="音频语言 (默认: zh)")
    
    args = parser.parse_args()
    
    if not os.path.exists(args.input):
        print(f"❌ 错误: 文件不存在 - {args.input}")
        sys.exit(1)
    
    # 创建输出目录
    for dir_name in ["transcripts", "summaries", "tasks", "reports"]:
        os.makedirs(dir_name, exist_ok=True)
    
    # 运行处理
    assistant = MeetingAssistant(
        whisper_model=args.model,
        llm_api=args.api
    )
    
    try:
        result = assistant.process_meeting(
            args.input,
            auto_execute=args.auto_execute
        )
        
        print("\n📂 输出文件:")
        print(f"  📄 转录: {result['transcript'].get('text_path', 'N/A')}")
        print(f"  📝 纪要: {result['summary'].get('summary_path', 'N/A')}")
        print(f"  📋 任务: {result['tasks'].get('md_path', result['tasks'].get('json_path', 'N/A'))}")
        
    except Exception as e:
        print(f"\n❌ 处理失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

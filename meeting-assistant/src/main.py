#!/usr/bin/env python3
"""
主程序 - 完整流程自动化
语音转文字 → 生成会议纪要 → 提取任务 → 自动执行
"""

import os
import sys
import argparse
from pathlib import Path

# 导入各模块
from transcribe import AudioTranscriber
from generate_summary import MeetingSummarizer
from extract_tasks import TaskExtractor, TaskAutomation


class MeetingAssistant:
    """会议助手 - 完整自动化流程"""
    
    def __init__(self, whisper_model="base", llm_api="kimi"):
        self.whisper_model = whisper_model
        self.llm_api = llm_api
        
        # 初始化各模块
        self.transcriber = AudioTranscriber(model_size=whisper_model)
        self.summarizer = MeetingSummarizer(api_type=llm_api)
        self.task_extractor = TaskExtractor()
    
    def process_meeting(self, audio_path, auto_execute=False):
        """
        处理会议录音完整流程
        
        Args:
            audio_path: 音频文件路径
            auto_execute: 是否自动执行任务
        
        Returns:
            dict: 处理结果
        """
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
        
        # 步骤4: 自动执行 (可选)
        if auto_execute:
            print("\n📍 步骤 4/4: 自动执行任务")
            print("-" * 70)
            automation = TaskAutomation(task_result["tasks"])
            automation.execute_automation()
        else:
            print("\n📍 步骤 4/4: 自动执行 (已跳过)")
            print("-" * 70)
            print("提示: 使用 --auto-execute 启用自动执行")
        
        # 生成最终报告
        self._generate_final_report(base_name, transcript_result, summary_result, task_result)
        
        print("\n" + "=" * 70)
        print("✅ 处理完成!")
        print("=" * 70)
        
        return {
            "meeting": base_name,
            "transcript": transcript_result,
            "summary": summary_result,
            "tasks": task_result
        }
    
    def _generate_final_report(self, base_name, transcript, summary, tasks):
        """生成最终处理报告"""
        report_path = f"reports/{base_name}_report.md"
        os.makedirs("reports", exist_ok=True)
        
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(f"# 📊 会议处理报告 - {base_name}\n\n")
            f.write(f"处理时间: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            f.write("## 📁 生成文件\n\n")
            f.write(f"| 类型 | 文件路径 |\n")
            f.write(f"|------|----------|\n")
            f.write(f"| 转录文本 | `{transcript['text_path']}` |\n")
            f.write(f"| 会议纪要 | `{summary['summary_path']}` |\n")
            f.write(f"| 任务清单 | `{tasks['md_path']}` |\n")
            f.write(f"| 任务数据 | `{tasks['json_path']}` |\n")
            f.write("\n")
            
            f.write("## 📋 提取的任务\n\n")
            f.write(f"共提取 **{len(tasks['tasks'])}** 个任务\n\n")
            
            for task in tasks['tasks']:
                priority_emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(task['priority'], "⚪")
                f.write(f"- {priority_emoji} **{task['title']}** ({task['assignee']}) - 截止: {task['due_date']}\n")
            
            f.write("\n## 📝 会议纪要摘要\n\n")
            f.write(summary['summary'][:1000] + "\n...\n" if len(summary['summary']) > 1000 else summary['summary'])
        
        print(f"\n📄 最终报告已生成: {report_path}")


def main():
    parser = argparse.ArgumentParser(
        description="智能会议助手 - 语音转文字 → 会议纪要 → 任务自动化",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 基本使用
  python main.py -i meeting.mp3
  
  # 启用自动执行
  python main.py -i meeting.mp3 --auto-execute
  
  # 使用更大的模型
  python main.py -i meeting.mp3 --model medium
        """
    )
    
    parser.add_argument("--input", "-i", required=True,
                       help="会议录音文件路径 (MP3/WAV/M4A)")
    parser.add_argument("--model", "-m", default="base",
                       choices=["tiny", "base", "small", "medium", "large"],
                       help="Whisper 模型大小 (默认: base)")
    parser.add_argument("--api", "-a", default="kimi",
                       choices=["openai", "kimi", "mock"],
                       help="LLM API 类型 (默认: kimi)")
    parser.add_argument("--auto-execute", action="store_true",
                       help="自动执行提取的任务")
    parser.add_argument("--language", "-l", default="zh",
                       help="音频语言 (默认: zh)")
    
    args = parser.parse_args()
    
    # 检查输入文件
    if not os.path.exists(args.input):
        print(f"❌ 错误: 文件不存在 - {args.input}")
        sys.exit(1)
    
    # 创建输出目录
    for dir_name in ["transcripts", "summaries", "tasks", "reports"]:
        os.makedirs(dir_name, exist_ok=True)
    
    # 运行处理流程
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
        print(f"  📄 转录: {result['transcript']['text_path']}")
        print(f"  📝 纪要: {result['summary']['summary_path']}")
        print(f"  📋 任务: {result['tasks']['md_path']}")
        
    except Exception as e:
        print(f"\n❌ 处理失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

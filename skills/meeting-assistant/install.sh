#!/bin/bash
# Meeting Assistant Skill 安装脚本

echo "🎙️ 安装智能会议助手 Skill..."

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: 需要 Python 3"
    exit 1
fi

# 检查 ffmpeg
if ! command -v ffmpeg &> /dev/null; then
    echo "⚠️  警告: 未找到 ffmpeg，正在安装..."
    if command -v apt-get &> /dev/null; then
        sudo apt-get update && sudo apt-get install -y ffmpeg
    elif command -v brew &> /dev/null; then
        brew install ffmpeg
    else
        echo "请手动安装 ffmpeg: https://ffmpeg.org/download.html"
    fi
fi

# 安装 Python 依赖
echo "📦 安装依赖..."
pip install -q openai-whisper openai

# 创建目录
echo "📁 创建目录..."
mkdir -p transcripts summaries tasks reports audio

echo ""
echo "✅ 安装完成!"
echo ""
echo "使用方法:"
echo "  meeting-assistant -i meeting.mp3"
echo ""
echo "或使用 Python:"
echo "  from meeting_assistant import MeetingAssistant"
echo "  assistant = MeetingAssistant()"
echo "  assistant.process_meeting('meeting.mp3')"

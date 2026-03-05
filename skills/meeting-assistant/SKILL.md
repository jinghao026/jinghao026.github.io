---
name: meeting-assistant
description: 智能会议助手 - 语音转文字、生成会议纪要、自动提取任务并执行。支持录音文件自动处理，输出结构化会议纪要和任务清单。
metadata:
  openclaw:
    requires:
      bins: ["python3", "ffmpeg"]
      env: ["OPENAI_API_KEY"]
    optionalEnv: ["KIMI_API_KEY"]
---

# Meeting Assistant Skill

智能会议助手，自动化处理会议录音，生成会议纪要并提取任务。

## 功能

- 🎙️ **语音转文字** - 使用 Whisper 高精度识别
- 📝 **会议纪要生成** - AI 自动生成结构化纪要
- 📋 **任务自动提取** - 从纪要中提取待办任务
- 🤖 **工作流自动化** - 自动创建任务、发送通知

## 安装依赖

```bash
pip install openai-whisper openai
```

## 使用方法

### 快速开始

```python
from meeting_assistant import MeetingAssistant

# 创建助手实例
assistant = MeetingAssistant(
    whisper_model="base",  # tiny/base/small/medium/large
    llm_api="kimi"         # kimi/openai
)

# 处理会议录音
result = assistant.process_meeting(
    audio_path="meeting.mp3",
    auto_execute=True  # 自动执行任务
)

print(f"转录文本: {result['transcript']['text_path']}")
print(f"会议纪要: {result['summary']['summary_path']}")
print(f"任务清单: {result['tasks']['md_path']}")
```

### 命令行使用

```bash
# 基本使用
meeting-assistant -i meeting.mp3

# 启用自动执行
meeting-assistant -i meeting.mp3 --auto-execute

# 使用更大的模型
meeting-assistant -i meeting.mp3 --model medium
```

### GitHub Actions 自动化

创建 `.github/workflows/meeting.yml`:

```yaml
name: Meeting Assistant

on:
  push:
    paths:
      - 'audio/**'
  workflow_dispatch:

jobs:
  process:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Meeting Assistant
        uses: openclaw/meeting-assistant@v1
        with:
          audio-path: 'audio/meeting.mp3'
          auto-execute: true
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
```

## 配置

创建 `meeting-config.yaml`:

```yaml
whisper:
  model: base
  language: zh

llm:
  provider: kimi
  temperature: 0.3

tasks:
  auto_create_issues: true
  notify_assignees: true

notifications:
  slack:
    enabled: true
    webhook_url: ${{ secrets.SLACK_WEBHOOK }}
```

## 输出文件

```
meeting-assistant/
├── transcripts/          # 转录文本
│   └── meeting.txt
├── summaries/            # 会议纪要
│   └── meeting_summary.md
├── tasks/                # 任务清单
│   └── meeting_tasks.md
└── reports/              # 处理报告
    └── meeting_report.md
```

## 会议纪要格式

```markdown
# 会议纪要 - 2026-03-05

## 参会人员
- 张三 (产品经理)
- 李四 (技术负责人)

## 主要议题
1. Q2 产品规划
2. 技术架构选型

## 决策事项
- ✅ 采用微服务架构

## 待办任务
| 任务 | 负责人 | 截止日期 |
|------|--------|----------|
| 完成技术方案 | 李四 | 2026-03-10 |
```

## 环境变量

| 变量 | 必需 | 说明 |
|------|------|------|
| `OPENAI_API_KEY` | 是 | OpenAI API 密钥 |
| `KIMI_API_KEY` | 否 | Kimi API 密钥 |
| `SLACK_WEBHOOK` | 否 | Slack 通知 |

## 示例

### 示例1: 处理本地录音

```python
from meeting_assistant import MeetingAssistant

assistant = MeetingAssistant()
result = assistant.process_meeting("weekly-meeting.mp3")

# 查看生成的任务
for task in result['tasks']['tasks']:
    print(f"{task['id']}: {task['title']} ({task['assignee']})")
```

### 示例2: 批量处理

```python
import os
from meeting_assistant import MeetingAssistant

assistant = MeetingAssistant()

for file in os.listdir("audio/"):
    if file.endswith(".mp3"):
        print(f"处理: {file}")
        assistant.process_meeting(f"audio/{file}")
```

### 示例3: 自定义处理流程

```python
from meeting_assistant import (
    AudioTranscriber,
    MeetingSummarizer,
    TaskExtractor
)

# 只转录
transcriber = AudioTranscriber()
transcript = transcriber.transcribe("meeting.mp3")

# 只生成纪要
summarizer = MeetingSummarizer()
summary = summarizer.generate_summary(transcript['text_path'])

# 只提取任务
extractor = TaskExtractor()
tasks = extractor.extract_tasks(summary['summary_path'])
```

## 参考

- [OpenAI Whisper](https://github.com/openai/whisper)
- [GitHub Actions](https://docs.github.com/en/actions)

## 许可证

MIT

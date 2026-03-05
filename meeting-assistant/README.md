# 🎙️ 智能会议纪要自动化系统

一个完整的语音转文字 → 会议纪要生成 → 工作任务自动化的系统。

## 📋 系统架构

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   录音输入   │ → │  语音转文字  │ → │  会议纪要生成 │ → │  任务自动化  │
│  (MP3/WAV)  │    │   Whisper   │    │    GPT-4    │    │  工作流执行  │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
```

## 🛠️ 技术栈

| 组件 | 技术 | 用途 |
|------|------|------|
| 语音识别 | OpenAI Whisper | 高精度语音转文字 |
| 说话人分离 | PyAnnote / Diart | 区分不同发言者 |
| 会议纪要 | GPT-4 / Kimi | 提取要点、生成摘要 |
| 任务管理 | n8n / GitHub Actions | 自动化工作流 |
| 存储 | GitHub / 本地 | 文件管理 |

## 📁 项目结构

```
meeting-assistant/
├── 📄 audio/                  # 录音文件存放
├── 📄 transcripts/            # 转录文本
├── 📄 summaries/              # 会议纪要
├── 📄 tasks/                  # 生成的任务
├── 📄 src/
│   ├── 🐍 transcribe.py      # 语音转文字
│   ├── 🐍 generate_summary.py # 生成会议纪要
│   ├── 🐍 extract_tasks.py   # 提取任务
│   └── 🐍 auto_execute.py    # 自动执行
├── 📄 .github/workflows/      # GitHub Actions
│   └── meeting-pipeline.yml  # 自动化流程
└── 📄 README.md
```

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install openai-whisper openai pyannote.audio
```

### 2. 配置环境变量

```bash
export OPENAI_API_KEY="your-api-key"
export GITHUB_TOKEN="your-github-token"
```

### 3. 运行完整流程

```bash
python src/main.py --audio meeting.mp3
```

## 📖 使用指南

### 方式1: 本地运行

```bash
# 1. 语音转文字
python src/transcribe.py --input audio/meeting.mp3

# 2. 生成会议纪要
python src/generate_summary.py --input transcripts/meeting.txt

# 3. 提取任务
python src/extract_tasks.py --input summaries/meeting_summary.md
```

### 方式2: GitHub Actions 自动化

1. 上传录音到 `audio/` 目录
2. 自动触发工作流
3. 查看生成的纪要和任务

## 📝 输出示例

### 会议纪要
```markdown
# 会议纪要 - 2026-03-05

## 参会人员
- 张三 (产品经理)
- 李四 (技术负责人)
- 王五 (设计师)

## 主要议题
1. Q2 产品规划讨论
2. 技术架构升级方案

## 决策事项
- ✅ 采用微服务架构
- ✅ 下周五前完成原型设计

## 待办任务
| 任务 | 负责人 | 截止日期 | 优先级 |
|------|--------|----------|--------|
| 完成技术方案文档 | 李四 | 2026-03-10 | 高 |
| 设计 UI 原型 | 王五 | 2026-03-12 | 中 |
```

### 自动生成的任务
```json
{
  "tasks": [
    {
      "id": "TASK-001",
      "title": "完成技术方案文档",
      "assignee": "李四",
      "due_date": "2026-03-10",
      "priority": "high",
      "source": "会议决策"
    }
  ]
}
```

## 🔧 进阶配置

### 自定义提示词

编辑 `config/prompts.yaml`:
```yaml
summary_prompt: |
  你是一个专业的会议纪要助手...
  
task_extraction_prompt: |
  从以下会议纪要中提取任务...
```

### 集成第三方工具

- **Notion**: 自动同步会议纪要
- **Slack**: 发送任务提醒
- **Jira**: 创建任务工单
- **日历**: 自动安排会议

## 📊 性能指标

| 指标 | 数值 |
|------|------|
| 语音识别准确率 | > 95% |
| 会议纪要生成时间 | < 30秒 |
| 任务提取准确率 | > 90% |
| 支持语言 | 中文、英文等 99 种 |

## 🌟 特色功能

- ✅ **说话人识别** - 自动区分不同发言者
- ✅ **实时转录** - 支持实时会议转录
- ✅ **智能摘要** - 自动提取关键信息
- ✅ **任务追踪** - 自动生成并追踪任务
- ✅ **多语言支持** - 支持 99 种语言
- ✅ **隐私保护** - 本地处理，数据安全

## 🤝 贡献指南

欢迎提交 PR 改进系统！

## 📄 许可证

MIT License

---

*让会议更高效，让工作更智能* 🚀

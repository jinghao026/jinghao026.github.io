---
name: xiaohongshu-content-creator
description: 小红书内容创作助手 - 从想法到发布的一站式工作流。生成幽默教育故事 → AI漫画 → 小红书文案 → 自动发布。
metadata:
  openclaw:
    requires:
      env: ["XHS_COOKIE"]
---

# 小红书内容创作助手

从想法到发布的完整自动化工作流。

## 工作流程

```
想法输入 → 生成故事 → AI漫画 → 小红书文案 → 自动发布
```

## 功能

- ✍️ **故事生成** - 基于想法创作幽默教育故事
- 🎨 **AI漫画** - 生成搞笑漫画分镜
- 📝 **文案生成** - 小红书风格标题和正文
- 📤 **自动发布** - 直接发布到小红书

## 使用方法

### 快速开始

```python
from xiaohongshu_creator import ContentCreator

creator = ContentCreator()

# 一键生成并发布
result = creator.create_and_publish(
    idea="程序员和产品经理的日常",
    story_length="medium",  # short/medium/long
    comic_panels=4,         # 漫画格数
    auto_publish=True       # 自动发布
)

print(f"故事: {result['story_path']}")
print(f"漫画: {result['comic_paths']}")
print(f"文案: {result['copy_path']}")
print(f"发布: {result['publish_url']}")
```

### 分步使用

```python
# 1. 生成故事
story = creator.generate_story(
    idea="程序员和产品经理的日常",
    tone="humorous",
    educational_theme="沟通的重要性"
)

# 2. 生成漫画
comics = creator.generate_comic(story, panels=4)

# 3. 生成文案
copy = creator.generate_copy(story, comics)

# 4. 发布
result = creator.publish_to_xiaohongshu(copy, comics)
```

### 命令行使用

```bash
# 完整流程
xiaohongshu-creator --idea "程序员和产品经理的日常" --publish

# 只生成故事和漫画
xiaohongshu-creator --idea "想法" --skip-publish

# 使用已有故事
xiaohongshu-creator --story story.md --publish
```

## 配置

创建 `creator-config.yaml`:

```yaml
story:
  default_length: medium  # short/medium/long
  tone: humorous
  educational: true

comic:
  style: "cartoon"  # cartoon/anime/realistic
  panels: 4
  size: "1024x1024"

copy:
  style: "casual"  # casual/professional/trendy
  emoji: true
  hashtags: ["#程序员", "#职场", "#搞笑"]

publish:
  auto_publish: false  # 需要手动确认
  schedule: null  # 定时发布
```

## 示例输出

### 生成的故事

```
《产品经理的"简单"需求》

程序员小明正在专心写代码，产品经理小红走过来...

小红："小明，这个按钮能不能改一下？"
小明："可以，怎么改？"
小红："很简单，就改一点点..."

（2小时后）

小红："对了，还要支持夜间模式、多语言、
      手势操作、语音控制..."

小明："这叫'一点点'？！"

【教育意义】
沟通时要明确需求范围，避免理解偏差。
```

### 生成的漫画

4格漫画：
1. 程序员认真coding
2. 产品经理过来说"简单需求"
3. 需求越加越多
4. 程序员崩溃表情

### 生成的小红书文案

```
标题：产品经理说"就改一点点"...😭

正文：
程序员们懂的都懂！
当产品经理说"很简单"的时候...
我就知道今晚要加班了😂

💡 职场小贴士：
沟通需求时一定要确认范围，
不然后续加需求真的顶不住！

#程序员 #产品经理 #职场搞笑 #加班日常
#程序员日常 #打工人 #内容过于真实

👇 你们遇到过这种情况吗？
```

## 依赖

```bash
pip install openai requests pillow
```

## 环境变量

| 变量 | 必需 | 说明 |
|------|------|------|
| `OPENAI_API_KEY` | 是 | OpenAI API 密钥 |
| `XHS_COOKIE` | 是 | 小红书登录 Cookie |
| `SILICONFLOW_API_KEY` | 否 | 可选，用于文生图 |

## 参考

- [小红书 MCP](https://github.com/xpzouying/xiaohongshu-mcp)
- [OpenAI DALL-E](https://platform.openai.com/docs/guides/images)

## 许可证

MIT

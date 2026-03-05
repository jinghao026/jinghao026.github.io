#!/bin/bash
# memory_init.sh - 每日记忆文件自动创建脚本
# 基于 OpenClaw 记忆系统教程

WORKSPACE="${OPENCLAW_WORKSPACE:-$HOME/.openclaw/workspace}"
MEMORY_DIR="$WORKSPACE/memory"
TODAY=$(date +%Y-%m-%d)
MEMORY_FILE="$MEMORY_DIR/$TODAY.md"

# 创建目录（如果不存在）
mkdir -p "$MEMORY_DIR"
mkdir -p "$MEMORY_DIR/archives"
mkdir -p "$MEMORY_DIR/meditation"

# 检查文件是否已存在
if [ -f "$MEMORY_FILE" ]; then
    echo "✅ 记忆文件已存在: $MEMORY_FILE"
    exit 0
fi

# 获取星期几
WEEKDAY=$(date +%u)
WEEKDAY_NAME=$(date +%A)

# 创建记忆文件
cat > "$MEMORY_FILE" << EOF
# $TODAY 交互记忆

> 日期：$(date +%Y年%m月%d日)（$WEEKDAY_NAME）
> 状态：正常记录

## 凌晨 00:00 - 午夜冥想
- 完成每日冥想
- 系统运行平稳

## 日间交互
- （待记录）

## 今日洞察
> （待补充 - 重要发现、教训、模式识别）

## 待办事项
- [ ] （待补充）

## 关键提炼（可选）
> 如有重要经验教训，更新到 MEMORY.md

---
*生成时间：$(date +%H:%M:%S)*
*记忆系统：Text > Brain*
EOF

echo "✅ 已创建记忆文件: $MEMORY_FILE"
echo "💡 提示：记得在一天结束时更新今日洞察和待办事项"

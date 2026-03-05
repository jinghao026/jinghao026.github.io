#!/bin/bash
# config_backup.sh - 核心配置文件自动备份脚本
# 基于 OpenClaw 记忆系统教程

WORKSPACE="${OPENCLAW_WORKSPACE:-$HOME/.openclaw/workspace}"
BACKUP_DIR="$WORKSPACE/backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
DATE=$(date +%Y%m%d)

# 核心配置文件列表
CORE_FILES=(
    "SOUL.md"
    "AGENTS.md"
    "IDENTITY.md"
    "USER.md"
    "MEMORY.md"
    "HEARTBEAT.md"
    "TOOLS.md"
)

# 可选配置文件
OPTIONAL_FILES=(
    "BOOTSTRAP.md"
    "config/group_management.json"
    "config/allowlist.json"
    "config/blacklist.json"
)

echo "🔒 开始配置备份..."
echo "工作目录: $WORKSPACE"

# 检查工作目录
if [ ! -d "$WORKSPACE" ]; then
    echo "❌ 错误: 工作目录不存在: $WORKSPACE"
    exit 1
fi

cd "$WORKSPACE" || exit 1

# 检查Git仓库
if [ ! -d ".git" ]; then
    echo "⚠️ 警告: 当前目录不是Git仓库，跳过Git备份"
    USE_GIT=false
else
    USE_GIT=true
fi

# 文件完整性检查
echo ""
echo "📋 检查核心文件..."
MISSING_FILES=()
for file in "${CORE_FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "  ✅ $file"
    else
        echo "  ❌ $file (缺失)"
        MISSING_FILES+=("$file")
    fi
done

# 检查可选文件
echo ""
echo "📋 检查可选文件..."
for file in "${OPTIONAL_FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "  ✅ $file"
        CORE_FILES+=("$file")
    else
        echo "  ⚠️  $file (不存在，跳过)"
    fi
done

# Git备份
if [ "$USE_GIT" = true ]; then
    echo ""
    echo "📝 Git备份..."
    
    # 添加文件
    git add "${CORE_FILES[@]}" 2>/dev/null
    
    # 检查是否有变更
    if git diff --cached --quiet; then
        echo "  ℹ️  没有变更需要提交"
    else
        # 提交
        git commit -m "config: 自动备份 $DATE" -m "备份时间: $TIMESTAMP" -m "备份脚本: config_backup.sh"
        echo "  ✅ 已提交: config: 自动备份 $DATE"
        
        # 创建标签
        git tag -a "config-$DATE" -m "配置自动备份 $DATE" 2>/dev/null || echo "  ⚠️  标签可能已存在"
        echo "  ✅ 已创建标签: config-$DATE"
    fi
fi

# 文件备份
mkdir -p "$BACKUP_DIR"
BACKUP_FILE="$BACKUP_DIR/config_backup_$TIMESTAMP.tar.gz"

echo ""
echo "📦 创建压缩备份..."
tar -czf "$BACKUP_FILE" "${CORE_FILES[@]}" 2>/dev/null

if [ -f "$BACKUP_FILE" ]; then
    echo "  ✅ 备份文件: $BACKUP_FILE"
    ls -lh "$BACKUP_FILE" | awk '{print "     大小:", $5}'
else
    echo "  ❌ 备份失败"
fi

# 总结
echo ""
echo "🎉 备份完成！"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if [ ${#MISSING_FILES[@]} -gt 0 ]; then
    echo "⚠️  缺失文件: ${#MISSING_FILES[@]} 个"
    for file in "${MISSING_FILES[@]}"; do
        echo "   - $file"
    done
else
    echo "✅ 所有核心文件正常"
fi

if [ "$USE_GIT" = true ]; then
    echo "✅ Git备份完成"
fi

echo "✅ 压缩备份: $BACKUP_FILE"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

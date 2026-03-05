# 🔧 精选 GitHub 工作流合集

收集 GitHub 上 Star 数量高、实用性强的自动化工作流，提升工作效率。

---

## 📊 数据统计

| 类别 | 项目数 | 总 Stars |
|------|--------|----------|
| CI/CD 自动化 | 15+ | 500K+ |
| 开发工具 | 20+ | 300K+ |
| 业务自动化 | 10+ | 200K+ |

---

## 🚀 顶级工作流项目

### 1. GitHub Actions 官方生态

| 项目 | Stars | 用途 |
|------|-------|------|
| [actions/starter-workflows](https://github.com/actions/starter-workflows) | 11,321 | 官方工作流模板 |
| [actions/setup-node](https://github.com/actions/setup-node) | 4,678 | Node.js 环境设置 |
| [actions/setup-python](https://github.com/actions/setup-python) | 3,200+ | Python 环境设置 |
| [actions/checkout](https://github.com/actions/checkout) | 2,800+ | 代码检出 |

### 2. 部署与发布

| 项目 | Stars | 用途 |
|------|-------|------|
| [JamesIves/github-pages-deploy-action](https://github.com/JamesIves/github-pages-deploy-action) | 4,553 | 自动部署到 GitHub Pages |
| [peter-evans/create-pull-request](https://github.com/peter-evans/create-pull-request) | 2,708 | 自动创建 PR |
| [softprops/action-gh-release](https://github.com/softprops/action-gh-release) | 2,100+ | 自动发布 Release |

### 3. 代码质量与检查

| 项目 | Stars | 用途 |
|------|-------|------|
| [rhysd/actionlint](https://github.com/rhysd/actionlint) | 3,646 | Workflow 文件静态检查 |
| [github/super-linter](https://github.com/github/super-linter) | 9,800+ | 多语言代码检查 |
| [codecov/codecov-action](https://github.com/codecov/codecov-action) | 1,500+ | 代码覆盖率报告 |

### 4. 通知与集成

| 项目 | Stars | 用途 |
|------|-------|------|
| [8398a7/action-slack](https://github.com/8398a7/action-slack) | 1,200+ | Slack 通知 |
| [rtCamp/action-slack-notify](https://github.com/rtCamp/action-slack-notify) | 900+ | Slack 消息通知 |

---

## 🔄 业务自动化平台

### n8n - 可视化工作流 (⭐ 177,631)

**GitHub**: https://github.com/n8n-io/n8n

**特点**:
- 400+ 集成（GitHub, Slack, Google Sheets, 数据库等）
- 可视化编辑器，拖拽式构建
- 支持自托管
- AI 能力集成

**适用场景**:
- 数据同步
- 定时任务
- 业务流程自动化
- 跨平台集成

---

## 📋 实用工作流模板

### 1. 自动部署网站

```yaml
name: Deploy to GitHub Pages

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          
      - name: Install dependencies
        run: npm ci
        
      - name: Build
        run: npm run build
        
      - name: Deploy
        uses: JamesIves/github-pages-deploy-action@v4
        with:
          folder: dist
```

### 2. 自动更新 README 统计

```yaml
name: Update README Stats

on:
  schedule:
    - cron: '0 0 * * *'  # 每天运行
  workflow_dispatch:

jobs:
  update-readme:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Update GitHub Stats
        uses: anmol098/waka-readme-stats@master
        with:
          WAKATIME_API_KEY: ${{ secrets.WAKATIME_API_KEY }}
          GH_TOKEN: ${{ secrets.GH_TOKEN }}
```

### 3. 代码质量检查

```yaml
name: Code Quality Check

on: [push, pull_request]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Run Super Linter
        uses: github/super-linter@v5
        env:
          DEFAULT_BRANCH: main
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

---

## 📚 学习资源

### Awesome 列表

- [sdras/awesome-actions](https://github.com/sdras/awesome-actions) - 27K+ Stars，精选 Actions 集合
- [opsre/awesome-ops](https://github.com/opsre/awesome-ops) - 运维相关优秀项目

### 官方文档

- [GitHub Actions 文档](https://docs.github.com/en/actions)
- [Workflow 语法参考](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions)

---

## 💡 工作流应用场景

| 场景 | 推荐工具 |
|------|----------|
| 自动部署 | github-pages-deploy-action |
| 代码检查 | super-linter, actionlint |
| 通知提醒 | action-slack |
| 版本发布 | action-gh-release |
| 数据统计 | waka-readme-stats |
| 业务自动化 | n8n |

---

## 📝 贡献指南

欢迎提交 PR 补充更多实用工作流！

1. Fork 本仓库
2. 添加新的工作流项目
3. 提交 PR

---

*最后更新: 2026-03-05*

<!-- superpowers-zh:begin (do not edit between these markers) -->
# Superpowers-ZH 中文增强版

本项目已安装 superpowers-zh 技能框架（20 个 skills）。

## 核心规则

1. **收到任务时，先检查是否有匹配的 skill** — 哪怕只有 1% 的可能性也要检查
2. **设计先于编码** — 收到功能需求时，先用 brainstorming skill 做需求分析
3. **测试先于实现** — 写代码前先写测试（TDD）
4. **验证先于完成** — 声称完成前必须运行验证命令

## 可用 Skills

Skills 位于 `.claude/skills/` 目录，每个 skill 有独立的 `SKILL.md` 文件。

- **brainstorming**: 在任何创造性工作之前必须使用此技能——创建功能、构建组件、添加功能或修改行为。在实现之前先探索用户意图、需求和设计。
- **chinese-code-review**: 中文 review 沟通参考——话术模板、分级标注（必须修复/建议修改/仅供参考）、国内团队常见反模式应对。仅在用户显式 /chinese-code-review 时调用，不要根据上下文自动触发。
- **chinese-commit-conventions**: 中文 commit 与 changelog 配置参考——Conventional Commits 中文适配、commitlint/husky/commitizen 中文模板、conventional-changelog 中文配置。仅在用户显式 /chinese-commit-conventions 时调用，不要根据上下文自动触发。
- **chinese-documentation**: 中文文档排版参考——中英文空格、全半角标点、术语保留、链接格式、中文文案排版指北约定。仅在用户显式 /chinese-documentation 时调用，不要根据上下文自动触发。
- **chinese-git-workflow**: 国内 Git 平台配置参考——Gitee、Coding.net、极狐 GitLab、CNB 的 SSH/HTTPS/凭据/CI 接入差异与镜像同步配置。仅在用户显式 /chinese-git-workflow 时调用，不要根据上下文自动触发。
- **dispatching-parallel-agents**: 当面对 2 个以上可以独立进行、无共享状态或顺序依赖的任务时使用
- **executing-plans**: 当你有一份书面实现计划需要在单独的会话中执行，并设有审查检查点时使用
- **finishing-a-development-branch**: 当实现完成、所有测试通过、需要决定如何集成这份工作时使用
- **mcp-builder**: MCP 服务器构建方法论 — 系统化构建生产级 MCP 工具，让 AI 助手连接外部能力
- **receiving-code-review**: 收到代码审查反馈后、实施建议之前使用，尤其当反馈不明确或技术上有疑问时——需要技术严谨性和验证，而非敷衍附和或盲目执行
- **requesting-code-review**: 完成任务、实现重要功能或合并前使用，用于验证工作成果是否符合要求
- **subagent-driven-development**: 当在当前会话中执行包含独立任务的实现计划时使用
- **systematic-debugging**: 遇到任何 bug、测试失败或异常行为时使用，在提出修复方案之前执行
- **test-driven-development**: 在实现任何功能或修复 bug 时使用，在编写实现代码之前
- **using-git-worktrees**: 当需要开始与当前工作区隔离的功能开发，或在执行实现计划之前使用——通过原生工具或 git worktree 回退机制确保隔离工作区存在
- **using-superpowers**: 在开始任何对话时使用——确立如何查找和使用技能，要求在任何响应（包括澄清性问题）之前调用 Skill 工具
- **verification-before-completion**: 在宣称工作完成、已修复或测试通过之前使用，在提交或创建 PR 之前——必须运行验证命令并确认输出后才能声称成功；始终用证据支撑断言
- **workflow-runner**: 在 Claude Code / OpenClaw / Cursor 中直接运行 agency-orchestrator YAML 工作流——无需 API key，使用当前会话的 LLM 作为执行引擎。当用户提供 .yaml 工作流文件或要求多角色协作完成任务时触发。
- **writing-plans**: 当你有规格说明或需求用于多步骤任务时使用，在动手写代码之前
- **writing-skills**: 当创建新技能、编辑现有技能或在部署前验证技能是否有效时使用

## 如何使用

当任务匹配某个 skill 时，使用 `Skill` 工具加载对应 skill 并严格遵循其流程。绝不要用 Read 工具读取 SKILL.md 文件。

如果你认为哪怕只有 1% 的可能性某个 skill 适用于你正在做的事情，你必须调用该 skill 检查。
<!-- superpowers-zh:end -->

---

## 当前目录自定义技能

- `skills/requirement-analysis/SKILL.md`：对新 PRD、飞书/Meegle 需求、本地需求文档和交互原型执行萃取、确认、澄清、评审，并按需生成测试用例。
- `skills/business-logic-query/SKILL.md`：针对已有业务规则、代码逻辑、状态流转和页面交互进行飞书知识库只读查询；普通业务询问不启动完整需求分析。
- `skills/api-coverage-review/SKILL.md`：对比需求文档、技术/API 文档和测试用例，生成双向追溯矩阵并判断接口设计覆盖与运行态验证状态。

三个技能按任务目的分工：新需求的系统性分析使用 `requirement-analysis`，聚焦既有规则的单点询问使用 `business-logic-query`，跨需求、技术方案和测试用例的一致性与接口覆盖评审使用 `api-coverage-review`。

---

# 工作区概览

本 monorepo 是 **Neptune Robotics 测试基础设施**，包含三个独立子项目。

## 子项目

| 项目 | 路径 | 用途 | 技术栈 |
|------|------|------|--------|
| **ui-autotest** | `../ui-autotest/` | Web 端 UI 自动化测试 | Python 3.12 + Playwright + Pytest + Excel 关键字驱动 |
| **PrdToTestCaseProject** | `../PrdToTestCaseProject/` | 从 PRD/需求生成测试用例 | Python 3.8+ + Node.js + lark-cli + meegle |
| **mobileframework** | `../mobileframework/mobileframework/` | 移动端 UI 自动化框架（参考） | Python + Appium + Selenium + Pytest + Allure |

---

## ui-autotest — Web UI 自动化测试

### 架构分层

```
Excel 用例 (testcases/*.xlsx)
    → run.py（主入口，通过 work_id 定位 Excel 文件）
    → KeywordEngine（自然语言步骤 → Page Object 调用）
    → pages/web/（POM：元素定位 + 原子操作）
    → actions/web/（业务场景组合：login_flow 等）
    → Playwright Chromium
    → 截图 + JSON/HTML/Allure 多格式报告
```

### 常用命令

```bash
cd "d:/git test/ui-autotest"

# 按 work_id 执行 Excel 用例
python run.py 7006322574

# 指定角色
python run.py 7006322574 --role=AM

# 无头模式
python run.py 7006322574 --headless

# Pytest 冒烟测试
pytest testcases/ -m smoke

# 安装依赖
pip install playwright openpyxl
playwright install chromium
```

### 关键文件

- [run.py](../ui-autotest/run.py) — 主入口：加载 Excel → 提取用例 → 关键字引擎执行 → 报告
- [common/keyword_engine.py](../ui-autotest/common/keyword_engine.py) — 关键字引擎：解析自然语言步骤，匹配 Page Object 调用
- [common/test_executor.py](../ui-autotest/common/test_executor.py) — 浏览器生命周期管理、登录状态保持、角色切换
- [common/excel_reader.py](../ui-autotest/common/excel_reader.py) — Excel 用例解析
- [config/accounts.json](../ui-autotest/config/accounts.json) — 多角色账号凭证（不入库）
- [setting.py](../ui-autotest/setting.py) — 路径常量与目标 URL
- [conftest.py](../ui-autotest/conftest.py) — Pytest fixtures: `accounts`, `browser`, `page`
- [actions/web/login_flow.py](../ui-autotest/actions/web/login_flow.py) — 角色登录流程实现

### 关键字驱动设计

非技术 QA 用自然语言在 Excel 中编写步骤，KeywordEngine 自动识别并执行：

| 步骤示例 | 引擎行为 |
|---------|---------|
| `访问 http://...` | page.goto(url) |
| `使用AM账号登录` | 从 accounts.json 按角色取凭证，调用 login_flow |
| `点击【检测报告】` | 多选择器兜底查找 + scroll + click |
| `验证页面显示螺旋桨` | page.innerText 包含检查 |

详细命令见 [ui-autotest/CLAUDE.md](../ui-autotest/CLAUDE.md)。

### CI/CD

`.github/workflows/pr-test.yml`：PR 修改 `pages/`、`core/`、`config/`、`testcases_excel/` 时，self-hosted runner 上执行 P0 冒烟测试。报告上传为 artifact，失败时截图一并上传。

---

## PrdToTestCaseProject — 需求 → 测试用例生成

### 核心流程

```
需求来源（飞书文档 / Meegle 工作项 / Figma）
    → tools/sync_product_docs.py（增量同步背景资料）
    → 读取正文 + 评论 + 图片 + 白板 + Figma
    → 用户确认识别结果
    → 按 8 类设计用例 → case-data/*.json
    → 生成器 → test-cases/<项目>/<项目>_[timestamp].xmind 或 .xlsx
```

### 不可跳过的关键规则

1. **每次执行前**运行 `tools/sync_product_docs.py` 增量同步代码逻辑 + 页面交互逻辑知识库
2. **未指定格式时先询问** XMind 还是 Excel，不同时生成两种
3. **图片/白板/Figma 识别结果**必须经用户确认后写入正式用例
4. **不覆盖历史产物** — 变化后生成带时间戳的新文件
5. **P0 仅限基础功能正向冒烟**；一条用例只覆盖一种独立场景
6. **规则优先级**：`用户本轮确认 > Meegle 最新评论 > 需求正文 > 背景资料 > 旧文档`

### 环境

- `.venv`（Python venv，位于项目根目录）
- `lark-cli`（飞书文档读写，每次必用）
- `meegle`（仅读取 Meegle 工作项时需要）
- Figma MCP（可选，仅含 Figma 设计稿时）

完整规范见 `skills/prd-to-test-cases/SKILL.md` 和 [PrdToTestCaseProject/CLAUDE.md](../PrdToTestCaseProject/CLAUDE.md)。

---

## mobileframework — 移动端 UI 自动化（参考框架）

Python + Appium + Selenium + Pytest，与 ui-autotest 同分层架构（pagefiles/pages/actions/testcases），支持 Android/iOS 双平台、多设备并发、Allure 报告。原始目标为豆瓣 App，现为参考模板。

```bash
cd "d:/git test/mobileframework/mobileframework"
python run.py
```

框架结构详见 [FRAMEWORK_STRUCTURE.md](../mobileframework/mobileframework/FRAMEWORK_STRUCTURE.md)。

---

## 跨项目约定

- **所有 Python 测试框架遵循相同分层**：配置层 → 元素定位层 → 页面对象层 → 业务动作层 → 测试用例层
- **中文优先**：用户中文交流，commit message 遵循中文规范
- **项目级 CLAUDE.md**：每个子项目有独立 CLAUDE.md，具体操作以子项目文件为准

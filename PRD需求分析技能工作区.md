# Neptune PRD 需求分析与测试技能工作区

本目录提供三个职责清晰的 Codex/Agent Skill，用于需求分析、既有业务逻辑查询和需求—技术—用例一致性评审：

| 技能 | 用途 | 典型请求 |
|------|------|----------|
| `requirement-analysis` | 分析新 PRD、飞书/Meegle 需求、本地文档或交互原型，并完成萃取、澄清和评审 | “分析这个需求”“评审这份 PRD”“生成测试用例” |
| `business-logic-query` | 查询已上线或既有系统的代码逻辑、状态规则和页面交互逻辑 | “这个状态如何流转”“按钮什么时候显示”“字段如何计算” |
| `api-coverage-review` | 对比需求、技术/API 文档和测试用例，判断接口设计与场景覆盖 | “技术方案满足需求和用例吗”“做接口覆盖评审” |

## 技能选择

- 用户提供新 PRD、需求链接或原型作为分析对象时，使用 `requirement-analysis`。
- 用户询问公司已有或已上线功能的具体规则时，使用 `business-logic-query`。
- 用户要求比较需求、技术/API 文档和测试用例，或判断接口方案是否覆盖场景时，使用 `api-coverage-review`。
- 即使问题只涉及一个字段，只要证据来自本轮提供的新 PRD，仍使用 `requirement-analysis`。
- 业务逻辑查询不会自动启动完整需求分析，也不会生成测试用例。

## 快速使用

### 完整需求分析

```text
使用 $requirement-analysis 分析这个需求：<需求链接或文件路径>
```

工作流：

```text
START
  → PARSE（本地文档按需）
  → EXTRACT（需求萃取）
  → 用户确认门
  → CLARIFY（澄清清单）
  → REVIEW（需求评审）
  → AGGREGATE（综合报告）
  → TEST_CASES（用户明确要求时）
```

需求萃取完成后必须等待用户确认。用户回复“继续”或确认萃取结果后，才能进入澄清和评审阶段。

### 业务逻辑询问

```text
使用 $business-logic-query 查询：任务状态在什么条件下会变为已完成？
```

回答默认包含：

- 直接结论
- 条件、处理和结果
- 边界与例外
- 未明确或冲突的待确认项
- 飞书来源链接、章节及修订信息（如可获取）

### 需求—技术—用例一致性评审

```text
使用 $api-coverage-review 对比以下材料并判断接口设计是否满足：
- 需求文档：<链接或文件路径>
- 技术/API 文档：<链接或文件路径>
- 测试用例：<链接或文件路径>
```

评审会生成需求—接口—用例双向追溯矩阵，并分别给出：

- 设计覆盖结论：满足、部分满足、不满足、无法判断、无需求依据或技术超范围；
- 运行态结论：已验证、未验证或验证失败。

只有技术文档时不会断言代码已经实现；只有读取代码、真实接口响应、日志或已执行测试结果后，才会标记运行态“已验证”。默认产物目录为：

```text
artifacts/<YYYYMMDD-HHmm>-<项目slug>-api-coverage/
```

## 支持的需求来源

`requirement-analysis` 支持：

- 飞书 Wiki、Docs
- Meegle 工作项
- Markdown、文本、DOCX、PDF
- HTML/Web 交互原型
- 文档与原型组合输入
- 已有分析报告、测试点或历史测试用例的增量分析

无法访问来源时，技能会明确记录证据缺口，不会假装已经读取内容。

## 飞书授权

需要访问飞书材料的技能统一使用飞书官方 `lark-cli` 用户授权，不使用自建 OAuth 应用。

检查授权：

```powershell
lark-cli auth status
```

重新登录：

```powershell
lark-cli auth login
```

如果系统 PATH 中没有 `lark-cli`，当前工作区提供的备用程序为：

```text
.tools/lark-cli/node_modules/@larksuite/cli/bin/lark-cli.exe
```

登录时直接扫描 CLI 生成的二维码。不要自行配置重定向 URL，也不要在日志或报告中保存访问令牌、Cookie、应用密钥。

## 需求分析产物

默认输出目录：

```text
artifacts/<YYYYMMDD-HHmm>-<项目slug>/
```

汇总并校验通过后，技能会额外发布一份便于查找的副本：

```text
需求分析/<项目名称>-需求分析.md
```

`artifacts` 中的 `final-report.md` 是带时间戳的历史源文件，始终保留；`需求分析` 中的同名文件是最新便捷副本，重复分析同一项目时允许更新覆盖。用户明确指定其他目录或文件名时，以用户要求为准。

| 文件 | 内容 |
|------|------|
| `_parsed-content.md` | 本地文档结构化解析结果；纯链接任务可不生成 |
| `_extraction.md` | 需求萃取、业务/用户/功能/非功能需求及逻辑评价 |
| `_clarifications.md` | 红、黄、绿三级澄清清单 |
| `_review.md` | 流程断点、风险、隐性需求、回归范围和评审发言稿 |
| `final-report.md` | 汇总后的最终需求分析报告 |
| `screenshots/` | 原型探索截图；纯文档任务可为空 |

发布命令：

```powershell
node "skills/requirement-analysis/scripts/publish-report.mjs" `
  "<RUN_DIR>" `
  "<项目名称>" `
  "<项目根目录>"
```

用户明确要求测试用例时，还可以生成：

```text
cases.json
cases.xlsx
```

测试用例不会在普通需求分析中自动生成。技能会先提供测试点或覆盖矩阵，确认后再生成完整用例。

## 目录结构

```text
skills/
├─ requirement-analysis/
│  ├─ SKILL.md
│  ├─ agents/openai.yaml
│  ├─ assets/
│  │  └─ default_template.json
│  ├─ references/
│  │  ├─ stages/          # 解析、萃取、澄清、评审阶段规范
│  │  ├─ knowledge/       # 异常、边界、状态机、反模式、量化基准
│  │  ├─ feishu-cli.md
│  │  ├─ meegle-access.md
│  │  └─ test-case-design.md
│  ├─ scripts/            # 产物校验、原型探索、Excel 生成
│  └─ tests/              # 基线样例与测试场景
├─ business-logic-query/
│  ├─ SKILL.md
│  ├─ agents/openai.yaml
│  └─ references/
│     ├─ sources.md       # 代码逻辑和页面交互知识库入口
│     └─ query-guide.md   # 授权、检索和 Wiki 子节点遍历
└─ api-coverage-review/
   ├─ SKILL.md
   ├─ agents/openai.yaml
   ├─ references/         # 比较模型、接口检查表和材料读取规范
   └─ scripts/
      └─ validate-review.mjs
```

工作区中的 `test data`、`test prd`、`testcase`、`需求分析` 和 `artifacts` 为业务资料或历史产物目录，不属于技能运行依赖。

## 生成 Excel 测试用例

安装依赖：

```powershell
python -m pip install -r "skills/requirement-analysis/scripts/requirements.txt"
```

生成 Excel：

```powershell
python "skills/requirement-analysis/scripts/generate_excel.py" `
  --input "cases.json" `
  --output "cases.xlsx" `
  --columns "skills/requirement-analysis/assets/default_template.json"
```

JSON 字段应与 `default_template.json` 一致，主要包括用例名称、所属目录、执行步骤、用例类型、预期结果、前置条件、关联需求、优先级和负责人。

## 产物校验

Node 版校验器是跨平台首选：

```powershell
node "skills/requirement-analysis/scripts/validate-artifacts.mjs" "<RUN_DIR>" --stage all
```

支持的阶段：

```text
parse | extract | clarify | review | aggregate | all
```

Windows PowerShell 备用校验：

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass `
  -File "skills/requirement-analysis/scripts/validate-artifacts.ps1" `
  -RunDir "<RUN_DIR>" `
  -Stage all
```

运行内置基线测试：

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass `
  -File "skills/requirement-analysis/tests/run-baseline.ps1" `
  -Stage all
```

## 关键质量规则

- 事实、测试推导和经验建议必须明确区分。
- 所有结论应能追溯到文件、文档章节、页面位置或截图。
- 主流程必须检查异常、取消、返回、重复提交、权限、空态、加载态和并发影响。
- “及时”“大量”“自动”等模糊描述必须转成可量化的澄清问题。
- 未确认规则不能被写成唯一确定的测试预期。
- 技能只读访问飞书和 Meegle，除非用户另行明确授权修改云端内容。

## 入口文件

- [完整需求分析技能](skills/requirement-analysis/SKILL.md)
- [业务逻辑询问技能](skills/business-logic-query/SKILL.md)
- [需求—技术—用例一致性评审技能](skills/api-coverage-review/SKILL.md)
- [飞书 CLI 使用说明](skills/requirement-analysis/references/feishu-cli.md)
- [Meegle 访问说明](skills/requirement-analysis/references/meegle-access.md)
- [测试用例设计规范](skills/requirement-analysis/references/test-case-design.md)

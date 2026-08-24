---
name: requirement-analysis
description: Analyze a new PRD, Feishu/Meegle requirement link, local requirement document, or interactive prototype from a QA perspective; extract requirements, identify gaps, prepare clarification questions, perform review, and optionally design test cases. Use for requests such as 需求分析、需求萃取、需求澄清、需求评审、分析原型、看需求、生成测试点或测试用例. Do not use for a focused question about an existing business rule or page interaction; use business-logic-query instead.
---

# 需求分析

把输入资料转成可追溯、可澄清、可评审、可测试的需求分析。保持事实、推导和建议三者分离，不把经验判断写成已确认需求。

执行命令前，把本技能所在目录的绝对路径记为 `SKILL_DIR`；不要假设技能安装在固定用户目录。

## 工作流

按以下状态机执行：

`START → PARSE（按需）→ EXTRACT → 用户确认门 → CLARIFY → REVIEW → AGGREGATE → TEST_CASES（按需）`

1. START
   - 识别输入：本地文档、飞书/Meegle 链接、网页原型或其组合。
   - 将用户当前工作/项目目录记为 `PROJECT_ROOT`，从 Meegle 工作项名称、文档标题或用户提供的项目名确定 `PROJECT_NAME`。
   - 在 `PROJECT_ROOT` 创建 `artifacts/<YYYYMMDD-HHmm>-<项目slug>/`；用户指定其他目录或文件名时服从用户要求。
   - 记录来源 URL、文件路径、抓取时间、访问限制和既有测试资产。
2. PARSE
   - 仅本地文档需要单独解析，读取 [文档解析阶段](references/stages/doc-reader-agent.md)，输出 `_parsed-content.md`。
   - 纯链接可跳过，但在后续产物中明确写明跳过原因。
3. EXTRACT
   - 读取 [需求萃取阶段](references/stages/extractor-agent.md) 以及 `references/knowledge/` 下五份检查库。
   - 飞书资料按 [飞书 CLI 访问](references/feishu-cli.md) 获取；Meegle 按 [Meegle 只读访问](references/meegle-access.md) 获取；交互原型优先使用可用浏览器能力，无法浏览时明确局限。
   - 输出 `_extraction.md`，覆盖页面/模块、字段与规则、角色权限、状态流转、异常与边界、依赖、可测试验收点。
   - 执行阶段校验：`node "$SKILL_DIR/scripts/validate-artifacts.mjs" <RUN_DIR> --stage extract`。
4. 用户确认门
   - 向用户展示萃取摘要、覆盖范围、证据缺口和未探索项。
   - 必须等待用户确认“继续”或提出修改；未确认不得进入 CLARIFY。
5. CLARIFY
   - 读取 [需求澄清阶段](references/stages/clarifier-agent.md)，输出 `_clarifications.md`。
   - 问题按红/黄/绿优先级分组，并覆盖异常分支、边界值、状态机细节、隐性依赖；每条必须包含来源、影响范围和可直接发送的完整问句。
   - 每个澄清点必须独立编号；不得把多个可分别回答的问题压缩成“规则待明确”“异常待补充”等摘要。
   - 执行 `--stage clarify` 校验。
6. REVIEW
   - 读取 [需求评审阶段](references/stages/reviewer-agent.md)，输出 `_review.md`。
   - 给出结论、产品问题、开发问题、风险、回归范围、可量化验收标准和会议发言稿。
   - 执行 `--stage review` 校验。
7. AGGREGATE
   - 生成 `final-report.md`，至少包含项目概览、需求萃取、分析评价、澄清结论、评审意见和来源追溯。
   - “澄清结论”必须完整内嵌 `_clarifications.md` 中的全部具体澄清项，逐条列出编号、来源/场景、需要确认的完整问题和影响；可增加分类统计，但统计、主题摘要或“详见 `_clarifications.md`”不能替代明细。
   - 最终报告中的澄清项数量、编号和优先级必须与 `_clarifications.md` 一致；即使报告会单独发布，也必须能脱离中间产物直接用于澄清会议。
   - 执行 `--stage aggregate` 或 `--stage all`；若 PARSE 合理跳过，校验器不会强制要求 `_parsed-content.md`。
   - 校验通过后，把最终报告发布到易查找目录：
     `node "$SKILL_DIR/scripts/publish-report.mjs" <RUN_DIR> "<PROJECT_NAME>" "<PROJECT_ROOT>"`。
   - 发布结果固定为 `PROJECT_ROOT/需求分析/<PROJECT_NAME>-需求分析.md`。该文件是最新便捷副本，允许同名覆盖；`RUN_DIR/final-report.md` 是带时间戳的历史源文件，必须保留。
   - 用户指定了其他发布目录或文件名时服从用户要求；但除非用户明确要求，否则仍保留 `RUN_DIR/final-report.md`。
   - 最终回复必须同时给出“便捷副本”和“历史产物目录”的绝对路径。发布失败时不得宣称流程全部完成，应报告失败原因和仍可用的 `final-report.md` 路径。
8. TEST_CASES
   - 仅当用户明确要求测试点或测试用例时执行。读取 [测试用例设计](references/test-case-design.md)。
   - 先展示测试点与覆盖矩阵；用户确认后再生成结构化 JSON，以及用户要求的 Excel 或 XMind。
   - 生成 XMind 时必须使用 `scripts/generate_xmind.py`，固定层级为“所属目录 → 所属页面 → 功能点 → 测试场景 → 前置条件 → 操作步骤 → 预期结果”；相同目录、页面、功能点、测试场景必须合并为同一组节点。

## 执行约束

- 使用子任务能力时，每个阶段只允许一个执行者写对应文件；总控负责校验与汇总。没有子任务能力时按顺序自行完成。
- 不因无法登录或无法浏览而假装已读取。先尝试官方授权；仍不可访问时明确阻塞点，并基于用户提供的文本/截图继续能完成的部分。
- 原型探索限制在需求相关范围；截图放入 `RUN_DIR/screenshots/`，正文引用相对路径。
- 增量分析优先对照既有 `_analysis.md`、测试点编号和历史报告，避免重复并标注新增覆盖。
- 不把飞书访问令牌、应用密钥、浏览器 Cookie 或完整凭据写入技能、报告或日志。
- 用户提供的新需求/PRD 是证据源时，即使问题聚焦某个字段，也继续使用本技能；只有查询已上线或既有公司规则时才切换到 `business-logic-query`。

## 质量基线

- 所有结论可追溯到文档段落、页面位置、截图或明确标注的经验推导。
- 每个主流程至少检查失败分支、取消/返回、重复提交、权限差异、空态、加载态和并发影响。
- 模糊词（如“及时”“大量”“自动”）必须转换为待确认的量化问题。
- 最终报告不得残留模板占位符、补丁标记或未经验证的断言。
- 最终报告不得用“重点包括”“待明确”“完整清单见其他文件”等概括性文字代替具体澄清问题。

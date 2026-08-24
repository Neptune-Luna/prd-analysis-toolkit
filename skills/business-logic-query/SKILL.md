---
name: business-logic-query
description: Answer a focused question about Neptune's existing business rules, code-side logic, data handling, state transitions, or page interaction behavior by querying the authoritative Feishu knowledge bases. Use for requests such as 业务逻辑是什么、这个字段怎么判断、页面为什么这样跳转、状态如何流转、代码逻辑询问、交互规则查询. Do not use for analyzing a new PRD, running a full requirement review, or generating test cases; use requirement-analysis instead.
---

# 业务逻辑询问

根据飞书权威知识库回答具体业务逻辑问题。目标是快速给出可追溯的规则答案，而不是启动完整需求分析流程。

## 权威来源

先读取 [业务知识源](references/sources.md)，按问题类型选择代码逻辑库、页面交互逻辑库或两者交叉验证。使用 [查询方法](references/query-guide.md) 获取资料。

## 工作流

1. 提取问题中的模块、页面、字段、状态、动作、角色和异常关键词。
2. 分类：
   - 数据处理、接口判断、字段计算、后端状态与权限 → 代码逻辑。
   - 按钮显隐、页面跳转、弹窗、表单校验和交互反馈 → 页面交互逻辑。
   - 跨端闭环、状态与 UI 联动 → 同时查询两库。
3. 优先做关键词查询；结果不足时读取目录和相关章节，不要无目的地抓取整个知识库。
4. 对照多个命中项，区分当前规则、历史说明、例外和可能冲突。以更新时间/修订版本较新且范围更具体的内容为优先，但明确披露冲突。
5. 用以下结构回答：
   - 结论：直接回答问题。
   - 规则明细：条件 → 处理 → 结果。
   - 边界与例外：角色、状态、空值、失败、重复操作等。
   - 待确认项：仅列资料没有覆盖或相互冲突的点。
   - 来源：文档标题、章节、链接、修订版本/更新时间（若可得）。

## 约束

- 仅执行只读查询，不修改飞书内容。
- 不把常识推断写成公司既有规则。没有权威依据时明确回答“知识库未找到明确说明”，并给出一条最小化的业务确认问句。
- 不输出访问令牌、Cookie、应用密钥或其他凭据。
- 若用户的问题实质是新需求分析，简要说明并切换到 `requirement-analysis` 的完整流程。
- 用户提供的新 PRD/需求文档是证据源时归 `requirement-analysis`；只有询问已上线或既有公司规则时使用本技能。

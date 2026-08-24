# 材料读取规范

## 总则

- 优先使用用户给出的原始材料和已登录的官方只读能力。
- 记录标题、URL/路径、版本、更新时间和实际读取范围。
- 不可读取的附件、图片、嵌入表格和子文档必须列入证据缺口。
- 不输出访问令牌、Cookie、应用密钥或其他凭据。
- 除非用户明确要求，禁止修改云端文档、工作项、测试用例和权限。

## 飞书 Wiki 与 Docs

使用官方 `lark-cli` 用户授权。优先使用 PATH 中全局安装的 `lark-cli`；若不存在，按参考项目的方法在 PowerShell 中执行：

```powershell
npm.cmd install -g @larksuite/cli
```

安装后仍不可用时，当前工作区可回退到：

```text
.tools/lark-cli/node_modules/@larksuite/cli/bin/lark-cli.exe
```

检查和重新授权：

```powershell
lark-cli auth status
lark-cli auth login --domain "docs,wiki,sheets" --scope "docs:document.comment:read,docs:document.media:download,board:whiteboard:node:read"
```

以上登录参数与 `D:\git test\PrdToTestCaseProject` 保持一致。使用 CLI 生成的二维码或官方验证链接，由用户在飞书确认；再次运行 `auth status`，只有用户身份显示可用后才读取材料。

若提示 `client_secret` 缺失、配置损坏或应用未初始化，先运行 `lark-cli config show`。仅在用户明确授权配置飞书应用时，使用 `lark-cli config init --new --brand feishu` 初始化，再重新登录。不得读取、复制或输出 App Secret、访问令牌、Cookie，也不得自行拼接 OAuth 请求。

读取节点和正文：

```powershell
lark-cli wiki spaces get_node --token "<wiki-token>" --as user
lark-cli wiki +node-get --node-token "<wiki-token-or-url>" --as user
lark-cli wiki +node-list --space-id "<space-id>" --parent-node-token "<parent-token>" --page-all --page-limit 5 --as user
lark-cli docs +fetch --doc "<wiki-or-doc-url>" --as user --api-version v2 --doc-format markdown --scope outline
lark-cli docs +fetch --doc "<wiki-or-doc-url>" --as user --api-version v2 --doc-format markdown --scope keyword --keyword "<keyword>"
lark-cli docs +fetch --doc "<wiki-or-doc-url>" --as user --api-version v2 --doc-format markdown --scope full
```

先读取目录和关键词命中，无法定位时再读取全文。目录页要遍历最相关的子节点，不把目录标题当正文。

嵌入表格可使用 `sheets +workbook-info` 和 `sheets +csv-get`；画板可使用 `whiteboard +query`。无法解析时记录缺口。

## Meegle/飞书项目工作项

`lark-cli` 的 Wiki/Docs 命令不能替代工作项接口。按顺序选择：

1. 当前环境已有的 Meegle 专用连接器或 CLI，以用户身份只读读取正文、字段、附件和最新评论；
2. 已登录会话的浏览器读取页面可见内容；
3. 请用户导出工作项或粘贴正文、评论和附件。

记录工作项标题、状态、更新时间、正文范围和所读取评论的时间，不用猜测或拼接私有 API。

## 本地文本与结构化文件

- Markdown/TXT/JSON/YAML/XML：直接读取并保留标题、键路径或行号定位。
- CSV/TSV：识别编码、表头和数据行，记录行号。
- Excel：逐个读取非空 Sheet，记录 Sheet 名、表头和行号；检查隐藏 Sheet、合并单元格和公式显示值。
- `.mm`：按 XML 节点层级提取测试目录、步骤和预期。
- `.xmind`：按 ZIP 包中的 `content.json` 或兼容内容文件提取主题树；不要只读预览图。

遇到损坏、加密、宏或不支持格式时停止对该文件的推断并报告限制。

## DOCX 与 PDF

- DOCX：读取正文、标题层级、表格、页眉页脚和批注（能力允许时）；图片中的关键信息需单独识别。
- PDF：提取文本后检查页面布局；扫描 PDF 需要 OCR，表格和流程图需进行视觉核验。
- 始终保留页码、章节或表格位置，不能只留下脱离上下文的文本片段。

## OpenAPI 与接口资料

- OpenAPI/Swagger JSON 或 YAML：解析 paths、operations、parameters、requestBody、responses、schemas、security 和 examples。
- Postman 集合：区分示例请求、脚本断言和环境变量；示例成功不等于所有场景已实现。
- 接口 Markdown/HTML：同时读取字段表、错误码、时序图、状态说明和版本记录。
- 数据库设计和时序图是补充证据，不能替代外部接口契约。

## 代码与运行态证据

只有用户把代码、环境或接口纳入评审范围时才检查运行态证据：

- 代码：定位路由、校验、授权、业务服务、事务和错误处理的真实调用链。
- 接口响应：记录环境、请求、响应、时间和必要的脱敏信息。
- 日志：记录请求/追踪 ID、时间范围和关键事件，不泄露敏感数据。
- 测试结果：区分已执行结果与静态用例，记录执行时间、环境、版本和失败详情。

无法确认代码版本与技术文档版本一致时，运行态结论写“未验证”或明确限定版本。

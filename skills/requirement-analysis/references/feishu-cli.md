# 飞书 CLI 访问

使用飞书官方 `lark-cli` 的用户身份读取文档。只执行读取操作；除非用户另行明确要求，不修改云端文档或权限。

## 定位 CLI

1. 优先调用 PATH 中全局安装的 `lark-cli`。
2. 若 PATH 中不存在，按参考项目的方法在 PowerShell 中执行 `npm.cmd install -g @larksuite/cli`。使用 `npm.cmd`，避免执行策略拦截 `npm.ps1`。
3. 安装后重新定位 `lark-cli`；当前工作区的备用路径是 `.tools/lark-cli/node_modules/@larksuite/cli/bin/lark-cli.exe`，仅在全局 CLI 不可用时使用。
4. 全局 CLI 和备用路径均不可用时，明确报告缺少官方 CLI；不要回退到自建 OAuth 脚本。

## 授权

先执行：

```powershell
lark-cli auth status
```

若未登录或刷新令牌失效，执行：

```powershell
lark-cli auth login --domain "docs,wiki,sheets" --scope "docs:document.comment:read,docs:document.media:download,board:whiteboard:node:read"
```

以上参数与 `D:\git test\PrdToTestCaseProject` 保持一致。把 CLI 生成的二维码或官方验证链接原样提供给用户，由用户在飞书确认；等待 CLI 明确返回成功后再次运行 `lark-cli auth status`，只有用户身份显示可用才继续读取。

若提示 `client_secret` 缺失、配置损坏或应用未初始化，先运行 `lark-cli config show`。仅在用户明确授权配置飞书应用时，使用官方 `lark-cli config init --new --brand feishu` 初始化，再执行上述登录命令。不得读取、复制或输出 App Secret、访问令牌、Cookie，也不得自行拼接 OAuth 请求。

## Wiki 与文档读取

先解析 Wiki 节点，再抓正文：

```powershell
lark-cli wiki spaces get_node --token "<wiki-token>" --as user
lark-cli docs +fetch --doc "<wiki-or-doc-url>" --as user --api-version v2 --doc-format markdown --scope outline
lark-cli docs +fetch --doc "<wiki-or-doc-url>" --as user --api-version v2 --doc-format markdown --scope keyword --keyword "<keyword>"
lark-cli docs +fetch --doc "<wiki-or-doc-url>" --as user --api-version v2 --doc-format markdown --scope full
```

先用 `outline` 或 `keyword` 控制上下文；只有目标内容无法定位时才取 `full`。记录标题、节点 URL、修订版本或更新时间（如返回）以及本次实际读取范围。

## 嵌入内容

- 表格：从文档 XML 找到 sheet token 和 sheet-id，再用 `sheets +workbook-info`、`sheets +csv-get`。
- 画板：用 `whiteboard +query --whiteboard-token <token> --output_as raw --as user`。
- 评论：仅当评审语义依赖评论时，用 `drive file.comments list --file-token <token> --file-type docx --page-all --as user`。

任何嵌入内容读取失败都要写入证据缺口，不得根据标题猜测内容。

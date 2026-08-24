# 查询方法

使用飞书官方 `lark-cli` 的用户身份执行只读查询。

## 授权与 CLI 路径

优先使用 PATH 中全局安装的 `lark-cli`。若不存在，按参考项目的方法在 PowerShell 中执行 `npm.cmd install -g @larksuite/cli`；安装后仍不可用时，才回退到 `.tools/lark-cli/node_modules/@larksuite/cli/bin/lark-cli.exe`。

```powershell
lark-cli auth status
lark-cli auth login --domain "docs,wiki,sheets" --scope "docs:document.comment:read,docs:document.media:download,board:whiteboard:node:read"
```

以上登录参数与 `D:\git test\PrdToTestCaseProject` 保持一致。使用 CLI 生成的二维码或官方验证链接，由用户在飞书确认；再次执行 `auth status`，只有用户身份显示可用后才读取文档。

若提示 `client_secret` 缺失、配置损坏或应用未初始化，先运行 `lark-cli config show`。仅在用户明确授权配置飞书应用时，才可执行 `lark-cli config init --new --brand feishu`，随后重新登录。不得读取、复制或输出 App Secret、访问令牌或 Cookie，也不得自行拼接 OAuth 请求。

## 查询策略

对每个知识库入口依次使用：

```powershell
lark-cli wiki spaces get_node --token "<wiki-token>" --as user
lark-cli wiki +node-get --node-token "<wiki-token-or-url>" --as user
lark-cli wiki +node-list --space-id "<space-id>" --parent-node-token "<parent-node-token>" --page-all --page-limit 5 --as user
lark-cli docs +fetch --doc "<wiki-url>" --as user --api-version v2 --doc-format markdown --scope keyword --keyword "<keyword>"
lark-cli docs +fetch --doc "<wiki-url>" --as user --api-version v2 --doc-format markdown --scope outline
```

`+node-get` 用于获取节点所属 space-id 和节点信息；`+node-list` 用于遍历该节点下的直接子节点。只对命中关键词的分支继续向下遍历，避免拉取整个知识库。若入口页指向子文档，继续读取最相关的子节点。关键词至少尝试：用户原词、常见同义词、页面/模块名、状态名。只有关键词和目录均不足时才使用 `--scope full`。

查询完成后记录：命中文档标题、命中章节、URL、修订版本或更新时间（如 CLI 返回）、关键规则的准确转述。不要长篇复制原文。

# 飞书工作流

检查工具及认证，不打印凭证。优先专用连接器；CLI读取不需要浏览器。

## Meegle

使用auth status、workitem get、meta-types和meta-fields读取认证、需求、缺陷及字段配置。先查当前命令帮助，不硬编码其他项目的字段。

Neptune已验证的MQL（替换项目和ID）：

```sql
SELECT `工作项id`, `名称`, `状态`, `关联需求`
FROM `neptune_software_system`.`缺陷`
WHERE `关联需求` = '<id:7051530185>'
```

PowerShell用单引号here-string保存MQL，避免反引号被解释。传给 `meegle workitem query --project-key ... --mql $mql --auto-paginate --format json`。

- 关系函数对端系统字段使用真实API key，例如work_item_id，不猜中文系统字段名。
- 空data或list:null不能只凭退出码0认定查询成功，应核实语法和关系。
- 逐个get读取完整描述、缺陷评级、状态、责任人；独立只读请求可并行。超过50条按当前CLI分页协议获取，核对总数并按缺陷ID去重。
- 将已修复/关闭、未解决、无需修复、转需求、重复等分别统计，不为凑数误称已修复。
- 不执行测试。另有执行请求时使用run-feishu-ui-tests技能。

## 云文档

```powershell
lark-cli whoami
lark-cli docs +search --query '<需求标题关键词>'
lark-cli docs +fetch --doc '<URL>' --detail with-ids
lark-cli docs +update --help
lark-cli docs +create --help
lark-cli skills read lark-doc/references/lark-doc-xml.md
lark-cli skills read lark-doc/references/lark-doc-update.md
```

- fetch直接解析wiki URL，返回document_id、revision_id及块ID。
- 用block_replace、block_delete、block_insert_after精确修改；连续范围必须同父节点。结构变化后重新fetch再使用块ID。
- 内容写入当前工作区work/，以相对路径@file传参。不以JSON序列化代替shell转义。
- 使用最新revision-id，冲突先重读，不盲目覆盖。
- 实拍上传XML：`<img path="@./outputs/实际截图.png" caption="测试环境—对应功能"/>`。
- 创建前查既有报告；创建结果不明先检查是否已创建，不重复创建。
- 写后fetch核对内容、统计及图片资源，检查partial_success和warning。

## 实拍

本机既有UI框架曾位于D:/git test/ui-autotest，其配置含测试环境URL和账号。其他机器定位实际项目，不假定路径存在。不打印accounts.json；仅在内存加载凭证用于对应环境正常登录。

用户授权独立Playwright时可复用已安装运行时和配置，不为一张截图启动完整用例流水线。按实际页面和DOM定位功能截图。Python交互中截图调用必须赋值，例如 `_ = page.screenshot(path=...)`，避免输出PNG字节。视觉核对后取消未保存编辑，关闭本任务创建的浏览器。

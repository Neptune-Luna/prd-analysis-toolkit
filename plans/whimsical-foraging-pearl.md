# Feishu Requirement → Excel Test Case Skill 设计方案

## Context

用户是测试人员，需要从飞书工作台"需求"模块获取需求信息，经过分析后自动生成 Excel 测试用例。当前存在以下不确定性：
- 需求在飞书中的存储形式未确认（可能是多维表格、文档、Wiki 或飞书项目）
- 没有飞书 API 凭证，需要指导创建
- 测试用例模板未确定，需要灵活支持自定义格式

## 整体架构

```
用户执行 /feishu-testcase
       │
       ▼
┌─────────────────────────────────────┐
│  Step 1: 配置检查与环境准备         │
│  - 检查飞书 API 凭证配置             │
│  - 引导用户创建飞书应用（如未配置）   │
│  - 确认需求来源类型                   │
└─────────────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────┐
│  Step 2: 获取需求数据               │
│  - 调用飞书 Open API 拉取需求       │
│  - 支持多种来源：Bitable/文档/Wiki   │
│  - 保存原始需求到本地临时文件        │
└─────────────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────┐
│  Step 3: 需求分析（Claude 执行）     │
│  - 解析需求内容，提取功能点          │
│  - 识别测试场景：正向/逆向/边界/异常  │
│  - 生成结构化的测试点清单            │
└─────────────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────┐
│  Step 4: 生成 Excel 测试用例        │
│  - 使用 Python (openpyxl) 生成 xlsx │
│  - 支持自定义模板/默认模板           │
│  - 包含：ID、模块、标题、步骤、期望等 │
└─────────────────────────────────────┘
```

## 文件结构

```
C:\Users\Neptune\.claude\skills\feishu-testcase\
├── skill.md                    # Skill 定义文件（Claude 执行的指令）
├── scripts\
│   ├── feishu_client.py        # 飞书 API 客户端（获取 access_token、拉取数据）
│   ├── generate_excel.py       # Excel 测试用例生成器
│   └── requirements.txt        # Python 依赖
├── templates\
│   └── default_template.json   # 默认测试用例字段模板
└── config.example.json         # 配置文件示例
```

## 各模块设计

### 1. `skill.md` — Skill 指令

定义 Claude 执行此 Skill 时的完整工作流：
- 检查 `config.json` 是否存在且有效
- 若无凭证，引导用户去飞书开放平台创建应用
- 通过交互式问答确认需求来源类型和访问参数
- 调用 Python 脚本拉取需求数据
- 对需求进行分析（边界值、等价类、异常路径、正向流程）
- 调用 Python 脚本生成 Excel 文件
- 输出结果摘要

### 2. `feishu_client.py` — 飞书 API 客户端

核心功能：
- `get_tenant_access_token(app_id, app_secret)` — 获取 tenant access token
- `fetch_bitable_records(bitable_id, table_id, ...)` — 拉取多维表格记录
- `fetch_document_content(doc_id)` — 拉取文档内容
- `fetch_wiki_nodes(space_id, ...)` — 拉取 Wiki 节点
- `discover_resources()` — 列出用户可访问的资源（帮助用户定位需求来源）
- 统一输出为 JSON 格式的标准化需求列表

### 3. `generate_excel.py` — Excel 生成器

核心功能：
- 读取分析后的测试用例 JSON 数据
- 使用 `openpyxl` 生成格式化的 `.xlsx` 文件
- 支持通过 JSON 配置文件自定义列定义
- 默认模板字段：
  | 用例ID | 模块 | 测试标题 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 用例类型 |
- 样式：自动设置列宽、表头加粗、单元格边框、冻结首行

### 4. `config.example.json` — 配置示例

```json
{
  "feishu": {
    "app_id": "",
    "app_secret": "",
    "source_type": "bitable",
    "source_config": {
      "bitable_id": "",
      "table_id": ""
    }
  },
  "testcase_template": {
    "columns": ["用例ID", "模块", "测试标题", "前置条件", "测试步骤", "预期结果", "优先级", "用例类型"],
    "priority_levels": ["P0-冒烟", "P1-核心", "P2-常规", "P3-边缘"]
  }
}
```

## 需求分析方法论（Claude 执行）

从原始需求中提取测试用例时，系统性地覆盖以下维度：
1. **正向流程** — 正常路径，输入合法数据，返回预期结果
2. **边界值** — 输入边界值（最大/最小/临界），验证边界行为
3. **等价类** — 有效等价类和无效等价类各取代表值
4. **异常路径** — 非法输入、空值、超长字符串、特殊字符
5. **权限/角色** — 不同角色的可见性和操作权限（如适用）
6. **状态流转** — 需求中涉及的状态机转换（如适用）
7. **组合场景** — 多条件组合、并发操作（如适用）

## 飞书 API 凭证获取指引（内嵌在 Skill 中）

当用户未配置凭证时，Skill 会输出分步指引：
1. 访问 [飞书开放平台](https://open.feishu.cn/app)
2. 创建企业自建应用
3. 开通所需 API 权限：`bitable:app`、`doc:document`、`wiki:wiki` 等
4. 获取 App ID 和 App Secret
5. 配置到本地 `config.json`

## 验证方案

1. 使用示例需求数据（无需飞书 API）测试分析逻辑和 Excel 生成
2. 确认生成的 `.xlsx` 文件格式正确，可在 Excel/WPS 中打开
3. 如有飞书 API 凭证，端到端测试：拉取真实需求 → 分析 → 生成用例

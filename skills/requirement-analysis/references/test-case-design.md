# 测试用例设计

仅在用户明确要求测试点或测试用例时使用。

## 设计顺序

1. 从已确认需求、澄清结果和评审风险生成测试点覆盖矩阵。
2. 覆盖正常流程、异常分支、边界值、状态流转、权限、并发/幂等、数据一致性、兼容性与回归影响。
3. 每条用例包含：名称、所属目录、所属页面、功能点、测试场景、前置条件、步骤、预期结果、类型、需求 ID、优先级、负责人（可空）。
4. 区分“需求明确支持”和“基于质量经验建议”；对尚未澄清的规则不要写唯一确定的预期。
5. 先让用户确认测试点范围，再落盘完整用例。

## JSON、Excel 与 XMind

JSON 使用对象数组，字段与 `assets/default_template.json` 一致。步骤和预期必须可执行、可观察，避免“操作正确”“显示正常”等空泛表述。

安装依赖后生成 Excel：

```powershell
python -m pip install -r "$SKILL_DIR/scripts/requirements.txt"
python "$SKILL_DIR/scripts/generate_excel.py" --input "<cases.json>" --output "<cases.xlsx>" --columns "$SKILL_DIR/assets/default_template.json"
```

生成后检查工作表可打开、表头顺序正确、用例数与 JSON 一致、中文无乱码。

用户要求 XMind 时，每条结构化用例还必须提供以下字段：

- `directory`：所属目录。
- `page`：所属页面。
- `feature_point`：功能点。
- `test_scenario`：测试场景；未显式提供时可以用用例名称，但落盘前应补齐。
- `preconditions`：前置条件。
- `steps`：编号操作步骤。
- `expected`：与步骤对应的编号预期结果。

使用技能内置脚本生成：

```powershell
python "$SKILL_DIR/scripts/generate_xmind.py" "<cases.json>" --output "<cases.xmind>"
```

XMind 固定使用以下层级，不得插入“用例分类”或其他中间节点：

```text
项目名称
└─ 所属目录
   └─ 所属页面
      └─ 功能点
         └─ 测试场景
            └─ 前置条件
               └─ 操作步骤
                  └─ 预期结果
```

分组键依次为 `directory + page + feature_point + test_scenario`。多条用例的四个分组键相同时，必须共用同一组目录、页面、功能点和测试场景节点，并在该测试场景下分别挂载各自的前置条件、操作步骤和预期结果。

生成后必须校验：

1. XMind 是可读取的 ZIP，包含 `content.json`、`metadata.json`、`manifest.json` 和缩略图。
2. 七级层级顺序正确，没有旧版“基础功能/异常功能”等分类节点。
3. 分组后测试场景节点数等于四字段唯一组合数。
4. 最末级用例链数量等于 JSON 用例数。
5. 中文无乱码，步骤与预期完整且可观察。

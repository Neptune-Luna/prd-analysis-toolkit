# 客户APP照片反馈 —— 接口文档（前端对接用）

> 配套技术方案见 [.doc/客户APP照片反馈_技术方案.md](./客户APP照片反馈_技术方案.md)。本文档只给前端需要的请求/响应格式，实现细节不在此赘述。

## 通用响应格式

所有接口统一响应外层结构：

```json
{
  "code": 0,
  "message": "",
  "data": { ... }
}
```

`code != 0` 表示业务/参数错误，`message` 是错误描述，`data` 可能为空。

## 反馈类型枚举

| 值 | 含义 |
|---|---|
| 1 | 海生物识别 |
| 2 | 漆况识别 |

App 端 4 个按钮（海生物-是、海生物-否、漆况-是、漆况-否）对应 `feedback_type` 取 1/2、`accurate` 取 1/2 的两两组合，每次点击只提交其中一种组合。

写接口的 `accurate` 和读接口（`inspection_report`）返回的反馈字段，统一用同一套编码：**`1`=是（准确） `2`=否（不准确）**。"未反馈"在读接口里不是单独的数字，而是**字段整体不出现**（见下方第二节）。全文档只有这一套数字含义，不用在不同接口间切换 bool/int。

---

## 一、提交/修改照片反馈

**`POST /api/client-app/v1/photo/feedback`**

对同一张照片的同一反馈类型重复提交，会覆盖上一次的结果（不是新增一条记录）。

### 请求体

```json
{
  "mobi_photo_id": 123456,
  "feedback_type": 1,
  "accurate": 2
}
```

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| mobi_photo_id | int64 | 是 | 照片ID，与 `inspection_report` 响应里每张照片的 `mobi_photo_id` 一致 |
| feedback_type | int32 | 是 | 1=海生物识别 2=漆况识别 |
| accurate | int32 | 是 | 1=识别准确 2=识别不准确（没有0，写接口不存在"未选择"这个值） |

### 响应

```json
{
  "code": 0,
  "message": "",
  "data": {}
}
```

### 鉴权

沿用 App 端现有登录态（JWT/Session），无需额外传用户信息，反馈人由服务端从登录态解析。只能对当前用户有权限访问的 `mobi_id` 下的照片提交反馈，越权会返回错误。

### 可能的错误

| 场景 | 说明 |
|---|---|
| `mobi_photo_id` 不存在 | 参数错误 |
| `feedback_type` 不是 1/2 | 参数错误 |
| `accurate` 不是 1/2 | 参数错误 |
| 该照片不属于当前用户可访问的客户账号 | 权限错误 |

---

## 二、查看反馈结果：随 `inspection_report` 接口返回

**`GET /api/client-app/v1/inspection_report?mobi_id=1174`**（已有接口，不新增查询接口）

每张照片对应的分类数据对象（原有字段不变）新增两个字段：

| 字段 | 类型 | 说明 |
|---|---|---|
| `biofouling_feedback` | int32 | 海生物识别反馈：`1`=是(准确) `2`=否(不准确)。**未反馈过时，这个字段整体不会出现在响应里** |
| `paint_feedback` | int32 | 漆况识别反馈：`1`=是(准确) `2`=否(不准确)。**未反馈过时，这个字段整体不会出现在响应里** |

前端按字段是否存在来判断有没有反馈过，不要用 `0` 做判断（后端永远不会返回`0`，未反馈是直接没有这个key）：

```javascript
const biofoulingState = item.biofouling_feedback ?? null; // undefined => null(未反馈) | 1(是) | 2(否)
const paintState = item.paint_feedback ?? null;
```

### 响应示例（单张照片的分类数据片段）

```json
{
  "mobi_photo_id": 123456,
  "marine_organism": [...],
  "rating": 3,
  "biofouling_feedback": 2
}
```

上例含义：这张照片，海生物识别被反馈为"不准确"（2）；`paint_feedback` 没有出现，说明漆况识别这个维度客户还没反馈过。

---

# mobi 后台 AM配置中心 —— 反馈列表接口（内部管理后台前端对接用）

> 以下内容面向 mobi 后台管理系统前端，跟上面 App 客户端的部分是两个不同的前端项目。鉴权走内部登录态（gtoken），不是 App 那套 JWT/Session。字段设计以配套技术方案第5节为准，属于设计阶段，还未实现，实现时字段命名可能有微调。

## 三、反馈列表

**`GET /api/cloud/v1/app/photo-feedback/list`**

### 请求参数（query string）

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| current | int32 | 否，默认1 | 页码 |
| pageSize | int32 | 否，默认20 | 每页条数 |
| mobiId | int64 | 否 | 按 mobi ID 精确检索 |
| userId | int64 | 否 | 按反馈人（客户账号）精确过滤。**名称→ID 的解析由另一个已有的客户搜索接口负责**，本接口只接收解析好的ID，不做名称模糊匹配 |

### 响应

```json
{
  "code": 0,
  "message": "",
  "data": {
    "total": 37,
    "list": [
      {
        "mobi_id": 1174,
        "vessel_name": "ONE INNOVATION",
        "feedback_type": 1,
        "feedback_content": "海生物识别：不准确",
        "feedback_at": "2026-08-06 10:23:00",
        "feedback_user_id": 8821,
        "feedback_user_name": "张三",
        "mobi_photo_id": 123456,
        "photo_thumbnail_url": "https://.../thumb.jpg",
        "photo_origin_url": "https://.../origin.jpg",
        "position": {
          "level1": "左侧板",
          "level2": "五线",
          "level3": "第3张",
          "water_line": "9m"
        }
      }
    ]
  }
}
```

字段说明：

| 字段 | 说明 |
|---|---|
| mobi_id | 出动ID |
| vessel_name | 船名 |
| feedback_type | 1=海生物识别 2=漆况识别 |
| feedback_content | 展示文案，由 `feedback_type` + 反馈结果拼出，例如"海生物识别：不准确"，不是数据库里存的原始字段 |
| feedback_at | 反馈时间 |
| feedback_user_id / feedback_user_name | 反馈人ID/姓名 |
| mobi_photo_id | 反馈照片ID |
| photo_thumbnail_url / photo_origin_url | 缩略图URL用于列表展示，点击放大和右键下载走原图URL |
| position | 照片所在部位：一级/二级/三级部分 + 侧板水尺，具体字段结构待实现时对齐 `vessel_part` 现有的分级命名 |

### 权限

- 管理员 / `am_admin`：看全部客户的反馈
- 普通 AM：只能看到自己作为主/辅AM的客户名下的反馈，看不到其他 AM 管的客户（按需求文档明确要求的行级隔离）
- 都不是以上角色：无权限，返回错误

### 可能的错误

| 场景 | 说明 |
|---|---|
| 当前用户不是管理员/AM/am_admin | 权限错误 |
| `mobiId`/`userId` 查无结果 | 返回空列表（`total: 0`），不算错误 |

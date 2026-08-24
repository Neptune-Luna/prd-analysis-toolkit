# Client App 产品说明文档

> **本文讲什么**：Neptune Client App（客户端手机 App）这条产品线——客户在里面能做什么、看到什么、看不到什么，有哪些业务规则和硬性门槛，以及它和其他产品线怎么衔接。
>
> **写给谁**：产品、UI、测试、前端、后端，以及新同事、运营人员（尤其 AM）和 AI 助手。全文按「客户能感知到什么」组织，不按代码目录组织。
>
> **定位与术语**：本文是 Client App 这条产品线**独立完整**的产品说明，可以单独阅读；跨产品线边界以《产品线依赖地图》为准。术语（出动 Mobi、三板、检测线、特殊部位 Niche、R0–R4 污损等级、船体分区、边缘侧 / 云端侧、AM、报告员）沿用《Neptune 产品文档总索引》中的全局术语对照表。
>
> **正文不放代码行号**。每一条说法背后的代码位置都收在文末「附录：代码依据对照表」里。转飞书文档时，附录可以整段保留、也可以整段删掉，不影响正文阅读。

---

## 导读：不同角色怎么读这份文档

| 你的角色 | 建议读的章节 | 为什么 |
|---|---|---|
| **产品 / 客户成功 / AM** | 第 3 章（重点）→ 第 1 章 → 第 5 章 → 第 6 章 | 第 3 章可以直接拿去回答客户「我为什么看不到这条船／这份报告／这个按钮」；第 6 章是需要产品拍板的事项 |
| **UI / 设计** | 2.2 – 2.5、2.8、2.13 | 卡片形态、三层下钻、颜色口径、离线表现都在这里 |
| **测试** | 第 2 章全部 + 3.2 + 第 5 章 | 所有阈值、倒计时、缓存有效期、提示文案原文都写进了正文，可以直接当用例来源 |
| **前端 / App 研发** | 第 2 章 + 2.13 + 第 4 章 | 交互规则、缓存策略、上下游边界 |
| **后端研发** | 第 3 章 + 第 4 章 + 第 6 章第二类（安全） | 可见范围的四层过滤、接口面清单、越权缺口 |
| **只有 10 分钟** | 第 0 章 + 第 3 章 + 第 6 章前 5 条 | 最容易串线的命名、最常被问的可见性、最需要拍板的口径 |

---

## 0. 开篇必读：两条最容易串线的命名

**一句话小结**：讨论 Client App 的后端时，「app」这个词有两个完全不同的含义，先分清再往下聊。

| 容易踩的坑 | 正确说法 |
|---|---|
| **Client App 的后端不是「主后端里的 app 服务」** | 系统里并没有一个叫 app 的服务。Client App 的业务后端是云端 **helix 网关**上的一组客户端接口面（客户端业务、用户账号、通知、实时长连接四块） |
| **云端接口路径里出现的 `app` 字样不代表 Client App** | 云端那一组带 app 字样的能力面，实际是**运营后台**在用的；面向客户端的那部分只剩极少数端点，不是 App 的主链路 |

---

## 1. 产品定位与用户角色

**一句话小结**：Client App 是唯一给外部客户看的界面，客户在里面基本只「看」，唯一往回写的业务动作是「确认清洗」。

### 1.1 一句话定位

Client App 是给船东 / 船舶管理公司用的手机 App（iOS + Android，中英文），是 Neptune 全系统里**唯一面向外部客户的界面**。它是**纯消费端**：客户在这里看检测与清洗结果、拿 PDF 报告、收消息推送，**唯一往云端回写的业务动作是「确认清洗（Proceed To Clean）」**。

判断依据很直观：全 App 只有 21 个页面，没有任何报告制作、审核、AI 原始结论相关的界面；全部写操作只有账号类（登录、找回 / 修改密码、改昵称、改头像、注销）、消息标记已读，以及「确认清洗」和「查看更多照片」这两个业务动作。

### 1.2 用户角色

App 只服务一类账号——**客户**。内部员工（AM、报告员、调度等）用运营后台，不进 App。客户账号内部还有两层细分，直接决定客户看到什么：

| 角色 | 是什么 | 影响 |
|---|---|---|
| **船队管理员** | 客户组织里被标为管理员的账号 | 看得到**本组织被授权的全部船舶**的报告 |
| **普通客户成员** | 组织下的一般联系人账号 | 只看得到**逐一授权给本人**的船舶 |
| **有清洗决策权的客户** | 在运营后台被单独打开「清洗决策权」的客户账号 | **只有这类账号才会看到「确认清洗」按钮，也只有他们会收到洗船建议推送** |

**只有客户能登录 App。** 登录时会校验账号有没有 App 平台身份，不具备的直接被拒（报「only support app platform」）。

### 1.3 支持的语言与平台

- 界面语言：**英文（默认）、简体中文**。另外声明了葡语（安哥拉）语区，但**没有对应的翻译资源**。登录页只给客户中 / 英两个选项。
- 平台：Android / iOS。每次业务请求都必须带上 App 版本号与平台标识，格式不对服务端直接拒。

---

## 2. 核心功能

**一句话小结**：账号、LIVE、报告详情、评级呈现、N0 视频、确认清洗、清洗进度、PDF、History、船队、消息推送、Profile、离线体验——13 块，本章的数字和提示文案可以直接当测试用例。

### 2.1 账号与登录

**做什么**：客户用邮箱 + 密码登录，忘记密码可自助找回，登录后可改密码、改昵称、改头像、切换语言、注销账号。

**给谁用**：全部客户账号。

**业务规则**

- **登录**：邮箱格式必须合法、密码必须满足强度规则、**必须勾选隐私协议**，三者齐了登录按钮才能点。
- **密码强度**（登录 / 改密 / 找回统一一套）：必须同时含大写字母、小写字母、数字、特殊符号，且只能是 ASCII 可见字符。逐条提示为「密码只能包含 ASCII 可见字符」「密码必须包含至少一个大写字母 / 小写字母 / 数字 / 特殊符号」；界面上统一显示「Password must contain uppercase, lowercase, numbers, and symbols / 密码要同时包含大写字母、小写字母、数字、字符」。
- **首次登录强制改密**：云端返回「需重置密码」标记时，客户被强制跳到改密页，改完才能用。App 冷启动那条路径也一样。
- **账号被禁用 / 被锁定**：登录时直接拒绝，分别报「用户已禁用」「用户已锁定」。
- **登录态有效期 7 天**（云端按 168 小时配置）。
- **找回密码（未登录，三步）**：输邮箱 → 收 **6 位数字验证码** → 设新密码。验证码**有效期 10 分钟**，通过**邮件**发送；同一有效期内重复点「发送」会拿到同一个验证码。App 端重发倒计时 **60 秒**。验证码错了只把输入框变红、不弹窗；两次新密码不一致提示「Passwords do not match」。
- **修改密码（已登录）**：走另一套三步流程，规格相同（6 位码、10 分钟有效、60 秒倒计时）。
- **改昵称**：只校验去空格后非空（「Name cannot be empty! / 名称不能为空！」），**App 侧不限制长度和字符**。
- **改头像**：可拍照或从相册选，选完可裁剪。**1 MB 以内原图直传**；超过 1 MB 会在本机压缩（超过 5 MB 用质量 60，否则 75），长边超 1024 像素等比缩小，统一输出 JPEG。云端拒收过大文件时客户看到「Image too large. Please choose a smaller one. / 头像文件过大，请重新选择或裁剪更小的图片」。
- **注销账号**：三重防误触——先看警示页「PROCEED WITH CAUTION!」，**按钮有 5 秒倒计时**才可点，再弹二次确认「删除用户后，数据将立马删除，且无法恢复，确认删除吗？」。
- **异地登录踢出**：同一账号在别处登录，当前设备被清登录态、断开推送长连接、退到登录页，2 秒后提示「Your account has been logged in on another device. / 您的账号已在其他设备登录。」。
- **登录过期自动登出**：先提示「Token Expired, Please login again. / 登录已过期，请重新登录。」，再退到登录页。
- **语言切换**：立即生效、无需重启；切换后同时刷新请求语言并把新语言上报给推送服务，保证后续推送文案语种正确（语言编码：中文 1、英文 2、葡语 3）。

**限制**

- **注销账号在 App 侧只清掉本机登录凭证**，不清本地缓存的用户资料和报告列表缓存、也不断开推送长连接；云端侧是**软删除**（只打删除时间戳），而且**不写账号失效标记**——已签发的登录凭证在有效期内理论上仍可用。这条已登记为待确认（第 6 章第 9 条）。
- 密码为空时的提示是**硬编码中文「请输入密码」**，没走多语言。

### 2.2 LIVE 页签：进行中的作业

**做什么**：客户打开 App 首先看到的就是 LIVE——正在进行 / 待开始 / 刚完成的出动卡片流。

**给谁用**：全部客户账号。

**卡片上有什么**

- 船名、港口名（跟随界面语言）
- 时间：`yyyy M/d HH:mm`；待开始状态显示为「ETB @time」（预计靠泊时间）
- 状态标签四种：**In Progress（进行中）/ To Be Started（待开始）/ Completed（完成）/ Canceled（中断）**
- 船体污损示意图 + 各部位评级圆环（部位缩写 VS / PS / SS / FB / PP）
- 清洗进度条；覆盖率还没有数据时显示「Not Started」
- 提示标签：「Long interval since last cleaning（距上次清洗间隔过长）」「High-frequency cleaning recommended（建议高频清洗）」
- 清洗建议文案 + 「Wait / Proceed To Clean」两个按钮（出现条件见 2.6）
- 报告就绪时的下载报告入口

**业务规则**

- **出动号默认不显示给客户**，只有打开内部调试开关后才会追加在港口下方。客户报障时问不到出动号，需要 AM 在运营后台按船名 + 日期反查。
- **已完成的出动卡片是精简形态**：不展示污损总览、进度条、清洗建议和操作按钮，只留下载报告入口。
- **只有被 AM 打开「在 APP 展示」开关的出动才会出现**（云端强制过滤）。客户说「看不到这条船的作业」，第一件事就是查这个开关。
- **时间下限 2026-05-01**：列表默认不返回该日期之前靠泊的出动。
- **完成后仍在 LIVE 停留 72 小时**：出动完成不满 72 小时的仍按「进行中」归到 LIVE，超过 72 小时才落到 History。这也是 LIVE 与 History 互不重复的机制。
- **只展示游泳机器人相关的作业类型**。
- **5 条线检测方案的报告默认不展示给客户**，由云端开关控制。
- 分页：默认每页 20 条，最多 100 条。
- 客户可以按船名搜索（中英文模糊匹配）。

**限制**

- 在 LIVE 页按物理返回键会弹「Exit the app?」确认退出。

### 2.3 检测报告详情页：客户看报告的主战场

**做什么**：客户点卡片进入报告详情，逐层下钻看到每条检测线、每米位置的照片与评级。

**给谁用**：全部客户账号（内容受审核门控，见 3.2）。

**浏览层级**（三层）

1. **一级页签 = 部位**：左舷 / 右舷 / 底板 / 螺旋桨 / 特殊部位，横向滑动切换（部位全集为 Double Side / Port Side / Starboard Side / Flat Bottom / Propeller / Special-Niche）。哪些部位对客户可见，由云端下发的配置决定。
2. **二级页签 = 检测线**：左舷 / 右舷 / 底板下面是检测线 L1…Ln，超过 5 条时横向滚动；**螺旋桨没有二级页签**；特殊部位下面是子部位（例如海底门再分高低位）。右舷的检测线页签**从右向左排（10→1）**，符合客户从船艉看船的习惯。
3. **内容区**：船体刻度示意图（随所选线联动高亮）→ 按水尺距离分组的逐米检测照片卡（评级标签 + 海生物名称与占比）→ 底部图例。没有照片时显示「No inspection photos」。

**另有一层「总览」切换**：污损总览 / 油漆总览。切到油漆总览时看的是油漆评级，**没有油漆数据的层不会回退去显示污损评级**。

**业务规则**

- 顶部有一张按船型下发的船体分区示意图作背景。
- 二级部位的示意图上会叠加评级圆环。
- 云端没下发示意图时，App 用内置船图兜底。

**限制**

- 未选中的部位色块用 **0.35 透明度**变暗，选中的才是满色。
- 全部内容只读。客户无法修改任何评级、标注或照片选择。

### 2.4 污损与油漆评级的呈现

**做什么**：把 R0–R4 污损等级和油漆状况用统一的颜色语言呈现给客户。

**污损颜色口径**（数值原样）

| 等级 | 色值 | 含义（客户看到的图例文案） |
|---|---|---|
| R0 | `#44D42A` 绿 | No fouling / Good Condition |
| R1 | `#F2EF3C` 黄 | Microfouling，`<5%` |
| R2 | `#FDDB6E` 浅橙黄 | Light Macrofouling，`[5%, 15%)` |
| R3 | `#FE882F` 橙 | Medium Macrofouling，`[15%, 40%)` |
| R4 | `#B3171B` 暗红 | Heavy Macrofouling，`≥40%` |
| **R9 / 无值** | **完全透明** | 「无评级 / 无数据 → 不着色」的哨兵值 |

图例底部的脚注是「2023 IMO Biofouling Guidelines (MEPC.378(80))」。

**R9 = 透明的实际后果**：界面靠「透明度为 0」来判断这一层有没有数据。判空之后既不高亮也不变暗；视频报告里遇到透明会做一次回退取值。

**油漆评级颜色**：实际生效的是 1 → `#D9D9D9`、2 → `#F4B083`、3 → `#AC5A0D`，其余（含 4 和空值）→ 透明。**代码注释里写的映射与实现不一致**，已登记待确认（第 6 章第 16 条）。油漆图例的四档面积区间是 `≤5%` / `5-15%` / `15-40%` / `≥40%`，脚注是「Guidance Notes on Maintenance and Repair of Protective Coatings (May 2017)」。

**客户看到的是哪一套聚合口径**（《产品线依赖地图》§4 第 2 条指出云端并存两套，代码里有「不可混用」的警告，这里给出明确答案）

| 客户看到的位置 | 用的口径 |
|---|---|
| **LIVE 卡片 / 检测进度里的部位评级** | **逐张照片评级求均值**（只统计已选用**且已过审**的检测线） |
| **报告详情页的部位节点评级、检测线汇总评级** | **部位级池化**（先汇总 / 平均覆盖率，再整体评一次级） |

也就是说：**客户在卡片上看到的部位评级，和他在报告详情页里看到的同一个部位的评级，来自两套不同算法，数值可能不一致。** 云端有一个开关决定走不走「客户端口径」。补充两条细节：双舷（VS）是派生项，取左右舷非零值的均值；10 线集装箱船的底板首线被排除在统计之外。

**App 侧不做二次计算**：云端直接下发部位级 / 检测线级 / 层级 / 逐张照片级的评级值，App 只负责把 1–5 映射成 R0–R4 标签，无值就显示 `---`。

**海生物污损分类配置**：客户看到的污损分类图例（分类名、说明、图标）由云端下发，云端**硬编码 4 档**：

| 分类 | 中文 | 涵盖生物 |
|---|---|---|
| Microfouling | 轻微污染 | Slime / 生物膜 |
| Macrofouling | 中度污染 | Algae, Seagrass / 海藻、海草 |
| Soft fouling | 重度污染 | Tunicates / 海葵 |
| Hard fouling | 严重污染 | Barnacles, Mussels, Calcium Deposit, Tubeworms / 藤壶、贝类、钙沉积、管虫 |

注意：这 4 档是**给客户看的分类图例**，和运营后台可维护的「海生物类型」清单不是一套东西——**在后台改海生物配置不会改变 App 上的这 4 档**。分类图标从 OSS 取。

### 2.5 N0 视频报告

**做什么**：N0 机器人做的检测，产出是**视频**而不是逐米照片，客户在报告详情页会多一层「视频报告 / 照片报告」切换。

**给谁用**：出动执行方式含 N0 的客户（App 侧按出动执行方式判定）。

**业务规则**

- **8 段视频**：云端按编号 1–8 下发，与部位的对应关系是——左舷段 1/2/3、右舷段 4/5、底板段 6/7/8。每段标注它覆盖的检测线，例如「Port side - L1–L3」「L4」「L5」。
- **视频与检测数据联动**：播放到哪里，屏幕上就显示该位置发现的海生物种类、占比和评级。数据按时间桶下发，按播放毫秒命中当前桶。为了不闪屏，**刷新按 5000 毫秒一档节流**；只有跳变超过 2500 毫秒才立即刷新。
- 污染物以 **3 列网格卡**呈现（不是表格），每格顶部有一条评级色边框和占比进度条。
- 视频段的污染物评级优先与照片报告同源（按物种名匹配对应层的评级），匹配不到才用时间桶里的评级。
- 视频报告的一级部位**不含螺旋桨和特殊部位**。

**限制**

- **播放器只有播放 / 暂停**：时间轴是只读的三层进度显示，**不能拖拽跳转**；全屏图标虽然在，但**没有接点击响应**。
- 没有字幕功能（视频遥测字幕是内部数据链路，不下发给客户）。
- 某段没有视频时显示禁播占位图，评级显示 `—`，控件禁用。
- 视频段卡片的标题是**硬编码中文模板「视频 N（部位）」，没走多语言**。

### 2.6 确认清洗（Proceed To Clean）——App 上唯一的业务回写

**做什么**：AM 在检测报告审核时勾了「建议客户洗船」之后，客户在卡片和报告详情页会看到清洗建议文案和两个按钮：**Wait（稍等）** / **Proceed To Clean（继续清洗）**。客户点确认，等于向 Neptune 表达「可以洗」。

**给谁用**：**只有被打开「清洗决策权」的客户账号**（见 1.2）。其他客户账号即便是同一条船的联系人，也看不到按钮。

**按钮出现的四个条件（缺一不可）**

1. 出动状态为**进行中**。
2. 云端下发的**两个按钮开关同时为真**。
3. 云端侧：**该部位的检测线全部审核通过**，且当前处于**过审后 8 小时的窗口内**（窗口起点取「最后一次审核通过时间」与「建议洗船时间」两者中较晚的那个）。
4. 云端侧：请求者**有清洗决策权**；查不到就按无权处理。

> 团队早期的口径 / 过去对外的说法是「客户能不能看到确认清洗按钮，取决于 AM 是否勾了建议洗船」——这是必要条件，但**不是全部**。客户反馈看不到按钮时，按上面四条依次排查，尤其是**8 小时窗口**和**这个客户有没有清洗决策权**。

**点下去发生什么**

- **没有二次确认弹窗**，点了就提交。
- 提交中按钮变成转圈，两个按钮同时不可点。
- 提交成功后：**清洗建议文案和两个按钮整块消失，只留清洗进度条**；LIVE 卡片和报告详情页两处**同步隐藏**（靠一个全局刷新计数跨页同步）。
- 云端只做两件事：把「谁在什么时候决策的」写进该出动的检测报告文档，以及**给该出动的飞书作业群和主 / 辅 AM 发一张通知卡片**。
- **幂等**：重复提交恒成功，用最新时间覆盖。**没有撤销入口**；一旦决策，按钮永久隐藏。

**对出动流程的影响（关键结论）**

团队早期的口径 / 过去对外的说法是「客户点了确认，流程才进入清洗阶段」——这是**业务意图**。**代码现状是：确认清洗不会自动推进出动状态机**，实现处明确注明「本期仅日志 + 落库，不触发真实洗船」，整个报告服务里没有任何流程状态机的推进调用。实际推进到清洗阶段的动作，由 AM 收到飞书通知后在运营后台手动完成。**这条口径差异已登记为待确认，是本文最需要人拍板的一条（第 6 章第 1 条）。**

**Wait（稍等）按钮**做的是另一件事：向云端请求「查看更多照片」，提交后同样把两个按钮收起。

**限制 / 风险**

- 云端的提交入口**只校验出动号非空和登录态**，**不校验这个出动是不是属于这个客户**。已登记为待确认（第 6 章第 8 条）。
- 提交失败只弹云端返回的文案，界面不变。出动号缺失时提示「Feature under development...」。
- 清洗建议文案**只用云端下发的原文**，App 本地不再拼模板；收起时显示 3 行、展开 8 行，超过 3 行才出展开箭头。

### 2.7 清洗进度

**做什么**：出动进入清洗后，客户在卡片和报告详情页都能看到清洗进度条。

**业务规则**：进度条**始终展示**，不受清洗决策按钮显隐的影响。进度数据来自云端汇总的作业监控数据，最终源头是边缘侧作业平台上报的三板清洗面积（见第 4 章）。

### 2.8 PDF 报告：下载、预览、分享

**做什么**：报告发布后，客户在卡片上点下载，拿到 PDF，可以在 App 内翻页看，也可以通过系统分享转发给同事。

**业务规则**

- **报告没生成时**点下载，提示「Report not ready yet / 报告尚未生成」。判断依据是云端有没有下发 PDF 地址——这个地址只有在云端渲染完成并回写之后才有值。
- **文件名**：`Neptune_<船名>_<出动编号>.pdf`，船名里的非法字符替换成下划线。
- **下载有实时进度条**。下载完成弹「Download successful / Tap to View PDF」，**弹窗期间屏蔽返回键**。
- **App 内预览**：支持双指缩放、侧栏缩略页跳转、左下页码、上 / 下页按钮。
- **系统分享**：调系统分享面板转发文件。
- **已下载记录会持久保存**（船名 + 出动编号 → 本机文件路径），下次点击直接打开本地文件；文件被系统清理掉时清掉记录并提示报告未就绪。
- 下载失败提示「Download failed. Network timeout, please check your network. / 下载失败，网络超时，请检查网络」。

**限制**

- PDF 存在**系统临时目录**下，系统清理临时空间时会丢；这就是「下载过的报告过一段时间又要重新下」的原因。
- PDF 的版式就是报告页面的最终样子，由云端定时任务用无头浏览器打开报告渲染页截图生成——**报告页面上的任何内容问题都会原样出现在客户拿到的 PDF 里**。

### 2.9 History 页签：历史报告

**做什么**：客户查已完成的历史作业。

**业务规则**

- **两种浏览方式**：按时间分组浏览（「Operation within 1 Month」/「Operation in 1-3 Months」），或按船舶分组浏览。
- 可按船名搜索（搜索框提示「Search by vessel name」）。搜索历史**最多保留 6 条**。
- **时间窗口硬限制：只有近 90 天**，分组切分点是 30 天。**超过 90 天的历史报告，客户在 App 里查不到。**
- 只含已完成和已取消的出动，且**排除刚完成不满 72 小时的**（那些还在 LIVE）。同样只含已发布到 App 的出动。
- **History 不分页**，90 天窗口内一次全出。
- 历史卡片信息比 LIVE 精简，只有船名（大写）和港口。
- 空态提示「No active inspections」，加载到底提示「All results loaded」。

### 2.10 船舶列表（船队）

**做什么**：客户查看自己被授权的船队，以及每条船最近一次作业的时间。

**业务规则**

- 船队范围完全由授权决定：船队管理员看组织全部授权船，普通成员看逐一授权给本人的船。
- 分页默认每页 5 条，最多 100 条。
- 云端会带上每条船的最近作业时间和最近一次出动编号，用于排序。
- **查不到客户身份时返回空列表而不是报错**——客户看到的是「空船队」而不是错误提示。这是排查「客户说啥都看不到」时的一个常见表象。

### 2.11 消息中心与推送

**做什么**：客户在 Profile 里进消息中心看站内信；重要事件通过手机推送触达，点推送直达对应报告。

**消息中心业务规则**

- 消息只有：标题、正文、关联出动、已读状态、时间。**没有消息分类 / 类型标签**给客户看。
- 未读小红点由云端返回的「有没有未读」决定，**App 不做本地计数，也不显示未读条数**。
- 点消息 → 自动标记已读 + 拉出动详情 + 跳转报告详情页。消息没有关联出动时提示「Invalid message data / 消息数据无效」。
- **只有单条标记已读，没有「全部已读」**。
- 每页 10 条，空态「No notifications yet. / 还没有收到任何通知」。
- 消息按客户账号严格隔离（云端按登录账号过滤）。

**客户实际会收到哪两类推送**（云端目前只有这两类业务推送）

| 推送 | 什么时候发 | 发给谁 | 客户看到的文案 |
|---|---|---|---|
| **检测审核完成** | AM 在运营后台**审核通过某个部位**时 | 该船关联的客户账号 | 「您所管理的船只已有部分区域完成检测，请点击查看>>」/「Some areas of the vessel you manage have completed inspection, please click to view >>」；同时写一条站内信 |
| **洗船建议** | AM 在检测报告里**打开「建议客户洗船」**开关时 | **只发给有清洗决策权的客户账号**；5 条线的报告不发 | 标题「洗船建议 / Cleaning recommendation」；正文「Inspection for <船名> is in progress. Based on current inspection results, …」+ 建议正文 |

**注意：「报告发布」和「出动阶段变更」目前都不发推送。** 客户想知道清洗报告发好了，只能自己打开 App 看。

**推送通道**

- **App 内长连接**：连上就把全部未读站内信补发一遍，之后**每 120 秒推一条全局刷新信号**让 App 重新拉数据。云端每 30 秒主动发心跳，App 侧也设了 30 秒心跳。
- **重连规则（精确数字）**：连接失败先立即重试，**最多 2 次**（间隔 1 秒）；**第 2 次失败后进入 8 分钟冷却**，冷却结束自动重连并清零计数。冷却期内不再发起连接。
- **系统级推送**：Android 走 FCM，iOS 走 APNs（iOS 侧先试生产环境证书，失败再退开发环境）。App 侧优先上报 APNs 令牌，回落 FCM。
- **设备注册**：以「客户账号 + 设备」为唯一键，重复注册就更新。推送令牌**超过 7 天**才会重新上报。
- **点推送直达报告**：App 冷启动时最多等 15 秒（每 200 毫秒轮询）等首页就绪，再按推送里的出动号拉详情并跳转报告详情页；已经在同一份报告页就原地刷新，在别的报告页就原地换数据。拉取失败提示「Failed to load data」。

**限制**

- **App 内长连接默认是关闭状态**（有一个全局开关）。
- **实时性远没有「实时」**：云端原本按业务事件通过消息总线推送的逻辑**整段被注释掉了**，所以长连接实际只剩「连上补未读」和「每 120 秒全局刷新」两种行为。客户看到数据更新的延迟上限约 2 分钟。
- 通知栏展示由原生层负责，Flutter 侧的本地通知已废弃。
- 推送服务在 App 启动后**延迟 15 秒**才初始化；用户资料在进主页后**延迟 4 秒**才拉。

### 2.12 Profile 与设置

**做什么**：客户在这里看自己的资料、进消息中心、改设置、看关于和隐私政策、退出登录。

**业务规则**

- 只有 Profile 页签有顶部背景图。
- 切到 Profile 会刷新未读红点。
- **退出登录**确认文案「Confirm Logout? / 确定要退出登录吗？」；主按钮是「Cancel」，红色文字按钮才是「Log Out」——刻意设计成不易误触。退登会解绑推送、清凭证、断开长连接。
- **版本检查**：只有「关于」页里的手动「Check for Updates」，**没有启动时自动检查、没有强制更新**。有新版本只弹一个可取消的提示，跳应用商店。
- **首次启动引导**：内置 4K 引导视频随包发布；是否看过记录在本机。
- 隐私政策是一个公网静态页。

**限制**

- 云端的「版本号」接口返回的是**硬编码的 `1.0.1`**，没有配置来源、没有强更字段。所以版本检查功能目前**实际不可用**——已登记为待确认（第 6 章第 12 条）。
- 版本号比较只看前 3 段数字，非数字段一律当 0；本机版本号带 flavor 后缀（如 `1.0.1-dev`）时会被判成 `1.0.0`。
- iOS 跳商店的地址用包名拼接，代码自己也注明缺真实 App Store ID。

### 2.13 离线与弱网下的实际体验

**做什么**：客户在船上、在港口这类网络差的地方，App 尽量还能看到东西。

**缓存了什么、多久有效**（数值原样）

| 内容 | 存哪 | 有效期 |
|---|---|---|
| 登录用户资料 | 本机对象库 | 常驻，登出清 |
| **检测报告列表（LIVE / History 共用）** | 本机对象库 | **5 分钟** |
| 报告详情 | 本机对象库 | 5 分钟 |
| **船舶列表** | 本机对象库 | **24 小时** |
| 登录凭证、推送令牌、已下载报告清单、语言、搜索历史 | 本机偏好存储 | 无过期 |
| **照片、船体示意图、图标** | 应用支持目录下的媒体缓存 | **持久，跨重启保留** |

**断网时客户看得到什么**

| 页面 | 断网表现 |
|---|---|
| LIVE | **能出内容**（读 5 分钟内的列表缓存），并 Toast「No internet connection!」 |
| History（按时间 / 按船分组） | **能出内容** |
| History 筛选后的任务列表 | **空**（这条路径没有缓存兜底） |
| 报告详情的照片与船图 | **已看过的能出**（媒体缓存持久保留），没看过的是空的 |
| 消息中心 | **空**（纯网络，无缓存） |
| 未读红点 | 静默保持上次的值 |
| 污损分类图例 | **冷启动断网就没有**（只在内存缓存，不落盘） |
| 船舶列表 | 能出（24 小时缓存） |
| 已下载的 PDF | **能打开** |

**照片缓存去掉签名参数带来的后果**：报告照片、船体示意图的地址都带会过期变化的 OSS 签名，所以缓存的键**刻意只保留域名和路径、丢掉查询串**。

- **好处**：同一张照片换了签名不会重复下载，客户的流量和等待都省了，离线也能看。
- **代价**：**同一路径的图片内容被替换后，客户端不会察觉，会一直显示旧图**。运营侧替换报告照片时如果沿用了同一存储路径，客户看到的可能还是替换前那张——排查「客户说照片不对」时要考虑这一层。清掉它的唯一途径是重装 App 或走缓存清理逻辑。

**其他弱网设计**：图片下载连接超时 12 秒 / 接收超时 20 秒；业务请求连接与接收各 30 秒。

---

## 3. 客户能看到什么、看不到什么（本文最重要的一章）

**一句话小结**：客户看到的东西，是全量数据经过**四层过滤**后的结果；运营后台里有 13 类东西 App 里根本没有；另外账号被禁用能即时生效，但有一个 Redis 故障时的例外。这一章可以直接拿给产品和客户成功团队看。

### 3.1 两套账号体系、两个入口——它们怎么联动

运营后台和 Client App 是**两套完全独立的账号体系和鉴权机制**，只通过一个失效标记联动。

| | 运营后台（内部） | Client App（客户） |
|---|---|---|
| 谁在用 | AM、报告员、调度、管理员等内部员工 | 船东 / 船舶管理公司 |
| 入口 | 云端的运营后台服务 | 云端 helix 网关上的客户端接口面 |
| 鉴权方式 | **会话式令牌**（状态存 Redis，后台一改立即生效） | **无状态令牌**（签发后 7 天内自带效力，云端不逐次查库） |
| 登录态有效期 | 见运营后台文档 | **7 天** |
| 平台限制 | — | 账号必须有 App 平台身份，否则拒登 |

**后台「禁用 / 删除客户」是怎么让 App 侧即时失效的**（这是两套体系唯一的联动点）

1. 运营人员在后台禁用或删除一个客户成员 → 云端往 Redis 写一个**账号失效标记**，**保留 7 天**（正好覆盖登录态的 7 天有效期）。禁用 / 启用、删除客户、后台禁用用户这几个动作都会触发。
2. App 的每一次请求都会被网关中间件检查这个标记，命中就直接拦下，客户看到「account has been deleted」或「account has been disabled」。
3. 重新启用会清掉标记，客户立即恢复。

> ⚠️ **要知道的例外一（安全风险）**：**Redis 挂了的时候，中间件选择放行而不是拦截**（只打一条告警日志）。也就是说 Redis 故障期间，刚被禁用的客户在登录态到期前仍然可以访问。已登记为待确认（第 6 章第 10 条）。
>
> ⚠️ **要知道的例外二（安全风险）**：客户在 App 里**自助注销**账号走的是另一条路——只软删账号记录，**不写这个失效标记**。所以自助注销之后，那张已经签发出去的令牌在 7 天有效期内理论上还能用。已登记为待确认（第 6 章第 9 条）。

### 3.2 客户的数据可见范围：四层过滤

客户看到的报告，是全量数据经过四层过滤后的结果。**任意一层不满足，客户就看不到。**

**第一层：船舶授权**（决定客户能碰哪些船）

- 客户账号先归到一个**客户组织**。
- **船队管理员** → 取该组织被授权的全部船舶（组织级授权）。
- **普通成员** → 取逐一授权给本人的船舶（用户级授权）。
- 授权关系由运营后台维护。
- **查授权失败时的行为是「返回空列表」而不是报错**（历史报告同理）。客户看到的是空白页，不是错误提示。
- 完全识别不出客户身份时才返回「无权限」。

**第二层：出动是否发布到 App**

- 云端强制只返回被 AM 打开「在 APP 展示」开关的出动；历史报告那条路径更是写死只查已发布的。
- 这个开关由运营后台的出动更新动作写入。

**第三层：内容审核门控**（决定客户在一份可见的报告里能看到多少）

即便报告对客户可见，**未经 AM 审核通过的检测线内容会被清空**再下发：

- 未过审的检测线，它的海生物标注和评级汇总会被清空，检测线级的评级汇总也会被隐藏。
- 客户在 App 上看到某条线「没有数据」，最常见的原因不是没拍，而是**AM 还没审到那条线**。

**第四层：时间与范围限制**

| 限制 | 数值 |
|---|---|
| 出动靠泊时间下限 | **2026-05-01 之前的不返回** |
| History 时间窗口 | **只有近 90 天** |
| 完成后停留 LIVE | **72 小时** |
| 作业类型 | 只展示游泳机器人相关的类型 |
| 5 条线检测方案的报告 | 默认**不给客户看**（云端开关） |

### 3.3 运营后台有、但 App 里看不到的东西（13 项）

这是本章的核心对照表。左列是运营后台的能力，右列说明客户在 App 里为什么看不到。

| # | 运营后台有 | Client App 看不到 |
|---|---|---|
| 1 | **报告制作页 / 报告六态流转**（未开始 → 部分完成 → 制作中 → 待审核 → 已发布 → 冻结中） | App 里没有任何报告制作、编辑、审核界面；全 21 个页面没有一个是编辑类的 |
| 2 | **报告制作中间态** | 客户端通道上云端**只允许「查看更多照片」这一种更新**，其他更新（发布、写 PDF 地址、改档位、写洗船建议）一律以参数非法拒掉 |
| 3 | **AI 原始结论**（七合一 AI 输出的物种、覆盖率、质量分、油漆类型原始记录） | **没有任何客户端入口能读到 AI 原始结论**；客户只看到经过审核门控的派生评级 |
| 4 | **人工修改前后的 AI 反馈记录**（redo log） | 同上，客户端无入口 |
| 5 | **未过审的检测线内容** | 被清空后才下发（见 3.2 第三层） |
| 6 | **未发布到 App 的出动** | 云端硬过滤（见 3.2 第二层） |
| 7 | **其他客户的数据** | 检测报告列表、历史报告、船舶列表都按船舶授权过滤 |
| 8 | **预览报告** | 客户端入口拿不到未发布的报告；只有内部平台身份才会关闭发布过滤 |
| 9 | **照片水印**（时间戳、部位戳） | 客户端通道恒定按「不打水印」组装照片 |
| 10 | **出动全流程状态机的 10 个阶段** | App 只呈现 4 个粗粒度状态（进行中 / 待开始 / 完成 / 中断） |
| 11 | **出动唯一编号** | 默认不展示（仅调试开关下可见） |
| 12 | **设备台账、防拆记录、遥控箱、OTA、飞书作业群、年度订单、客户 / 船队主数据管理** | App 里没有任何对应界面 |
| 13 | **视频遥测字幕、原始视频、抽帧原图** | 客户只看到 8 段成品视频和已选用的报告照片 |

### 3.4 越权防护的现状（需要如实说明）

**做得到的**：检测报告列表与详情、历史报告、船舶列表都把船舶授权条件下推到了查询里；客户拿别人的出动号去查检测报告，**查不出行，返回空列表**（不是 403）。

**⚠️ 做不到的（三个安全缺口，均已登记待确认）**：

| 能力 | 缺什么 |
|---|---|
| 清洗报告 | **完全没有权限和船舶范围校验**，只按出动号查；出动号不存在时甚至会创建一份默认文档 |
| N0 视频报告 | **没有权限校验**；而且**不传出动号时会跨出动分页返回所有报告** |
| 确认清洗 | **不校验这个出动是不是属于这个客户** |

对照：运营后台侧的建单流程有完整的客户越权防护——建单时会校验传入的客户确实是客户角色，且如果该客户不是船队管理员，必须逐一验证他对这条船有授权，否则返回「无权限」。

### 3.5 客户端里的内部调试面（不是客户功能，但随生产包发布）

⚠️ 这些入口客户理论上碰不到，但确实在生产包里：

- **环境切换开关默认为开**，4 个环境可切；连带导致调试角标恒显示。
- **「关于」页连点标题 7 次**会打开调试对话框，能看到推送令牌、设备 ID、登录凭证，并能开关「首页显示出动号」和「HTTP 抓包」（抓包悬浮窗宿主包住了整个 App）。
- **推送调试页**注册了路由但**没有任何入口可达**（业务代码零调用）。
- 云端也在客户端路由组下挂了三个**生成测试报告 / 测试视频**的入口，由云端开关控制。

这些是否该随生产包发布、归谁维护，已登记待确认（第 6 章第 11 条）。

---

## 4. 与其他产品线的接口

**一句话小结**：App 只有一个业务后端（云端 helix 网关），加上 OSS、FCM / APNs 三条外部依赖；客户看到的报告数据来自一条很长的上游链路，App 只在最后一环消费；另外还有一条不在 App 内的邮件触达通道。

以《产品线依赖地图》为边界基准，这里只写与 Client App 直接相关的那几条。

### 4.1 Client App ← 云端（helix 网关）

**唯一业务后端**。App 所有接口地址集中在一处配置里，按环境切换域名：生产 `ms.neptune-robotics.com`、预发布 `testms.neptune-robotics.com`。

客户端接口面提供的能力，大致分四组（完整端点清单见附录）：

| 分组 | 客户能拿到什么 |
|---|---|
| **客户端业务** | LIVE 列表、单出动报告详情、历史报告、N0 视频报告、清洗报告、**确认清洗**、查看更多照片、船舶列表、污损分类图例、消息中心与标记已读、版本号 |
| **用户账号** | 登录 / 登出、资料读写（含头像上传）、改密三步、找回密码三步、注销账号 |
| **通知** | 推送设备注册与更新 |
| **实时** | 实时刷新长连接 |

两点需要注意：

- **登录和找回密码这三步注册在免鉴权路由组里**（不在用户路由文件里），先前浅扫代码时没找到它们就是这个原因。
- **清洗报告的接口云端有实现，但 App 侧没有见到调用**——客户实际是通过 PDF 而不是接口看清洗报告。已登记待确认（第 6 章第 18 条）。

### 4.2 Client App ← 对象存储（阿里云 OSS）

照片、船体 / 部位示意图、视频、报告 PDF 都是云端下发的**带签名的存储地址**，App 直接下载并在本机持久缓存（见 2.13）。示意图地址由云端按船型和部位生成（船型会先做归一化，总布置图还可以按客户组织覆盖）。

### 4.3 Client App ← Google / Apple 推送

Android 走 FCM、iOS 走 APNs；云端凭证从配置中心动态拉取。极光推送已停用，App 侧只留了空占位字段。

### 4.4 客户报告数据的上游链路（客户看到的东西是怎么来的）

按《产品线依赖地图》§2.1–§2.5：边缘侧（NOS 遥控箱 / BOS 作业队笔记本）采集照片与视频 → 打包上 OSS → 云端抽帧（每秒 4 帧）→ 七合一 AI 识别海生物与油漆 → 算 R0–R4 → 结论落库 → AM 在运营后台核对并逐部位审核 → 定时任务用无头浏览器打开报告渲染页截成 PDF、存 OSS 并回写地址 → **客户在 App 里看到报告和 PDF**。

Client App 在这条链路上**只在最后一环消费**，不参与任何采集、计算或制作。

### 4.5 定期提醒邮件（另一条触达客户的通道，不在 App 内）

除了 App 推送，客户还会收到定期提醒邮件——**收件人就是客户 App 账号的邮箱**。

- 收件人由云端按「提醒配置里的成员 → 该成员的邮箱」解析；邮箱为空就跳过并记一条日志。
- **邮件里的船只范围同样受船舶授权约束**，口径和 App 完全一致（船队管理员看组织授权船，普通成员看个人授权船）。保存提醒配置时就会校验每位成员对每条船都有权限，否则报「某账号不具有某船的权限」。
- **客户可以退订**：邮件里带一个 30 天有效的退订链接，点了就把该客户从这份提醒的收件人里排除（退订入口本身免鉴权）。
- 邮件正文里附 AM 联系人和邮箱。

---

## 5. 关键业务流程（端到端）

**一句话小结**：五条最常被问到的端到端流程，按「谁在什么时候做了什么」串起来。

### 5.1 客户从「船检完了」到「看到报告」

1. **AM 在运营后台逐部位审核检测报告**，审核通过。
2. 云端立刻做两件事：给该船的客户账号**写一条站内信 + 发一条推送**（「您所管理的船只已有部分区域完成检测，请点击查看>>」）。
3. **客户点推送** → App（冷启动时最多等 15 秒首页就绪）按推送里的出动号拉详情 → 直接落到该出动的报告详情页。
4. 或者**客户自己打开 App**：LIVE 页签出现这条船的卡片（前提：AM 已打开「在 APP 展示」开关）。
5. 客户在报告详情页按 **部位 → 检测线 → 逐米照片** 三层下钻查看。**没审到的线内容是空的**（见 3.2 第三层）。
6. App 内长连接每 120 秒收一次全局刷新信号，客户不动手也会看到数据更新（延迟上限约 2 分钟）。

### 5.2 客户做清洗决策

1. **AM 在检测报告审核时勾选「建议客户洗船」**。
2. 云端给**有清洗决策权的客户账号**发「洗船建议 / Cleaning recommendation」推送。
3. 客户打开 App，在 LIVE 卡片或报告详情页看到清洗建议文案和 **Wait / Proceed To Clean** 两个按钮——前提是 2.6 里那四个条件全部满足，尤其**过审后 8 小时内**。
4. **客户点 Proceed To Clean**（无二次确认）→ 云端记下「谁在什么时候决策的」，并**给该出动的飞书作业群和主 / 辅 AM 推一张卡片**。
5. 客户这边：建议文案和两个按钮整块消失，只留清洗进度条；卡片和详情页同步隐藏；**决策不可撤销**。
6. **AM 收到飞书通知，在运营后台手动把出动推进到清洗阶段。** ⚠️ 团队早期的口径 / 过去对外的说法是「客户确认后流程进入清洗阶段」，而代码现状是不自动推进——见本文第 6 章第 1 条。
7. 客户在 App 上跟进清洗进度条。

### 5.3 客户拿 PDF 报告

1. 清洗报告在运营后台**审核通过并发布** → 云端置发布标记，并把 PDF 生成任务幂等入队。
2. 定时任务消费队列，用**无头浏览器打开报告渲染页截成 PDF**，上传 OSS，回写下载地址。
3. 客户在 App 卡片上出现**下载报告**入口（地址有值才出现，否则点了提示「Report not ready yet / 报告尚未生成」）。
4. 客户点下载 → 看实时进度条 → 完成弹「Tap to View PDF」→ App 内翻页预览 → 可走系统分享转发。
5. 已下载记录持久保存，下次点击直接开本地文件。⚠️ 文件在系统临时目录，被系统清理后需要重新下载。
6. **报告发布本身不发推送**——客户不会被主动告知「报告好了」，需要自己打开 App 看，或者由 AM 另行告知。

### 5.4 后台禁用一个客户，App 侧多久失效

1. 运营人员在后台禁用该客户成员。
2. 云端往 Redis 写账号失效标记，保留 7 天。
3. 该客户**下一次 App 请求**就被拦下，收到「account has been disabled」。**即时生效，不用等登录态过期。**
4. 重新启用 → 清标记 → 客户立即恢复。
5. ⚠️ Redis 故障期间会放行（见 3.1 例外一）。

### 5.5 客户忘记密码

1. 客户在登录页点「Forgot password」→ 输邮箱 → 云端生成 **6 位数字验证码**，**10 分钟有效**，**邮件**发出。
2. 客户输码校验。**校验这一步不消费验证码**，所以校验通过后即使设密码失败，还能重来。
3. 客户设新密码 → 成功之后验证码才被删除。
4. 有效期内点「Resend」拿到的是**同一个码**；App 端重发倒计时 60 秒。
5. 没收到码时可以进「Didn't get code」帮助页看 4 条排查建议。

---

## 6. 待确认清单

**一句话小结**：共 **18** 条，按影响面从大到小排；第二类（安全）建议单独开工单。每条只写「问题是什么、影响什么、需要谁拍板」，代码位置见附录。

### 一、口径级（会影响产品对外说法）

1. **「客户确认清洗后流程自动进入清洗阶段」与代码不符。** 团队早期的口径 / 过去对外的说法是这样，但代码明确注明「本期仅日志 + 落库，不触发真实洗船」，且报告服务全域没有流程状态机推进调用，实际靠飞书通知 AM 手动推进。**影响**：对客户的承诺口径、AM 的操作手册。**需要产品拍板**：是产品预期未实现，还是文档写超前了？本文按代码事实写。
2. **客户看到的部位评级并存两套算法，数值可能不一致。** LIVE 卡片 / 检测进度用「逐张照片评级求均值」，报告详情页的部位节点用「部位级池化」，同一部位在两个界面可能显示不同等级。**影响**：客户会直接看到矛盾数字，客服无法解释。**需要产品 + 算法拍板**：对客户的官方口径是哪一套？
3. **「客户能不能看到确认清洗按钮」的判定条件比团队早期的口径多三条**：过审后 8 小时窗口、该客户账号有清洗决策权、该部位检测线全部过审。**影响**：客服口径需要更新，否则「勾了就该能看到」会误导客户。**需要产品拍板**：8 小时窗口是刻意设计还是临时值？
4. **「清洗决策权」这个客户账号内的二级权限，团队早期的口径 / 过去对外的说法里完全没提。** 它决定谁能看到按钮、谁收洗船建议推送。**影响**：运营配置遗漏会直接导致客户看不到按钮。**需要运营 + 产品明确**：归谁维护、默认值是什么？
5. **History 只有近 90 天、LIVE 只到 2026-05-01 之后。** **影响**：客户要查更早的报告时没有兜底方案。**需要产品拍板**：这两个硬门槛是产品决策还是过渡措施？更早的报告怎么给客户？

### 二、安全与合规（⚠️ 建议单独开工单，逐条走安全评审）

6. ⚠️ **清洗报告入口无任何权限校验**：只按出动号查，任何登录客户都能拿到任何出动的清洗报告；而且出动号不存在时还会创建一份默认文档（可被用来污染数据）。**需要后端 + 安全定级修复。**
7. ⚠️ **N0 视频报告入口无权限校验，而且不传出动号时会跨出动分页返回所有报告**——等于一次请求可以枚举全量视频报告。**需要后端 + 安全定级修复。**
8. ⚠️ **确认清洗入口不校验出动归属**：理论上任一客户都可以为任意出动做清洗决策，并触发发给 AM 的飞书通知。**影响不只是数据，还会造成误派工。需要后端 + 安全定级修复。**
9. ⚠️ **App 自助注销只软删账号、不写失效标记**，已签发的令牌在 7 天有效期内仍然可用。**与 GDPR 类「立即删除」承诺可能冲突，需要法务 / 产品 + 后端确认。**
10. ⚠️ **账号失效检查在 Redis 故障时选择放行**，故障期间被禁用的客户仍可访问。**需要后端 + 安全拍板**：这是刻意的可用性取舍，还是遗漏？
11. ⚠️ **生产包里的环境切换开关默认为开**，且「关于」页连点 7 次就能拿到登录凭证与推送令牌、还能开 HTTP 抓包。**需要 App 研发 + 安全拍板**：是否该在生产包里关闭？

### 三、功能缺失 / 半成品

12. **版本检查功能实际不可用**：云端返回硬编码的 `1.0.1`，无配置来源、无强更字段；App 侧的版本比较对带 flavor 后缀的版本号会误判；iOS 跳商店缺真实 App Store ID。**影响**：无法引导客户升级，也没有强更能力。**需要产品 + 双端排期。**
13. **App 内长连接默认关闭，且业务事件推送的代码整段被注释掉了**，「实时推送」目前实际就是 120 秒轮询刷新。**需要产品 + 后端拍板**：这是过渡状态还是终态？
14. **报告发布不发推送**，客户不知道报告什么时候好了。**影响**：完全依赖 AM 手工告知。**需要产品拍板**：是否该补这条推送？
15. **视频报告播放器只能播放 / 暂停**，时间轴不可拖拽、全屏按钮没接响应。**需要产品 + App 研发确认**：是未完成还是刻意？

### 四、实现细节 / 文档漂移（登记备查）

16. **油漆评级颜色的代码注释与实现不一致**：注释声明 1/2/3 → `#D9D9D9`、4 → `#F4B083`、5 → `#AC5A0D`；实现是 1 → `#D9D9D9`、2 → `#F4B083`、3 → `#AC5A0D`、其余透明。**需要 UI + App 研发确认以哪套为准。**
17. **两处硬编码未国际化的文案**：密码为空提示「请输入密码」、视频段标题「视频 N（部位）」。**英文用户会看到中文。需要 App 研发修复。**
18. **葡语（安哥拉）语区已声明但没有翻译资源**，仓库里另有一份零引用的安哥拉银行数据。**需要产品确认**：安哥拉市场是在研需求还是残留？另外，**清洗报告接口云端有实现但 App 侧未见调用**——客户是通过 PDF 而不是接口看清洗报告，需确认是否符合预期。

---

## 附录：代码依据对照表

> 本附录把正文里每一条说法对应的代码位置集中在这里，供研发核对。转飞书文档时可整段保留或整段删除，不影响正文阅读。
>
> 路径均相对各代码仓库根目录；主要涉及 `client-mobile-app`（App 端）与 `voyager_server`（云端）两个仓库。

### A0. 命名口径（对应第 0 章）

| 文档中的说法 | 代码位置 |
|---|---|
| Client App 的后端是 helix 网关上的客户端接口面（客户端业务 / 用户 / 通知 / 长连接四块） | `voyager_server/internal/helix/app/gateway/biz/router/infra/clientapp.go:24-44`；`client-mobile-app/lib/config/api_config.dart:78-115` |
| 云端带 app 字样的路径是运营后台能力面，面向客户端的只剩 4 个端点 | `voyager_server/api/cloud/v1/user/app_frontend/app_frontend.go:13-40` |

### A1. 产品定位与角色（对应第 1 章）

| 文档中的说法 | 代码位置 |
|---|---|
| 全 App 只有 21 个页面，无报告制作 / 审核 / AI 结论界面 | `client-mobile-app/lib/app/routes/app_pages.dart:52-187` |
| 客户角色枚举 | `voyager_server/internal/consts/consts_cloud.go:22` |
| 船队管理员看组织全部授权船 | `voyager_server/internal/helix/handler/internal/report/service/inspection.go:517-520` |
| 普通成员看逐一授权给本人的船 | `voyager_server/internal/helix/handler/internal/report/service/inspection.go:522-532` |
| 清洗决策权决定按钮可见性与推送收件人 | `.../report/service/recommend_cleaning.go:158-173`；隐藏按钮 `.../cleaning_decision.go:262-277`；收件人 `.../recommend_cleaning.go:175-202` |
| 非 App 平台身份拒登（「only support app platform」） | `voyager_server/internal/helix/app/gateway/biz/handler/infra/jwt.go:121-124` |
| 葡语语区已声明但无翻译资源；登录页只给中 / 英 | `client-mobile-app/lib/config/translations/localization_service.dart:30-34,52-56`；`.../login/controllers/login_container_controller.dart:71-74` |
| 每次请求必带版本号与平台标识 | `voyager_server/internal/helix/app/gateway/biz/router/infra/middleware.go:25-55,165-167` |

### A2.1 账号与登录

| 文档中的说法 | 代码位置 |
|---|---|
| 邮箱 + 密码 + 勾隐私协议才能点登录 | `client-mobile-app/lib/app/modules/login/controllers/login_container_controller.dart:423-431` |
| 密码强度规则与逐条提示、统一提示文案 | `.../login_container_controller.dart:459-490,253` |
| 首次登录强制改密 | `.../login_container_controller.dart:554-561`；启动路径 `.../splash/controllers/splash_controller.dart:298-307` |
| 账号禁用 / 锁定拒登 | `voyager_server/internal/helix/app/gateway/biz/handler/infra/jwt.go:112-119` |
| 登录态 7 天（168 小时） | 配置 `voyager_server/internal/helix/config/config.yaml:109-111`；实现 `.../jwt.go:51` |
| 找回密码 6 位码 / 10 分钟 / 有效期内复用同码 / 邮件发送 | `voyager_server/internal/helix/handler/user.go:70-87,102-103,110,377-378,385` |
| 重发倒计时 60 秒；验证码错误只变红；两次密码不一致提示 | `client-mobile-app/.../login_container_controller.dart:680-690,721,752-757` |
| 改密（已登录）三步同规格 | `client-mobile-app/lib/app/modules/change_password/controllers/change_password_controller.dart:27-32,111-119`；云端 `voyager_server/internal/helix/handler/user.go:89-206` |
| 改昵称只校验非空、无长度限制 | `client-mobile-app/lib/app/modules/edit_name/controllers/edit_name_controller.dart:75-78` |
| 头像 1 MB 阈值、5 MB / 质量 60 与 75、长边 1024、输出 JPEG、过大提示 | `client-mobile-app/lib/app/modules/user_info/controllers/user_info_controller.dart:544-596,464-479` |
| 注销三重防误触、5 秒倒计时、二次确认文案 | `client-mobile-app/lib/app/modules/profile/controllers/delete_account_controller.dart:15-18,39-57,74-81` |
| 异地登录踢出（判定 HTTP 401 + 业务码 40105）与提示 | `client-mobile-app/lib/app/services/base_dio_client.dart:295-343,72-73,198-208`；云端单设备开关 `voyager_server/.../middleware.go:532-583` |
| 登录过期自动登出提示 | `client-mobile-app/.../base_dio_client.dart:346-391` |
| 语言切换即时生效、上报推送语言、语言编码 1/2/3 | `client-mobile-app/lib/app/modules/language_selection/controllers/language_selection_controller.dart:44-80,60-64` |
| 注销只清本机凭证，不清缓存、不断长连接 | `client-mobile-app/.../delete_account_controller.dart:129-135` |
| 云端注销是软删除、不写失效标记 | `voyager_server/internal/helix/handler/user.go:473-490`（对比后台删除 `voyager_server/internal/library/token/token.go:82-91`） |
| 密码为空提示硬编码中文 | `client-mobile-app/.../login_container_controller.dart:461` |

### A2.2 LIVE 页签

| 文档中的说法 | 代码位置 |
|---|---|
| 卡片字段、时间格式、ETB、出动号调试开关 | `client-mobile-app/lib/app/modules/live_tab/widgets/live_inspection_card_new.dart:79-94,325-349` |
| 四种状态标签 | `.../live_inspection_card_new.dart:1429-1435` |
| 部位缩写 VS / PS / SS / FB / PP | `.../live_inspection_card_new.dart:1168-1176` |
| 覆盖率无数据显示「Not Started」 | `.../live_inspection_card_new.dart:1120` |
| 两条提示标签文案 | `.../live_inspection_card_new.dart:710,720` |
| 已完成卡片精简形态 | `.../live_inspection_card_new.dart:21-32` |
| 只返回已发布到 App 的出动 | `voyager_server/internal/helix/app/gateway/biz/handler/infra/inspection_report_service.go:27-32,133`；SQL 层 `.../report/service/inspection.go:608-610` |
| 靠泊时间下限 2026-05-01 | `voyager_server/.../inspection_report_service.go:20,40-48` |
| 完成后停留 LIVE 72 小时；LIVE 与 History 不重复 | `voyager_server/.../report/service/inspection.go:630-644`；`.../history.go:81-85` |
| 只展示游泳机器人作业类型 | `voyager_server/.../inspection.go:589-598` |
| 5 条线报告默认不给客户看 | `voyager_server/.../inspection.go:612-616` |
| 分页默认 20、最多 100 | `voyager_server/.../inspection.go:698-712` |
| 按船名中英文模糊搜索 | `voyager_server/.../inspection.go:618-628` |
| 返回键弹「Exit the app?」 | `client-mobile-app/lib/app/modules/main/controllers/main_app_controller.dart:80-95` |

### A2.3 报告详情页

| 文档中的说法 | 代码位置 |
|---|---|
| 一级部位页签横向切换 | `client-mobile-app/lib/app/modules/inspection_detail/views/inspection_detail_view_part_header_tabs.dart:1346-1373` |
| 部位常量与顺序 | `client-mobile-app/lib/app/data/models/live_inspection_model.dart:2350-2355` |
| 可见部位由云端配置决定 | `.../inspection_detail/controllers/inspection_detail_controller.dart:2392-2399` |
| 二级检测线页签、超 5 条滚动、螺旋桨无二级、特殊部位分子部位 | `.../views/inspection_detail_view_part_line_selector.dart:53-120` |
| 右舷检测线从右向左排（10→1） | `.../inspection_detail_controller.dart:343-360` |
| 逐米照片渲染、距离分组、「No inspection photos」 | `.../views/inspection_detail_view_part_photo_list.dart:113-127`；`.../inspection_detail_controller.dart:2654-2865,727` |
| 污损总览 / 油漆总览切换；无油漆数据不回退 | `.../inspection_detail_controller.dart:457-460`；`.../inspection_detail_view_part_header_tabs.dart:836-937`；`.../inspection_detail_view.dart:1409-1441` |
| 按船型下发的分区示意图作背景 | `.../inspection_detail_view_part_header_tabs.dart:22-56` |
| 二级部位示意图叠加评级圆环 | `.../inspection_detail_view_part_ship_progress.dart:223-259` |
| 无示意图时内置船图兜底 | `client-mobile-app/lib/app/data/models/live_inspection_model.dart:1067-1072` |
| 未选中部位 0.35 透明度 | `.../inspection_detail_view.dart:1403` |

### A2.4 评级呈现

| 文档中的说法 | 代码位置 |
|---|---|
| R0–R4 色值与 R9 = 透明 | `client-mobile-app/lib/utils/constants.dart:18-35`（哨兵值 `:30-34`） |
| 图例文案与 IMO 脚注 | `client-mobile-app/lib/config/translations/en_US/en_us_translation.dart:338-353`；图例卡 UI `.../inspection_detail_view_part_header_tabs.dart:939-1034` |
| 靠透明度判空、判空后不高亮不变暗；视频报告遇透明回退 | `.../inspection_detail_view.dart:1397-1400`；`.../widgets/inspection_video_report_body.dart:36-43` |
| 油漆评级颜色实现（1/2/3 有色、其余透明） | `client-mobile-app/lib/utils/constants.dart:42-59` |
| 油漆图例四档区间与脚注 | `client-mobile-app/lib/config/translations/en_US/en_us_translation.dart:54-74` |
| LIVE 卡片 / 进度用「逐张求均值」 | `voyager_server/.../report/service/inspection.go:1092` → `.../inspection_progress_detail.go:89-151,182-276` |
| 报告详情用「部位级池化」 | `voyager_server/.../report/service/inspection_tools.go:3833`；`voyager_server/internal/helix/handler/internal/report/domain/line_rating.go:62,86-89` |
| 客户端口径开关与判定 | `voyager_server/.../inspection.go:1092`；`.../report_stamp.go:31-34` |
| 双舷取左右舷非零均值 | `.../inspection_progress_detail.go:145-168` |
| 10 线集装箱船底板首线被排除 | `.../inspection_progress_detail.go:191-195` |
| App 只做 1–5 → R0–R4 映射，无值显示 `---` | `client-mobile-app/lib/app/data/models/live_inspection_model.dart:1287-1310` |
| 污损分类图例由云端下发 | `client-mobile-app/lib/app/services/fouling_config_service.dart:9-64` |
| 云端硬编码 4 档分类；图标取自 OSS | `voyager_server/internal/helix/handler/client_app.go:26-66`（图标 `:60-63`） |

### A2.5 N0 视频报告

| 文档中的说法 | 代码位置 |
|---|---|
| 按出动执行方式判定是否有视频报告 | `client-mobile-app/lib/app/data/models/live_inspection_model.dart:527-536` |
| 8 段视频与部位对应关系、每段覆盖的检测线 | `client-mobile-app/lib/app/data/models/n0_inspection_video_report_model.dart:139-150,152-184` |
| 时间桶下发与按播放毫秒命中 | `.../n0_inspection_video_report_model.dart:67-85,118-136` |
| 5000 毫秒节流、跳变超 2500 毫秒立即刷新 | `client-mobile-app/lib/app/modules/inspection_detail/widgets/inspection_video_report_body.dart:397-399,430-447` |
| 3 列网格卡 + 评级色边框 + 占比进度条 | `.../inspection_video_report_body.dart:1060-1152` |
| 评级优先与照片报告同源，匹配不到用时间桶 | `.../inspection_video_report_body.dart:72-112` |
| 视频报告一级部位不含螺旋桨与特殊部位 | `.../inspection_detail_view_part_header_tabs.dart:1376-1392` |
| 只有播放 / 暂停，时间轴只读，全屏图标未接响应 | `.../inspection_video_report_body.dart:790-886,149-186` |
| 无视频时禁播占位、评级 `—`、控件禁用 | `.../inspection_video_report_body.dart:927-937` |
| 视频段标题硬编码中文模板 | `.../n0_inspection_video_report_model.dart:186-190` |

### A2.6 确认清洗

| 文档中的说法 | 代码位置 |
|---|---|
| 条件一：出动状态为进行中 | `client-mobile-app/lib/app/modules/live_tab/widgets/live_inspection_card_new.dart:99`；状态判定 `.../live_inspection_model.dart:987` |
| 条件二：云端两个按钮开关同时为真 | `.../live_tab/widgets/live_inspection_in_progress_session.dart:21-24`；解析 `.../live_inspection_model.dart:1908-1926` |
| 条件三：该部位检测线全部过审 + 过审后 8 小时窗口（起点取较晚者） | `voyager_server/.../report/service/inspection.go:2687-2688`；`.../cleaning_decision.go:22,45-77` |
| 条件四：请求者有清洗决策权，查不到按无权 | `voyager_server/.../inspection.go:964-977`；`.../cleaning_decision.go:262-277` |
| 无二次确认弹窗、提交中转圈、两键同时禁用 | `client-mobile-app/.../live_inspection_in_progress_cleaning_panel.dart:709-740,723,747-748` |
| 成功后整块消失、两处同步隐藏（全局刷新计数） | `.../live_inspection_in_progress_cleaning_panel.dart:727-730`；`.../live_inspection_in_progress_session.dart:9` |
| 云端只落库 + 发飞书卡片给作业群与主 / 辅 AM | `voyager_server/.../cleaning_decision.go:146-159,171,183-260` |
| 幂等、最新时间覆盖、无撤销、按钮永久隐藏 | `.../cleaning_decision.go:131,45-53` |
| 不自动推进出动状态机（「本期仅日志 + 落库」） | `.../cleaning_decision.go:130` |
| Wait 按钮实际是「查看更多照片」 | `client-mobile-app/lib/app/data/providers/inspection_provider.dart:592-638` |
| 提交入口只校验出动号非空与登录态 | `voyager_server/.../cleaning_decision.go:132-174` |
| 提交失败提示、出动号缺失提示 | `client-mobile-app/.../live_inspection_in_progress_cleaning_panel.dart:731-734,718-721` |
| 建议文案只用云端原文；3 行 / 8 行展开规则 | `.../live_inspection_in_progress_cleaning_panel.dart:280-293,51-52,566-574` |

### A2.7 – A2.8 清洗进度与 PDF

| 文档中的说法 | 代码位置 |
|---|---|
| 进度条始终展示，不受按钮显隐影响 | `client-mobile-app/.../live_inspection_in_progress_cleaning_panel.dart:18,441` |
| 「Report not ready yet / 报告尚未生成」 | `client-mobile-app/lib/app/modules/live_tab/controllers/live_tab_controller.dart:968-975` |
| PDF 地址由云端渲染完成后回写 | `voyager_server/internal/helix/handler/internal/report/infra/presign.go:11-25`；回写 `.../report/service/inspection.go:1351-1354` |
| 文件名规则与非法字符替换 | `client-mobile-app/.../live_tab_controller.dart:1062-1068` |
| 下载实时进度条 | `.../live_tab_controller.dart:1001-1010` |
| 下载完成弹窗期间屏蔽返回键 | `client-mobile-app/lib/app/components/dialogs/download_success_dialog.dart:29-30` |
| App 内预览（缩放、缩略页、页码、上下页） | `client-mobile-app/lib/app/modules/pdf_viewer/views/pdf_viewer_view.dart:44-47,169-346` |
| 系统分享面板 | `.../pdf_viewer_view.dart:348-366` |
| 已下载记录持久保存、文件丢失时清记录 | `client-mobile-app/lib/app/data/local/my_shared_pref.dart:179-214`；`.../live_tab_controller.dart:1014,1033-1045` |
| 下载失败文案 | `client-mobile-app/lib/config/translations/en_US/en_us_translation.dart:410-411` |
| PDF 存系统临时目录 | `client-mobile-app/.../live_tab_controller.dart:993-999` |

### A2.9 – A2.10 History 与船舶列表

| 文档中的说法 | 代码位置 |
|---|---|
| 按时间分组标题；按船舶分组 | `client-mobile-app/lib/app/modules/all/widgets/history_operation_section.dart:40-42`；`.../history_embedded_vessel_section.dart:30` |
| 搜索框提示；搜索历史最多 6 条 | `client-mobile-app/lib/app/modules/all/views/history_tab_view.dart:355`；`client-mobile-app/lib/app/data/local/my_shared_pref.dart:33,251-262` |
| History 只有近 90 天；30 天分组切分点 | `voyager_server/internal/helix/handler/internal/report/service/history.go:89-93`；`voyager_server/internal/helix/handler/internal/report/domain/history.go:21-46` |
| 只含完成 / 取消，排除不满 72 小时；只含已发布 | `voyager_server/.../service/history.go:81-85,75` |
| History 不分页 | `.../service/history.go:133-139` |
| 历史卡片只有船名（大写）与港口 | `client-mobile-app/lib/app/modules/all/widgets/history_operation_preview_card.dart:41-42,104-107` |
| 空态与加载到底文案 | `.../history_tab_view.dart:286,318` |
| 船队范围由授权决定 | `voyager_server/.../report/service/inspection.go:5520-5559` |
| 船舶列表分页默认 5、最多 100 | `voyager_server/.../inspection.go:5562-5574` |
| 返回最近作业时间与最近出动编号用于排序 | `voyager_server/.../inspection.go:5578,5594-5600` |
| 查不到客户身份返回空列表 | `voyager_server/.../inspection.go:5525-5528` |

### A2.11 消息中心与推送

| 文档中的说法 | 代码位置 |
|---|---|
| 消息字段只有标题 / 正文 / 关联出动 / 已读 / 时间 | `client-mobile-app/lib/app/data/models/message_model.dart:37-48` |
| 未读红点只用布尔值，不做计数 | `client-mobile-app/lib/app/modules/profile/controllers/profile_controller.dart:104-122` |
| 点消息标记已读 + 跳报告；无关联出动提示 | `client-mobile-app/lib/app/modules/messages/controllers/messages_controller.dart:104-179,113-118` |
| 只有单条已读，无全部已读 | `client-mobile-app/lib/app/data/providers/message_provider.dart:83-126` |
| 每页 10 条；空态文案 | `.../messages_controller.dart:26`；`.../views/messages_view.dart:121-122` |
| 消息按登录账号隔离 | `voyager_server/internal/helix/handler/client_app.go:127` |
| 检测审核完成推送 + 站内信与文案 | `voyager_server/.../report/service/inspection_tools.go:2455-2529`（文案 `:2476-2481`；站内信 `:2426-2453`） |
| 洗船建议推送、收件人、文案 | `voyager_server/.../report/service/recommend_cleaning.go:217-261`（收件人 `:175-202`；文案 `:236-239`） |
| 报告发布 / 阶段变更不发推送 | `voyager_server/internal/helix/handler/mobi.go:111-114`；`voyager_server/.../report_published_hook.go:40-51` |
| 长连接连上补未读；每 120 秒全局刷新 | `voyager_server/internal/helix/handler/client_app.go:246-263,265-268,294-302` |
| 云端 30 秒心跳；App 侧 30 秒心跳 | `voyager_server/internal/helix/app/gateway/biz/handler/infra/wss.go:94-117`；`client-mobile-app/lib/app/services/push/push_websocket_service.dart:152` |
| 重连 2 次（间隔 1 秒）+ 8 分钟冷却 + 冷却后清零 | `client-mobile-app/.../push_websocket_service.dart:26-28,101-108,225-229` |
| FCM / APNs；iOS 先生产证书再退开发；App 侧优先 APNs | `voyager_server/internal/helix/handler/pusher.go:56-202`（`:112-118`）；`client-mobile-app/lib/app/services/push/push_notification_service.dart:318-374` |
| 设备注册以账号 + 设备为唯一键；令牌超 7 天才重报 | `voyager_server/internal/helix/handler/deviceregistration.go:33-87`；`client-mobile-app/lib/app/services/push/push_token_manager.dart:385-403` |
| 冷启动最多等 15 秒（200 毫秒轮询）后跳报告；失败提示 | `client-mobile-app/lib/app/services/push/push_notification_handler.dart:172-217,270-493` |
| 长连接默认关闭 | `client-mobile-app/.../push_websocket_service.dart:38` |
| 业务事件推送代码整段被注释 | `voyager_server/.../report/service/inspection.go:4600-4631` |
| Flutter 侧本地通知已废弃 | `client-mobile-app/.../push_notification_service.dart:246-255,499-520` |
| 推送延迟 15 秒初始化；资料延迟 4 秒拉 | `client-mobile-app/.../splash_controller.dart:323-328`；`.../main_app_controller.dart:205-208` |

### A2.12 Profile 与设置

| 文档中的说法 | 代码位置 |
|---|---|
| 只有 Profile 有顶部背景图；切到 Profile 刷新红点 | `client-mobile-app/lib/app/modules/main/controllers/main_app_controller.dart:169,187-192` |
| 退出登录文案与按钮层级；退登解绑推送 / 清凭证 / 断连 | `client-mobile-app/lib/app/components/dialogs/logout_dialog_helper.dart:64,91,111-116,131-143` |
| 只有手动检查更新、无自动检查与强更；提示可取消并跳商店 | `client-mobile-app/lib/app/modules/about/controllers/about_controller.dart:119-180,159-166,201-219` |
| 内置 4K 引导视频；看过与否记录在本机 | `client-mobile-app/lib/app/modules/user_guide/controllers/user_guide_controller.dart:23-24`；`client-mobile-app/lib/app/data/local/my_shared_pref.dart:19-33` |
| 隐私政策为公网静态页 | `client-mobile-app/lib/utils/constants.dart:15` |
| 云端版本号硬编码 `1.0.1`、无强更字段 | `voyager_server/internal/helix/handler/client_app.go:307-312` |
| 版本比较只看前 3 段、flavor 后缀会误判 | `client-mobile-app/.../about_controller.dart:182-199` |
| iOS 跳商店缺真实 App Store ID | `client-mobile-app/.../about_controller.dart:208` |

### A2.13 离线与弱网

| 文档中的说法 | 代码位置 |
|---|---|
| 用户资料常驻本机对象库 | `client-mobile-app/lib/app/data/local/my_hive.dart:11-13` |
| 检测报告列表缓存 5 分钟 | `client-mobile-app/lib/app/data/local/inspection_cache_manager.dart:10` |
| 报告详情缓存 5 分钟 | `.../inspection_cache_manager.dart:155,462-490` |
| 船舶列表缓存 24 小时 | `client-mobile-app/lib/app/data/local/vessel_cache_manager.dart:8-10` |
| 凭证 / 令牌 / 已下载清单 / 语言 / 搜索历史无过期 | `client-mobile-app/lib/app/data/local/my_shared_pref.dart:19-33` |
| 媒体文件持久缓存、跨重启保留 | `client-mobile-app/lib/app/services/oss_media_cache.dart:269-278` |
| LIVE 断网出缓存 + Toast | `client-mobile-app/lib/app/modules/live_tab/controllers/live_tab_controller.dart:420-459,705-709` |
| History 断网出缓存 | `client-mobile-app/lib/app/modules/all/controllers/history_tab_controller.dart:650-660` |
| History 筛选后任务列表无缓存兜底 | `client-mobile-app/lib/app/modules/all/controllers/history_task_list_controller.dart:115` |
| 已看过的照片 / 船图断网能出 | `client-mobile-app/lib/app/components/images/oss_cached_image.dart:43-52` |
| 消息中心断网为空 | `client-mobile-app/lib/app/modules/messages/controllers/messages_controller.dart:48-67` |
| 未读红点静默保持上次值 | `client-mobile-app/lib/app/modules/profile/controllers/profile_controller.dart:117-121` |
| 污损分类图例只在内存缓存 | `client-mobile-app/lib/app/services/fouling_config_service.dart:11` |
| 船舶列表断网能出 | `client-mobile-app/.../vessel_cache_manager.dart:27-53` |
| 已下载 PDF 断网能开 | `client-mobile-app/.../live_tab_controller.dart:979-982` |
| 缓存键丢掉查询串（签名） | `client-mobile-app/lib/app/services/oss_media_cache.dart:41-56` |
| 图片超时 12 / 20 秒；业务请求 30 / 30 秒 | `client-mobile-app/.../oss_media_cache.dart:22-23`；`client-mobile-app/lib/app/services/base_dio_client.dart:120-121` |

### A3. 客户可见范围（对应第 3 章）

| 文档中的说法 | 代码位置 |
|---|---|
| App 侧登录态 7 天（配置） | `voyager_server/internal/helix/config/config.yaml:109-111` |
| 必须有 App 平台身份 | `voyager_server/.../jwt.go:121-124` |
| 失效标记（key 前缀 `helix:gateway:user:invalid:` + 账号 ID，保留 7 天） | `voyager_server/internal/library/token/token.go:67,72,75-91` |
| 触发点：禁用 / 启用、删除客户、后台禁用用户 | `voyager_server/internal/logic/app/customer.go:209,216,705`；`voyager_server/internal/logic/cloud_auth/auth.go:1046,1139` |
| 每请求检查标记并拦截（40106 / 40107） | `voyager_server/internal/helix/app/gateway/biz/router/infra/middleware.go:518-527,589-636`；文案常量 `voyager_server/internal/helix/consts/const.go:18-19,24-25` |
| 重新启用清标记 | `voyager_server/internal/library/token/token.go:110-119` |
| Redis 故障时放行（只打告警） | `voyager_server/.../middleware.go:617-622` |
| 自助注销不写失效标记 | `voyager_server/internal/helix/handler/user.go:473-490` |
| 客户账号归属客户组织 | `voyager_server/.../report/service/inspection.go:500-507` |
| 组织级 / 用户级船舶授权 | `voyager_server/.../inspection.go:508-520,522-532` |
| 查授权失败返回空列表 | `voyager_server/.../inspection.go:563-565`；历史报告 `.../scope.go:97-99` |
| 识别不出客户身份返回无权限 | `voyager_server/.../inspection.go:571-574` |
| 只返回已发布到 App 的出动；历史报告写死已发布 | `voyager_server/.../inspection_report_service.go:27-32,133`；`.../inspection.go:608-610`；`.../history.go:75` |
| 发布开关由出动更新动作写入 | `voyager_server/internal/helix/handler/mobi.go:111-114` |
| 未过审检测线内容被清空 | `voyager_server/.../inspection.go:1078-1088`；实现 `.../inspection_tools.go:893-1046,832` |
| 靠泊下限 / History 90 天 / 停留 72 小时 / 作业类型 / 5 线报告 | `voyager_server/.../inspection_report_service.go:20,40-48`；`.../history.go:89-93`；`.../inspection.go:630-644,589-598,612-616` |
| App 无编辑类路由（21 个页面） | `client-mobile-app/lib/app/routes/app_pages.dart:52-187` |
| 客户端通道只允许「查看更多照片」更新；其他更新报参数非法 | `voyager_server/.../inspection_report_service.go:411-424`；`voyager_server/.../inspection.go:1161-1167` |
| AI 原始结论只在服务端内部读取 | `voyager_server/internal/helix/handler/internal/report/infra/photo_rating.go:150-167`；`voyager_server/internal/helix/handler/ai.go:235`；`voyager_server/.../inspection_tools.go:3160` |
| AI 反馈记录（redo log）无客户端入口 | `voyager_server/internal/helix/handler/internal/report/infra/redo_writer.go:118-130` |
| 其他客户数据按授权过滤 | `voyager_server/.../inspection.go:499-534,581`；`.../scope.go:91-129`；`.../history.go:52` |
| 预览报告：只有内部平台身份关闭发布过滤 | `voyager_server/.../inspection_report_service.go:22-32,110-119` |
| 客户端通道恒不打水印 | `voyager_server/.../inspection_report_service.go:293-295` |
| App 只呈现 4 个状态；出动号默认不展示 | `client-mobile-app/.../live_inspection_card_new.dart:1429-1435,325-349` |
| 传别人的出动号查不出行（返回空列表） | `voyager_server/.../inspection.go:714-719` |
| 缺口一：清洗报告无权限校验，出动号不存在会创建默认文档 | `voyager_server/internal/helix/handler/internal/report/service/clean.go:81-206`（尤其 `:94-125`） |
| 缺口二：N0 视频报告无权限校验，且不传出动号跨出动返回 | `voyager_server/internal/helix/handler/n0_inspection_report.go:36-116`（尤其 `:79-116`） |
| 缺口三：确认清洗不校验出动归属 | `voyager_server/.../cleaning_decision.go:132-174` |
| 对照：运营后台建单有完整越权防护 | `voyager_server/internal/logic/app/mobi_create.go:246,305-321` |
| 环境切换开关默认为开；调试角标恒显示 | `client-mobile-app/lib/config/env/app_env.dart:73`；`client-mobile-app/lib/main.dart:233` |
| 连点 7 次打开调试对话框；抓包悬浮窗宿主 | `client-mobile-app/lib/app/modules/about/controllers/about_controller.dart:242-291`；`client-mobile-app/lib/app/services/http_capture/`；`client-mobile-app/lib/main.dart:243` |
| 推送调试页有路由无入口 | `client-mobile-app/lib/app/routes/app_pages.dart:92-96` |
| 云端客户端路由组下的三个测试报告 / 测试视频入口 | `voyager_server/.../router/infra/clientapp.go:41-43`；开关 `voyager_server/internal/helix/pkg/config/config.go:272` |

### A4. 与其他产品线的接口（对应第 4 章）

| 文档中的说法 | 代码位置 |
|---|---|
| App 接口地址集中一处；生产 / 预发布域名 | `client-mobile-app/lib/config/api_config.dart`；`client-mobile-app/lib/config/env/env_online.dart:11`；`.../env_predistribution.dart:11` |
| LIVE 列表 / 单出动报告详情 | `GET /api/client-app/v1/inspection_report` — App `client-mobile-app/lib/config/api_config.dart:78,86`；云端 `voyager_server/internal/helix/app/gateway/biz/handler/infra/inspection_report_service.go:65-138` |
| 历史报告 | `GET /api/client-app/v1/inspection_report/history` — App `.../api_config.dart:82`；云端 `.../inspection_report_service.go:153-185` |
| N0 视频报告 | `GET /api/client-app/v1/n0_inspection_report` — App `.../api_config.dart:91`；云端 `.../inspection_report_service.go:312-350` |
| 清洗报告（App 侧未见调用） | `GET /api/client-app/v1/clean_report` — 云端 `.../inspection_report_service.go:250-298` |
| 确认清洗 | `POST /api/client-app/v1/inspection_report/cleaning_decision` — App `client-mobile-app/lib/app/data/providers/inspection_provider.dart:548-589`；云端 `voyager_server/.../cleaning_decision.go:132-174` |
| 查看更多照片 | `POST /api/client-app/v1/inspection_report` — App `.../inspection_provider.dart:592-638`；云端 `.../inspection_report_service.go:411-424` |
| 船舶列表 | `GET /api/client-app/v1/vessels` — App `.../api_config.dart:115`；云端 `voyager_server/.../inspection.go:5511-5600` |
| 污损分类图例 | `GET /api/client-app/v1/config` — App `client-mobile-app/lib/app/services/fouling_config_service.dart:26`；云端 `voyager_server/internal/helix/handler/client_app.go:26-66` |
| 消息中心 / 标记已读 | `GET`、`PUT /api/client-app/v1/message` — App `.../api_config.dart:99,102`；云端 `voyager_server/internal/helix/handler/client_app.go:102-211` |
| 版本号 | `GET /api/client-app/v1/version` — App `.../api_config.dart:109`；云端 `voyager_server/.../client_app.go:307-312` |
| 登录 / 登出 | `POST /api/user/v1/login`、`logout` — App `.../api_config.dart:35`；路由 `voyager_server/.../noauth.go:25`、`user.go:28`；实现 `voyager_server/.../jwt.go:88-205,287-301` |
| 资料读 / 改（含头像上传） | `GET`、`PUT /api/user/v1/profile` — App `.../api_config.dart:41,44`；云端 `voyager_server/.../user_service.go:155-283` |
| 改密三步 | `/api/user/v1/reset_password/send｜verify｜reset` — App `.../api_config.dart:50-56`；云端 `voyager_server/internal/helix/handler/user.go:89-206` |
| 找回密码三步（免鉴权组） | `/api/user/v1/forgot-password/send｜verify｜reset` — App `.../api_config.dart:61-67`；路由 `voyager_server/.../noauth.go:28-31`；实现 `voyager_server/internal/helix/handler/user.go:360-471` |
| 注销账号 | `DELETE /api/user/v1/` — App `.../api_config.dart:112`；云端 `voyager_server/internal/helix/handler/user.go:473-490` |
| 推送设备注册 | `POST`、`PUT /api/notification/v1/registration` — App `.../api_config.dart:73`；云端 `voyager_server/internal/helix/handler/deviceregistration.go:23-88` |
| 实时刷新长连接 | `WSS /api/wss/v1/push` — App `client-mobile-app/lib/app/services/push/push_websocket_service.dart:25`；云端 `voyager_server/.../wss.go:29-167`；`voyager_server/internal/helix/handler/client_app.go:213-305` |
| 用户路由文件里那段是注释块（所以浅扫找不到登录 / 找回密码） | `voyager_server/.../user.go:35-39` |
| 示意图地址按船型和部位生成；船型归一化；可按客户组织覆盖总布置图 | `voyager_server/.../inspection.go:2386,2810-2837,2727-2745,2787-2817` |
| FCM / APNs 凭证从配置中心动态拉取 | `voyager_server/internal/helix/handler/pusher.go:57-59,82,158` |
| 极光推送已停用，只留空占位字段 | `client-mobile-app/lib/app/services/push/push_token_manager.dart:159-164` |
| 提醒邮件收件人解析与邮箱为空跳过 | `voyager_server/internal/helix/app/backend/cronjob/handler/reminderemail/job.go:130-137,173,182-189`；`.../user_email_resolver.go:20-22` |
| 邮件船只范围受授权约束；保存配置时逐条校验 | `voyager_server/internal/helix/handler/reminder.go:130-158,162-190` |
| 退订链接 30 天有效；退订落库；免鉴权退订入口 | `voyager_server/.../reminder.go:1671-1694,1696-1751`；`voyager_server/internal/helix/app/gateway/biz/router/infra/external.go:11-19` |
| 邮件正文附 AM 联系人与邮箱 | `voyager_server/.../reminder.go:1108-1128` |

### A5. 端到端流程（对应第 5 章）

| 文档中的说法 | 代码位置 |
|---|---|
| 审核通过 → 写站内信 + 发推送 | `voyager_server/.../report/service/inspection_tools.go:2426-2529` |
| 点推送 → 冷启动等首页 → 跳报告详情 | `client-mobile-app/lib/app/services/push/push_notification_handler.dart:172-217,338-493` |
| 洗船建议推送 | `voyager_server/.../recommend_cleaning.go:217-261` |
| 确认清洗落库 + 飞书卡片 | `voyager_server/.../cleaning_decision.go:146-159,183-260` |
| 不自动推进状态机 | `voyager_server/.../cleaning_decision.go:130` |
| 发布 → 置标记 + PDF 任务幂等入队 | `voyager_server/internal/helix/handler/report_published_hook.go:40-71` |
| 禁用 → 写标记（保留 7 天）→ 下次请求被拦 → 启用清标记 | `voyager_server/internal/library/token/token.go:82-91,110-119`；触发 `voyager_server/internal/logic/app/customer.go:209`；拦截 `voyager_server/.../middleware.go:589-636` |
| Redis 故障放行 | `voyager_server/.../middleware.go:617-622` |
| 找回密码：6 位码 / 10 分钟 / 邮件 | `voyager_server/internal/helix/handler/user.go:377-385` |
| 校验步骤不消费验证码 | `voyager_server/.../user.go:140-143` |
| 设密码成功后才删验证码 | `voyager_server/.../user.go:436-439` |
| 有效期内 Resend 拿同一个码 | `voyager_server/.../user.go:70-87` |
| 「Didn't get code」帮助页 4 条建议 | `client-mobile-app/lib/app/modules/didnt_get_code/views/didnt_get_code_view.dart`；文案 `client-mobile-app/lib/config/translations/en_US/en_us_translation.dart:302-310` |

### A6. 待确认清单（对应第 6 章，编号一致）

| 待确认条目 | 代码位置 |
|---|---|
| 1 确认清洗不推进状态机 | `voyager_server/internal/helix/handler/internal/report/service/cleaning_decision.go:130-174` |
| 2 两套评级算法并存 | `voyager_server/.../inspection_progress_detail.go:89-151`；`voyager_server/.../inspection_tools.go:3833` |
| 3 按钮条件多三条 | `voyager_server/.../cleaning_decision.go:22,45-77`；`.../recommend_cleaning.go:158-173`；`voyager_server/.../inspection.go:2687-2688` |
| 4 清洗决策权在早期口径中未提 | `voyager_server/.../recommend_cleaning.go:158-173` |
| 5 History 90 天 / 靠泊下限 2026-05-01 | `voyager_server/.../history.go:89-93`；`.../inspection_report_service.go:20` |
| 6 清洗报告无权限校验、会创建默认文档 | `voyager_server/internal/helix/handler/internal/report/service/clean.go:81-206` |
| 7 N0 视频报告无权限校验、跨出动返回 | `voyager_server/internal/helix/handler/n0_inspection_report.go:79-116` |
| 8 确认清洗不校验出动归属 | `voyager_server/.../cleaning_decision.go:132-174` |
| 9 自助注销只软删、不写失效标记 | `voyager_server/internal/helix/handler/user.go:473-490` vs `voyager_server/internal/library/token/token.go:82-91` |
| 10 Redis 故障时放行 | `voyager_server/.../middleware.go:617-622` |
| 11 生产包环境切换默认开 + 连点 7 次调试面 | `client-mobile-app/lib/config/env/app_env.dart:73`；`client-mobile-app/lib/app/modules/about/controllers/about_controller.dart:242-291` |
| 12 版本检查不可用 | `voyager_server/internal/helix/handler/client_app.go:307-312`；`client-mobile-app/.../about_controller.dart:182-199,208` |
| 13 长连接默认关闭 + 事件推送被注释 | `client-mobile-app/.../push_websocket_service.dart:38`；`voyager_server/.../inspection.go:4600-4631` |
| 14 报告发布不发推送 | `voyager_server/internal/helix/handler/mobi.go:111-114`；`.../report_published_hook.go:40-51` |
| 15 视频播放器只能播放 / 暂停 | `client-mobile-app/lib/app/modules/inspection_detail/widgets/inspection_video_report_body.dart:790-886` |
| 16 油漆颜色注释与实现不一致 | `client-mobile-app/lib/utils/constants.dart:42-59` |
| 17 两处硬编码中文文案 | `client-mobile-app/lib/app/modules/login/controllers/login_container_controller.dart:461`；`client-mobile-app/lib/app/data/models/n0_inspection_video_report_model.dart:186-190` |
| 18 葡语无翻译资源 / 零引用安哥拉银行数据 / 清洗报告接口 App 未调用 | `client-mobile-app/lib/config/translations/localization_service.dart:30-34,52-56`；`client-mobile-app/lib/app/data/models/angola_bank.dart`；`client-mobile-app/lib/config/api_config.dart`（无对应常量） |

---

*本文档基于 2026 年 7 月 `client-mobile-app`（App 端）与 `voyager_server`（云端）两个仓库的代码现状撰写。产品仍在快速迭代，如发现与系统实际不符，以系统为准并请更新本文。相关文档：《产品线依赖地图》（跨产品线边界）、《运营后台产品说明文档》（内部侧对应能力）。*

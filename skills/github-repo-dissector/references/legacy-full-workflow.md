---
name: github-repo-dissector
description: Use when the user shares a GitHub repository URL, owner/repo, or asks to understand, analyze, dissect, compare, run, learn, install, use, evaluate, or find trending/growing GitHub projects.
---

# GitHub Repo Dissector

## Overview

把 GitHub 仓库拆成用户真正能用的判断：它是什么、怎么用、怎么跑、值不值得看、为什么最近火、背后代表什么 AI/工程范式、能不能转成公众号素材。默认面向 Codex 实操，不只复述 README。

核心四件事：

1. **Understand**：讲清楚项目解决什么问题，给谁用。
2. **Visualize**：优先做成好看的 HTML 可视化报告；Markdown 场景才用 Mermaid 辅助说明。
3. **Evaluate**：判断热度、维护、风险、安装门槛和真实落地边界。
4. **Learn/Use**：给普通用户或初学者一条可执行的下载、安装、学习、试跑路径。

## Non-Negotiable Rules

- **先读再说**：必须先读取 README、repo metadata、release/docs/关键文件。不要编文件名、目录、命令、指标。
- **路径必须存在**：图里、解释里、代码引用里的文件/目录必须来自仓库或官方文档；不确定就说“未确认”。
- **事实带来源**：可写进文章或决策的事实要标来源：README、docs、release、issue、PR、commit、demo 页面、GitHub API。
- **未实测不夸大**：没本地跑过，就写“README 声称/项目设计目标/需要实测确认”，不写“稳定可用/生产可用”。
- **指标不脑补**：star、fork、issue、contributors、release、commit 频率只能用当前可访问数据；拿不到就写“无法获取实时指标”。
- **新手优先**：用普通人能懂的话解释，技术词首次出现要翻译成工作动作。
- **控制范围**：深度分析只抓 5-10 个核心抽象，不试图文档化每个文件。
- **合法合规**：遇到网络代理、爬虫、浏览器自动化、安全工具等仓库，只讲合规用途、安装与风险，不提供规避平台规则、绕过限制或违法使用指导。

## Intent Router

先判断用户到底要哪种输出，不要每次都套完整长模板。

| 用户意图 | 典型说法 | 输出模式 |
|---|---|---|
| 默认仓库测试 | 用户只给 GitHub URL、owner/repo、“测试一下”“看一下这个仓库” | Quick HTML Snapshot |
| 只要口头理解 | “不用 HTML”“只口头说说”“这是干嘛的” | Quick Scan |
| 快速 HTML 拆解 | “快速拆解成 HTML”“简短 HTML 报告”“快速 HTML 报告” | Quick HTML Snapshot |
| 下载使用 | “下载后怎么用”“怎么安装”“普通人怎么用” | Usage Guide |
| 本地试跑 | “克隆试跑一次”“跑起来看看” | Trial Run |
| 深度拆解 | “详细介绍”“架构讲透”“学习这个项目” | Deep Analysis |
| HTML 可视化报告 | “生成报告”“可视化报告”“HTML 展示”“像截图那样”“好看的报告” | HTML Visual Report |
| 热点趋势 | “最近增长快的 AI 仓库”“GitHub 热点” | Trend Watch |
| 公众号素材 | “给 AI应用实战派PRO”“公众号角度” | Writing Material |
| 简历复盘 | “整理成简历能力证据卡” | Evidence Card |

如果用户只给一个 GitHub 仓库，或说“测试一下/看一下这个仓库”，默认输出 **Quick HTML Snapshot**：先做低成本取证，再生成一版短 HTML 分享页。只有用户明确说“不要 HTML/只口头说说”时，才退回 Quick Scan。只有用户要求“深度/详细/学习/架构/公众号素材/试跑/完整报告”时，才升级到 Deep Analysis、Trial Run 或完整 HTML Visual Report。

如果用户要求“可视化”但没有明确格式，优先理解为 **HTML Visual Report**，不要只输出 Mermaid 图。

## Speed Defaults & Clone Gate

默认把用户的“看一下这个仓库 / 测试一下这个仓库 / 这个项目有什么”理解为 **Quick HTML Snapshot 的低成本取证阶段**，先跑极速扫描，不 clone：

```powershell
python scripts/github_repo_stats.py https://github.com/owner/repo --fast
```

默认只取这些低成本证据：GitHub metadata、README 前 3 段、README 徽章/目录、root contents、release metadata、官方截图/banner。正常应在数秒到十几秒内完成，然后生成一页式 HTML 分享页。

只有出现下面任一触发条件才 clone：

- 用户明确说“克隆 / 试跑 / 本地跑起来 / 安装运行 / 看源码架构 / 生成完整 HTML 报告”。
- README/API 不足以判断项目是什么、怎么用、风险在哪里。
- 需要验证真实目录、入口文件、脚本、demo、样例输出。
- 需要对代码类仓库做 Deep Analysis，且必须引用真实文件路径。

clone 也要默认浅克隆：

```powershell
git clone --depth 1 <repo-url>
```

增长趋势也不是默认动作。Quick Scan 只写当前 stars/forks/issues 和“实时增长未确认”；只有用户问“增长趋势/最近涨得快/热点仓库”时，才扫 stargazers 或 Trending。

## Run Worthiness Gate

任何“要不要试跑”的仓库，先输出试跑决策，不要直接安装或 clone。

如果这个仓库来自 `github-content-radar` 的候选、试用队列、创作者来源或趋势源，完成快拆、试跑、安装验证、拒绝或观察结论后，要把结果回写到该 Skill 的：

```text
references/social-repo-trial-outcomes.md
```

回写只记录事实：做了什么、是否跑通、成本、风险、后续建议。不要把未实测仓库写成“可用”。

### Gate 1：值不值得跑

只用低成本证据判断：

- 项目是否解决真实痛点，而不是只有概念描述。
- README 是否提供明确 quick start、requirements、demo、截图或 benchmark。
- 最近是否仍在维护：latest release、pushed_at、open issues、README 更新。
- 安装是否可逆：是否有 uninstall、uninit、配置回滚说明。
- 是否会改系统配置、Agent 配置、PATH、浏览器、代理、数据库、云资源。
- 是否需要 API key、付费模型、GPU、大模型权重、Docker、管理员权限。

输出：

```markdown
## 试跑决策
- 是否值得跑：
- 值得跑的原因：
- 暂不跑的原因：
- 最小安全试跑方式：
- 是否需要 clone：
- clone 谁：
- 会写入哪里：
- 可回滚方式：
```

### Gate 2：是否需要 clone

默认答案是“不 clone”。只有下面情况才 clone：

- 要运行的是 GitHub 仓库源码本身，而不是 npm/pip/release 提供的已发布包。
- 工具必须读取本地项目文件，例如代码索引、静态分析、构建、测试、生成报告。
- 用户要求验证目录结构、入口文件、真实 demo、样例输出。
- README/API/release 信息不足，必须看源码确认安装和风险。

不需要 clone 的典型情况：

- 项目提供 npm/pip/binary/release，一条命令即可运行。
- 只需要看它是什么、怎么用、是否值得关注。
- 只需要 `--help`、`--version`、`install --print-config` 这类非侵入式烟测。
- 要测试的是工具能力，但可以用本地临时小项目作为目标。

### Gate 3：安全试跑顺序

按侵入性从低到高执行：

1. `--help` / `--version` / `npm view` / release metadata。
2. 只打印配置或 dry-run，例如 `install --print-config`。
3. 在临时目录或一次性小项目里试跑，不碰用户真实项目。
4. 在用户指定项目里运行初始化或索引。
5. 最后才全局安装、写 Agent 配置、改 PATH、启动服务。

每一步都要记录耗时、写入文件、是否可回滚。只要某一步已经足够回答用户问题，就不要继续加重。

## Shareable Lean Mode

当用户说“给别人分享 / 演示 / 快速体验 / 不要搞复杂 / 别跑太久 / 别人照着用”时，进入 **Shareable Lean Mode**。

目标不是把仓库研究透，而是让别人看到一个低门槛、可复现、不会吓人的流程。默认控制在 5-10 分钟内完成；超过时间预算就停下来汇报，不继续加码。

### 必做

1. 一句话说明工具解决什么问题。
2. 判断是否需要 clone；默认不 clone。
3. 只选一种安装方式，优先 npm/pip/release，不比较所有安装路线。
4. 只做一个版本验证：`--version` 或 `--help` 二选一。
5. 只做一个最小 smoke test：临时小项目或用户指定项目，二选一。
6. 输出“别人照着做”的 3-5 步流程。
7. 明确回滚命令。

### 默认跳过

- 多轮 `--help` 命令。
- 同时测试 npm、release、源码 clone、多种安装路径。
- 大段 README/文档全文读取。
- stargazer 增长趋势扫描。
- clone 源码仓库，除非工具必须从源码运行。
- 浏览器截图、复杂 HTML 可视化、深度目录树、竞品对比。
- 额外的 callers/callees/context 多轮查询；smoke test 只验证一个查询即可。
- 重新读取完整 HTML 配色手册；使用已有模板即可。

### 轻量 HTML 报告

如果 Shareable Lean Mode 下仍需要 HTML，默认做 **一页式分享报告**：

1. 工具是什么。
2. 为什么值得试。
3. 安装命令。
4. 最小验证命令。
5. 写入了哪里。
6. 回滚命令。
7. 适合谁 / 不适合谁。

不要做完整仓库可视化报告，除非用户明确要求“详细报告/公众号素材/完整可视化”。

### 快速 HTML 视觉规则

快速拆解的 HTML 也必须好看，但要短。目标是 **1 个首屏 Hero + 3-5 个信息区块 + 1 个结论区**，不要做 10 节以上的完整报告。

视觉要求：

- 配色必须先调用 `html-color-system` 的 Preferred Palette Queue，不要临时凭感觉选色。
- 默认按这个权重自动选择：`warm-sand-editorial` > `forest-warm-gray` > `black-gold-premium` > `ink-gray` > `sunset-coral` > `dark-tech` > `smoky-mauve`。
- 如果用户没有指定配色，GitHub 快拆/深拆报告默认使用 `warm-sand-editorial`。它最适合公众号/分享页/项目解释类报告。
- 当仓库是知识库、工作流、本地优先、隐私、安全、效率工具、教程文档时，可自动切到 `forest-warm-gray`。
- 当报告是高价值对比、商业决策、管理汇报、深度结论型内容时，可自动切到 `black-gold-premium`，但必须先保证可读性。
- 当仓库偏代码分析、开发工具、数据/技术报告、较严肃的中性内容时，可自动切到 `ink-gray`。
- 当仓库偏图像、视频、AIGC、创意营销、视觉素材时，可自动切到 `sunset-coral`，但不要做高饱和橙红冲撞。
- 当仓库偏 dashboard、监控、infra、代码智能、数据密集时，可自动切到 `dark-tech`。
- `smoky-mauve` 只作为低优先级备选：除非用户明确喜欢烟紫/灰粉/lookbook 气质，否则不默认使用。
- 先确定主色调，再选渐变色；不要随机渐变。
- 渐变色必须从主色相邻色展开，色相跨度建议 20-45 度，最多不超过 60 度。
- 页面可以浅色、清爽，但不能寡淡；整个页面画布（`body` 或最外层容器）也要有主题渐变，不要只让中间卡片渐变、两侧留白纯白。
- 主题渐变可以比普通浅蓝白更重一档：用蓝/青/蓝灰的中低饱和相邻色叠加径向光斑、线性渐变和阴影，避免灰白空白感。
- 按已选主题色做视觉锚点，例如全页渐变背景、浅渐变 Hero、柔和 KPI、侧边色块、强调分割线；不要让所有仓库都回到蓝青模板。
- 仍然遵守 `html-color-system`：所有颜色、阴影、圆角、间距、字号、渐变都必须定义在 `:root` 变量中。
- 渐变要“切换主题颜色”：不同仓库类型可以换主色，但默认避免紫粉感；AI/设计/图片类也先按主题队列判断，不默认品红紫，也不固定默认蓝青。
- 避免大红大绿、高对比互补色硬撞、彩虹渐变；丰富感来自同色系深浅、相邻色、透明叠层和阴影。
- 面向分享的 HTML 页面不要展示内部过程信息：不要把 `Quick HTML Snapshot`、耗时、`未 clone`、`GitHub API`、取证方式这类字样放到页面首屏或正文；这些只在最终回复里说明。
- 面向读者的 HTML 页面不要展示给 agent/内部模板看的解释，例如“这份报告如何组织”“可视化策略”“数据图表只是辅助判断”“单仓库/双仓库/三仓库展示规则”等。除非用户要求沉淀方法论，否则这些内容只放在最终回复或内部交接卡。
- 页面文案尽量中文化。保留真实仓库名、URL、文件名、命令、包名；但 UI 标签、section 标题、KPI 名称、说明卡片尽量用中文，例如“关注度倍数”“复用转化率”“仓库类型”“下一步动作”“适合谁看”。
- 首屏右侧信息卡要放项目判断或读者关心的内容，不放“可视化策略/报告方法”。常用卡片：`主判断`、`适合谁看`、`最低成本怎么试`、`不要夸大的地方`。
- 结论区必须写项目结论和下一步，而不是评价报告本身。不要出现“这一版更适合正式报告”之类的模板自评。
- 附录可以直接展开，不必折叠。附录只放读者可能不懂但有助理解的概念，例如“什么是技能包/提示词模板库”“为什么高 star 不等于可用”；不要放我们内部的版式决策说明。

### GitHub Report Palette Mapping

当用户只说“测试一下/快速拆解/生成 HTML 报告”时，按仓库类型自动选配色：

| 仓库类型 | 默认主题 | 备选主题 | 说明 |
|---|---|---|---|
| 技能包 / 提示词模板库 / AI 工作流 | `warm-sand-editorial` | `forest-warm-gray` | 重点是经验复用和普通人理解，优先温暖、稳重、可读 |
| 教程文档 / 案例仓库 / 课程资料 | `warm-sand-editorial` | `ink-gray` | 适合文章化、学习路线和结构化拆解 |
| 内容库 / 素材库 / Prompt 库 / awesome 清单 | `warm-sand-editorial` | `sunset-coral` | 如果内容偏创意、图片、视频，再切珊瑚 |
| 图像 / 视频 / AIGC / 视觉创意工具 | `sunset-coral` | `warm-sand-editorial` | 需要更有传播感，但仍要柔和低冲突 |
| CLI / 开发工具 / 代码分析 / MCP / 插件 | `ink-gray` | `forest-warm-gray` | 默认中性技术感，避免太营销 |
| 数据 / dashboard / 监控 / infra | `dark-tech` | `ink-gray` | 适合深色科技感或中性数据报告 |
| 商业决策 / 高端对比 / 管理报告 | `black-gold-premium` | `warm-sand-editorial` | 适合结论型、对比型，但要严格检查对比度 |
| 隐私 / 本地优先 / 安全 / 稳定性工具 | `forest-warm-gray` | `ink-gray` | 给人可信、低噪音、可持续的感觉 |

如果类型不确定，先用 `warm-sand-editorial`，不要默认蓝紫。

### Palette Fixes To Preserve

- 非蓝色主题的深色区域光晕必须跟随自身主色调，不能残留蓝青光晕。
- `forest-warm-gray` 的正文辅助色应使用暖灰，例如 `hsl(45, 8%, 34%)`，避免绿上绿发糊。
- `smoky-mauve` 的主渐变应在紫到粉之间增加中间停靠点，避免中段变脏。
- `warm-sand-editorial` 的数字渐变保持同一暖色族，例如棕橙到金橙，不跨到黄绿色。
- 深色和黑金主题里，外部白底图表要加深色框、padding、混合模式或文字 fallback，避免白底 SVG 刺眼。
- 所有主题都要让卡片背景有极浅方向性渐变，不用纯白卡片。
- 关键数字可用渐变文字，但仓库名不要用容易裁掉 `g/y/p/q` 的渐变裁字方案。

### Current Preferred Theme Ranking

用户当前偏好排序如下，后续 GitHub HTML 报告优先按这个顺序自动选：

1. 暖砂米色：默认首选。
2. 森绿暖灰：知识/流程/本地优先/专业报告优先。
3. 黑金：高级、商业、深色对比场景优先，但需要可读性复查。
4. 水墨灰：中性、技术、稳重。
5. 日落珊瑚：创意、视觉、传播感。
6. 深色模式：数据、dashboard、技术监控。
7. 烟紫灰粉：低优先级，仅在用户偏好时使用。

旧版主题色只作为次级参考；优先使用上面的 `GitHub Report Palette Mapping` 和 `Current Preferred Theme Ranking`：

| 仓库/内容类型 | 主色 | 渐变方向 |
|---|---|---|
| AI Agent / 技能包 / 工作流 | 暖砂 / 森绿 | 暖砂 → 橄榄 / 森绿 → 暖灰 |
| 代码理解 / 开发工具 / MCP | 水墨灰 / 深色科技 | 石墨灰 → 青灰 / 深蓝灰 → 青 |
| 设计 / 图像 / 创意工具 | 日落珊瑚 / 暖砂 | 珊瑚 → 橙金 / 暖砂 → 低饱和橙 |
| 视频 / 多媒体 / AIGC | 日落珊瑚 / 水墨灰 | 珊瑚 → 玫瑰灰 / 石墨 → 青灰 |
| 数据 / BI / 仓库分析 | 水墨灰 / 深色科技 | 青灰 → 石墨 / 深蓝灰 → 青 |
| 效率 / 办公 / 自动化 | 森绿暖灰 / 暖砂 | 森绿 → 橄榄 / 暖砂 → 绿灰 |
| 安全 / 隐私 / 本地优先 | 森绿暖灰 / 水墨灰 | 森绿 → 暖灰 / 石墨 → 青灰 |
| 金融 / 商业 / 管理报告 | 黑金 / 暖砂 | 黑金 → 琥珀 / 暖砂 → 金橙 |

快速 HTML 默认结构：

```markdown
1. Hero：仓库名 + 完整仓库地址 URL + 仓库简介 + 视觉截图/README 图 + 4 个 KPI
2. 它是什么：3 张短卡片
3. 为什么值得看：痛点 / 热点 / 转发理由
4. 怎么最低成本试：只给最轻路径
5. 不要夸大：3-4 个边界
6. 结论：适合谁 + 下一步
```

### 时间预算

| 任务 | 预算 | 超时处理 |
|---|---:|---|
| Quick Scan | 30 秒 | 停止深挖，给当前结论 |
| 安装或版本验证 | 2 分钟 | 记录卡点，不切换多条安装路线 |
| 最小 smoke test | 1 分钟 | 只保留一个失败样例和下一步 |
| 快速 HTML Snapshot | 5 分钟 | 只做一页短报告，不加深度章节 |
| 一页式分享 HTML | 5 分钟 | 先给 Markdown 版，再决定是否补 HTML |
| 完整 HTML 报告 | 15 分钟 | 需要用户明确授权 |

### 耗时任务黑名单

除非用户明确要求，不主动执行：

- clone 大仓库或多仓库。
- 安装完整依赖、构建源码、运行测试套件。
- 扫 stargazers 历史增长。
- 读取完整 docs/site/README 长文并逐节总结。
- 多工具重复验证同一件事。
- 生成长篇 HTML 后再多轮视觉返工。

## Type-First Triage

任何仓库分析先做 **30 秒仓库类型判定**，再决定后续动作。不要一上来 clone、扫 stargazers、读全仓库。

低成本分类信号：仓库名、GitHub description、topics、primary language、release/asset、README 前 3 段、README 徽章和目录标题。

| 仓库类型 | 判断信号 | 默认要做 | 默认跳过 |
|---|---|---|---|
| 代码应用/AI 工具 | 有 `src/`、`api/`、`web/`、`pyproject/package`，README 讲运行 | README、manifest、入口文件、核心目录 | 完整 clone、完整趋势，除非深度报告 |
| 桌面应用/安装包 | release 有 Windows/macOS/Linux 包，README 讲下载 | release、安装步骤、配置、截图 | 源码架构，除非用户问开发 |
| 教程/文档/课程 | docs/book/course/tutorial 为主，代码少 | 内容结构、适合谁、学习路线 | 运行、架构图、依赖分析 |
| 图库/提示词/素材库 | gallery/prompts/images/assets，内容展示为主 | 分类、来源、授权、可用场景 | 代码架构深挖，除非有生成脚本 |
| awesome/list/资源导航 | README 列表为主 | 内容质量、分类、维护频率、选题价值 | 本地试跑、架构图 |
| 模型/推理项目 | model/checkpoint/inference/eval | 模型用途、依赖、显存、demo、限制 | 普通安装包逻辑 |
| 数据集/语料库 | dataset/corpus/benchmark/data | 数据来源、字段、许可、下载方式 | 应用试跑 |
| 插件/连接器 | plugin/extension/MCP/connector | 支持平台、安装接入、权限风险 | 普通 Web 应用流程 |
| 模板/脚手架 | template/boilerplate/starter | 使用方式、技术栈、改造成本 | 社区热点长分析 |
| 基础设施/部署工具 | docker/k8s/terraform/deploy | 部署路径、权限、网络、安全边界 | 面向普通用户的功能体验 |

输出中必须写明“仓库类型”和“分类依据”。如果不确定，写“暂定类型”，不要让错误分类带偏后续分析。

### 仓库简介写法

仓库简介固定用 **使用方式 + 内容形态**，让普通人 10 秒内判断它是什么。不要写抽象句子如“这是一个强大的开源项目”。

```text
这是一个[使用方式]的[内容形态]。
```

在 HTML 报告里，必须高亮 `[内容形态]` 这一段，例如把 `教程文档 / 案例仓库`、`素材库 / Prompt 库`、`npm 库 / Mermaid 渲染工具` 包成醒目的 badge/span。不要只高亮“这是一个”或整句话。

常用“使用方式”：

- 可以直接用：资料、模板、prompt、清单、图库、脚本入口已经明确，读者不需要完整部署。
- 需要本地运行：需要 clone、安装依赖、执行命令或启动服务。
- 需要接入到 Agent/平台：需要 Claude Code、Codex CLI、MCP、浏览器插件、VS Code、飞书等宿主。
- 需要私有化部署：需要 Docker、数据库、服务端、环境变量或云资源。
- 主要供学习参考：教程、论文复现、案例、课程、架构样例。

常用“内容形态”：

- 素材库 / Prompt 库
- AI Agent Skill / 插件 / MCP 工具
- CLI 工具 / 桌面应用 / Web 应用
- 模板 / 脚手架 / 自动化工作流
- 教程文档 / awesome 清单 / 数据集 / 模型项目

例子：

- “这是一个可以直接用的素材库 / Prompt 库。”
- “这是一个需要接入到 Agent 的电商生图 Skill / Prompt 模板库。”
- “这是一个需要本地运行的 CLI 工具 / 代码分析项目。”
- “这是一个主要供学习参考的教程文档 / 案例仓库。”

## Information Gathering

优先按这个顺序取证：

1. GitHub API 或 GitHub 页面：description、topics、stars、forks、open issues、license、language、created/updated/pushed、latest release、仓库类型初判。
2. README 前 3 段和目录：定位、类型、截图、demo、quick start、限制。
3. 根据仓库类型决定是否继续读取 docs/examples/demo、dependency manifest、目录树、入口文件、issues/PR/discussions。
4. 只有深度拆解、试跑、架构必须精确、或 README/API 信息不足时，才浅克隆。

可用脚本：

```powershell
python scripts/github_repo_stats.py https://github.com/owner/repo
```

极速模式：

```powershell
python scripts/github_repo_stats.py https://github.com/owner/repo --fast
```

趋势热点：

```powershell
python scripts/github_repo_stats.py --trending --since daily --limit 10 --max-star-pages 3
```

## Rate Limit Fallback

GitHub API 限流时按这个降级：

1. 先用 GitHub 网页、release 页面、raw README、官方 docs。
2. Trending 候选可用 GitHub Trending HTML。
3. 增长数字拿不到时不要硬算，写“实时增长无法确认”。
4. 只把脚本输出的 `lower_bound` 写成“至少/样本内/下限”，不能写完整增长。
5. 如果 repo 页面都打不开，要求用户贴 README、目录树或关键文件。

## Output Modes

### 1. Quick Scan

用于“看下这个仓库有什么”。控制在短而有判断。

```markdown
## 快速判断
- 仓库：
- 一句话：
- 适合谁：
- 它解决的真实问题：
- 当前热度/维护信号：
- 怎么开始：
- 主要风险/坑：
- 是否值得继续看：
```

### 1.5 Quick HTML Snapshot

用于“快速拆解成 HTML / 简短 HTML 报告”。这是 Quick Scan 的 HTML 版本，不是完整分析报告。

必须控制：

- 不 clone。
- 不扫完整趋势。
- 不做源码架构。
- 不超过 6 个主区块。
- 不做长证据表，最多 1 个简短事实表。
- 视觉要比普通卡片丰富：全页渐变背景、浅色主题 Hero、相邻色渐变、KPI 强化、结论卡；Hero 必须出现完整仓库地址 URL；不要在页面里显示耗时、未 clone、API 来源等内部过程信息。

输出文件命名：

```text
YYYY-MM-DD_owner_repo_快速拆解分享页.html
```

### 2. Usage Guide

用于“下载后怎么用/怎么安装”。优先给普通用户可执行步骤。

```markdown
## 下载后怎么用
1. 下载哪个版本：
2. 安装后第一步：
3. 必须准备什么配置/API Key/账号/订阅/模型：
4. 最小可用流程：
5. 常用模式怎么选：
6. 验证是否成功：
7. 常见问题：
8. 安全/隐私/合规提醒：
```

规则：

- 不要把开发者源码安装流程当普通用户流程，除非用户问“自建/源码运行”。
- 如果 release 有多平台安装包，按用户系统优先说明；不知道系统时先给 Windows/macOS/Linux 选择规则。
- 如果软件本身不提供服务，只是客户端，要明确说明还需要配置、订阅、API key、模型或后端。

### 3. Trial Run

用于“克隆试跑一次”。实际执行前先读 README/install docs。

```markdown
## 本地试跑记录
- 环境：
- 克隆方式：
- 依赖安装：
- 启动命令：
- 本地访问地址：
- 是否成功：
- 报错和处理：
- 截图/可观察结果：
- 试跑结论：
- 后续实测建议：
```

执行原则：

- 优先浅克隆：`git clone --depth 1 <repo-url>`。
- 不运行明显危险脚本；需要密钥、付费 API、系统级权限、网络代理、驱动、内核扩展时先说明风险。
- 前端/本地服务跑起来后，用浏览器或截图验证，不只看命令输出。

### 4. HTML Visual Report

用于“可视化报告/HTML 报告/好看的展示报告”。这是仓库分析的首选可视化形式，Mermaid 只作为报告内部的小型辅助图，不是最终交付物。

必须创建一个可本地打开的 `.html` 文件，并遵守 `html-color-system`：

- 所有颜色、阴影、圆角、间距、字号都通过 `:root` CSS 变量定义。
- 报告使用“总分总”结构：开头总览，中间分模块拆解，结尾给结论和下一步。
- 第一屏必须是仓库简介仪表盘，类似报告封面，而不是流程图。
- 默认中文报告的 section 小标题使用中文，例如 `01 · 总览判断`，不要擅自改成英文；只有用户明确要求英文时才英文。
- 首屏至少包含：仓库名、完整仓库地址 URL、owner/repo、stars、forks、open issues、增长趋势、项目类型、是否代码类/内容类/工具类、license、更新时间、一句话判断。
- 总览页必须有“仓库类型”KPI 或显眼标签，例如：代码应用、安装包、教程文档、图库素材、awesome 清单、模型、数据集、插件、模板、基础设施。优先使用作者/官方描述和 GitHub topics；如果是推断，要标注“暂定”。
- 仓库名必须单行自适应：长名称要缩小字号或使用 `fitText` JS，完整显示在一行内；不能只用 `overflow:hidden` 截断，也不允许换行把首屏撑爆；报告标题另起一行，用较小字号。
- 仓库名不要用容易裁掉 descender 的 `background-clip:text + color:transparent` 方案；如果出现 `g/y/p/q` 下沿被切掉，立刻改为实色 `color: var(...)`，并加足 `line-height` 与 `padding-bottom`。
- 首屏字体要服务信息密度，不要把 repo 名做成海报级超大字；优先保证一屏内能看到核心 KPI。
- 趋势图默认轻量：快速报告优先最近 7 天；如果 stargazer 扫描慢、限流、或 30 天覆盖度是 `lower_bound`，只展示 7 天趋势。只有在 30 天数据已完整或无需额外 API 请求时，才展示 30 天趋势，并按约 5 天间隔抽样（如 1/5/10/15/20/25/30 天）而不是铺满 30 行。
- 中段按仓库类型展示，不要硬套架构：
  - 代码类：系统架构、目录结构、入口文件、运行方式、依赖关系。
  - 工具/客户端类：下载版本、安装路径、核心配置、使用流程、常见坑。
  - 内容/awesome/list/dataset 类：改名为 **Content Pipeline Visualization**，展示内容来源、审核、生成、发布、分类、版权边界。
  - 模型/数据类：数据来源、训练/推理路径、评测指标、使用限制。
- 视觉组件优先用 HTML/CSS 卡片、KPI、时间线、流程带、分层面板、矩阵表、风险标签；不要把 Mermaid 当主视觉。
- HTML 报告仍应提供一个“可复制 Mermaid 小图”作为辅助，便于用户放进 Markdown/飞书/公众号二次加工，但不能让 Mermaid 成为唯一可视化。
- 必须包含文件树/目录概览，至少展示 top 2-3 层关键目录及用途。
- 必须包含相似项目/竞品/形态对比；没有直接竞品时，用“同类形态对比”，并说明不是完整市场对标。
- 必须说明增长趋势方法论：API/Trending/Star History 来源、扫描页数、覆盖度、`complete` 或 `lower_bound`、为什么选 7 天或 30 天；如果是 7 天图，要明确这是为了速度和可信覆盖，不是因为 30 天没有价值。
- 如果使用图表，可以用原生 HTML/CSS 或 ECharts，但必须能在本地打开；外链 CDN 不稳定时要提供无 JS 降级内容。
- 移动端必须可读，宽表格要横向滚动。

推荐 HTML 结构：

```markdown
1. Hero Overview：仓库封面 + 核心指标卡 + 一句话结论
2. Executive Summary：值不值得看、解决什么问题、适合谁
3. Repository Type Map：代码类/内容类/工具类/模型类定位
4. Main Breakdown：按类型拆解架构或内容管线
5. File Tree：关键目录/文件概览
6. Portable Diagram：可复制 Mermaid 小图
7. Evidence Board：README/docs/release/issue/API 事实表
8. Comparison：相似项目/同类形态对比
9. Risk & Adoption：安装门槛、API key、成本、隐私、合规、维护风险
10. Final Verdict：总结判断 + 下一步动作
```

HTML 报告命名建议：

```text
YYYY-MM-DD_owner_repo_仓库可视化分析报告.html
```

### 5. Deep Analysis

用于“详细介绍/架构/学习”。合并用户给的 Deep Analyzer 思路，但适配中文和 Codex。

````markdown
# [Repo Name] — 深度分析

> 一句话总结

## 1. 项目身份
- One-line summary：
- 解决的问题：
- 目标用户：
- 技术栈：
- 项目类型：
- 和相似项目的区别：

## 2. 架构可视化 / 内容管线可视化
### 2.1 系统架构图
```mermaid
graph TB
```

### 2.2 核心数据/调用流程
```mermaid
sequenceDiagram
```

### 2.3 目录地图
```mermaid
graph LR
```

## 3. 社区健康度
| 指标 | 值 | 信号 |
|---|---:|---|

### 健康度判断

### 增长趋势判断

## 4. 新手学习路线
### 核心概念总览
### Chapter 1-N

## 5. Quick Start

## 6. 资源与下一步
````

深度分析必须遵守：

- Mermaid 图节点要能映射到真实目录/文件；节点标签里标路径或模块名。
- 系统架构图最多 10 个节点；sequenceDiagram 最多 6 个参与者。
- 非代码/内容型仓库不要写“系统架构图”，改写为“内容管线可视化”或“资源结构图”。
- 学习章节抓 5-10 个核心抽象，每章包含：是什么、为什么重要、在哪里、和谁连接、可以怎么试。
- 代码片段最多 10 行；必须来自真实文件，并给文件路径。

### 6. Trend Watch

用于“最近增长快的 AI 仓库/GitHub 热点”。

流程：

1. 先用 GitHub Trending 候选，不要全网乱搜。
2. 用脚本对少量候选算 7d/30d stargazers 增长。
3. API 限流时保留 Trending 当日/本周 stars 文案，并标注实时增长不可确认。
4. 输出时按“值得深挖程度”而不是纯 star 排序。

输出：

```markdown
## GitHub 热点速览
| 仓库 | 今日/本周热度 | 增长判断 | 它是干嘛的 | 为什么值得看 |

## 最值得深挖的 3-5 个

## 这批项目背后的趋势

## 数据边界
```

### 7. Writing Material

用于公众号素材。固定输出板块：

```markdown
## 公众号素材摘取：给 AI 应用实战派 Pro

### 1. 这个仓库一句话值不值得看
### 2. 选题价值判断
### 3. 普通人怎么理解它
### 4. 最适合文章开头展示的东西
### 5. 可以直接写进文章的事实
| 可写事实 | 来源 | 可用于文章哪里 |
|---|---|---|
### 6. 这个仓库真正解决的问题
### 7. 值得展开的 3 个角度
### 8. 读者最可能踩的坑
### 9. 配图建议
### 10. 给公众号主对话的提醒
```

公众号判断：

- 热点追踪：star 突增、刚发布、被公司/社区提到、有时间节点。
- 工具实测：能本地跑、有 demo、有输入输出、有截图空间。
- 避坑分析：issue/docs 里集中出现安装、依赖、key、成本、隐私问题。
- 案例拆解：README/docs 有清楚 workflow，可迁移到公司、电商、内容或客服。
- 趋势判断：背后代表 Prompt -> Agent -> Workflow -> Skill/MCP/Memory/CLI/Code Graph 的范式变化。

### 8. Evidence Card

用于“简历能力证据卡”。只基于本对话或本次真实操作，不编造上线、规模、ROI。

输出：

```markdown
## 简历能力证据卡
1. 项目/任务一句话
2. 业务场景归类
3. 原始问题拆解
4. 实际操作顺序
5. 使用工具和技术
6. 岗位 JD 能力对标
7. 可量化成果
8. 可写进简历的项目经历
9. STAR 面试版本
10. 风险和需隐藏信息
11. 给主对话的总结
```

## Community Health Framework

能取到数据时使用；取不到就跳过，不要编。

| 指标 | 健康 | 警告 | 红旗 |
|---|---|---|---|
| 最近 commit | 3 个月内 | 3-12 个月 | 超过 12 个月 |
| open issues 比例 | 低于 30% | 30%-60% | 高于 60% |
| contributors | 多于 5 | 2-5 | 1 |
| release | 规律 | 零散 | 12 个月无 release |
| issue 响应 | 1 周内 | 1-4 周 | 超过 1 个月 |
| docs | 完整 | 基础 | 缺失 |

判断要写成“信号”，不要写成绝对结论。高 star 但长期不维护，也要提示风险。

## Growth Trend

脚本支持：

```powershell
# 单仓库快筛：默认优先覆盖 7 天趋势，速度更快
python scripts/github_repo_stats.py https://github.com/owner/repo --max-star-pages 8 --trend-days 7

# 单仓库极速/限流安全：跳过 stargazers 时间戳和热门 issue 搜索，只取基础指标和仓库类型初判
python scripts/github_repo_stats.py https://github.com/owner/repo --fast

# 单仓库深挖：需要 30 天趋势时再打开，可能更慢
python scripts/github_repo_stats.py https://github.com/owner/repo --max-star-pages 20 --trend-days 30

# 小仓库完整 stargazers，慢
python scripts/github_repo_stats.py https://github.com/owner/repo --full-stars

# Trending 优先
python scripts/github_repo_stats.py --trending --since daily --limit 10 --max-star-pages 3
```

趋势写法：

- 好：`脚本抽取最近 N 页 stargazers，7 天内新增至少 X star，覆盖度 lower_bound。`
- 好：`Trending 页面显示今日新增 X stars，但实时 stargazer 明细因限流无法确认。`
- HTML 报告默认：`7d` 趋势优先，因为最快且最容易完整覆盖。
- HTML 报告可选：`30d` 趋势只有在完整覆盖或无需额外请求时展示；展示时按约 5 天间隔抽样（如 1/5/10/15/20/25/30 天），并明确标注 `complete` 或 `lower_bound`。
- 如果 GitHub API 限流或用户明显在意速度，先用 `--fast` 生成基础报告，把增长趋势写成“实时增长暂未确认”，不要让 stargazers 分页或 issue 搜索阻塞整份报告。
- 不为了画 30 天趋势额外跑大量分页导致报告变慢；热点筛选优先速度，深度分析再补完整趋势。单仓库快筛建议 `--max-star-pages 8`，Trending 批量筛选建议 `--max-star-pages 3`。
- 速度优先时不要默认 `git clone`。先用 GitHub API/raw README 获取身份、指标、README、关键文件；只有用户要求试跑、深度架构、文件树必须精确、或 raw 内容不够时，才浅克隆。
- 坏：`全网爆火/碾压同类/必火`。

## External Accelerators

这些只能辅助理解，事实仍回原始来源验证：

| 工具 | 用法 | 适合 |
|---|---|---|
| DeepWiki | `github.com/owner/repo` 改 `deepwiki.com/owner/repo` | 快速看结构化文档/架构图 |
| GitIngest | `gitingest.com` | 仓库转长文本 |
| GitHub1s | `github.com` 改 `github1s.com` | 在线 VS Code 看结构 |
| Sourcegraph | 搜 repo | 查符号引用 |
| OctoLinker | 浏览器插件 | GitHub 依赖跳转 |
| Repo Visualizer | Action/现成图 | 结构可视化 |

## Language-Specific Entry Hints

- Python：看 `pyproject.toml`、`setup.py`、`requirements.txt`、`src/`、`__init__.py`。
- JavaScript/TypeScript：看 `package.json` scripts、`src/index.*`、`app.*`、`vite/next/electron/tauri` 配置。
- Go：看 `go.mod`、`cmd/`、`internal/`。
- Rust：看 `Cargo.toml`、`src/main.rs`、`src/lib.rs`。
- Java：看 `pom.xml`、`build.gradle`、`src/main/java/`。
- Desktop apps：看 release 安装包、Tauri/Electron 配置、系统依赖。
- Non-code repos：跳过架构代码分析，改做内容结构、资源质量、维护情况、使用路径。

## Error Handling

| 问题 | 处理 |
|---|---|
| 私有/不可访问 | 说明无法访问，请用户贴 README/目录/关键文件 |
| 空仓库 | 只分析现有内容，标为 minimal content |
| 超大仓库 | 聚焦 `src/` 或主包，说明范围限制 |
| monorepo | 先识别 packages，必要时问用户聚焦哪个模块 |
| 找不到入口 | 列候选入口，不硬猜 |
| 无 README | 作为健康度红旗，从代码/manifest 尽力分析 |
| API 限流 | 跳过实时指标，标注 unavailable |
| 需要密钥/付费 API | 不假装已跑通，说明配置需求 |

## Common Mistakes

- 只复述 README 功能列表，不提真实痛点和主要矛盾。
- 把 README 愿景、benchmark、宣传语当成实测结果。
- 用 star 制造价值判断，但没看 release、issue、commit、docs。
- 用户问“怎么用”，却输出公众号素材长文。
- 用户问“详细架构”，却没有读目录和入口文件。
- Mermaid 图里出现不存在的模块或虚构数据流。
- 用户要“可视化报告/HTML报告”时，只给 Mermaid 或 Markdown，缺少可打开的 HTML 仪表盘。
- HTML 报告首屏没有仓库总览 KPI，直接进入流程图或长文字。
- HTML 报告首屏 repo 名过大、换行、溢出，导致 KPI 不在第一屏。
- HTML 小修时重新跑完整仓库分析、趋势扫描或重写整份报告；应优先定位具体选择器/局部 HTML，快速补丁验证。
- HTML 标题用渐变裁字导致 `g/y/p/q` 等字母下沿被切掉。
- 中文报告里把 section 小标题改成英文，造成风格不一致。
- 趋势图没有说明数据来源和扫描方法，让用户无法判断可信度。
- 内容型仓库缺少文件树、相似形态对比和可复制 Mermaid 辅助图。
- 忽略 API Key、模型成本、安装权限、隐私合规、平台规则这些真实坑。
## Screenshot Short Card Mode

Use this mode when the user says the article works better with screenshots, asks for short repo breakdowns, or wants several GitHub repos shown as separate HTML cards.

Goal: create screenshot-friendly repo cards, not full reports.

Rules:

- One repo per HTML file.
- Each repo should use a different palette/layout when multiple cards are made in the same batch.
- Do not show author/account labels.
- Do not show internal process labels such as screening logic, writing plan, Quick HTML, API collection method, elapsed time, or clone status.
- Keep the copy short enough to understand from the screenshot alone.
- Default card content:

```markdown
仓库名
一句话判断
它解决什么
适合谁
先怎么试
GitHub URL
```

For roundup articles, prefer 4 concise repo cards over one long HTML report. If the card screenshot communicates the repo value better than prose, let the screenshot carry the explanation and keep the article text short.

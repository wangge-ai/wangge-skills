---
name: beginner-tutorial-writer
description: 从产品名与官方资料生成可操作的新手教程，配搜索查询脚本和独立 HTML 渲染脚本。
license: MIT
metadata:
  version: 1.2.0
  author: Wangge
  tags:
  - tutorial
  - writing
  - research
  - chinese
  - beginner
  trigger_keywords:
  - 新手教程
  - 保姆级教程
  - 产品教程
  - 教程生成
  - tutorial-writer
  source_pack: '13'
---

# Beginner Tutorial Writer · Skill 说明

## 1. 目标

输入一个产品名（中文 / 英文皆可），自动产出一份 **5000–10000 字** 的中文 Markdown 教程和一份可直接打开的 **HTML 教程报告**，
面向完全没用过该产品的小白，覆盖：

注册 → 下载安装 → 首次配置 → 配置 API → 功能介绍 → Skill / 插件用法（含创建）
→ 集成接入 → 经典玩法案例 → 进阶技巧 → 常见问题 FAQ → 资源汇总

## 2. 输入参数

| 参数               | 类型     | 必填 | 默认                        | 说明                                                                  |
| ---------------- | ------ | -- | ------------------------- | ------------------------------------------------------------------- |
| `product_name`   | string | ✅  | —                         | 产品名称，如 `WorkBuddy`                                                  |
| `vendor`         | string | ⬜  | 由 Agent 自动检索              | 出品方 / 厂商，如 `腾讯`                                                     |
| `language`       | string | ⬜  | `zh-CN`                   | 输出语言，目前主推中文                                                         |
| `target_words`   | int    | ⬜  | `7000`                    | 目标字数（中文字符），建议 5000–10000                                            |
| `output_dir`     | string | ⬜  | `output/`                 | 输出目录                                                                |
| `source_weights` | object | ⬜  | 见 `templates/search-config.yaml` | 各平台搜索权重，自定义时合计建议 = 100                                              |
| `html_report`    | bool   | ⬜  | `true`                    | 是否自动生成独立 HTML 教程报告；默认生成                                             |
| `skip_publish`   | bool   | ⬜  | `true`                    | 是否跳过自动发布（默认只生成文件，不发布）                                               |

### 触发示例

```
/beginner-tutorial-writer product_name=WorkBuddy vendor=腾讯
/beginner-tutorial-writer product_name=Coze
/beginner-tutorial-writer product_name=Dify target_words=8000 html_report=true
/beginner-tutorial-writer product_name=Notion source_weights='{"wechat":40,"youtube":20,"official":20,"reddit":10,"github":10}'
```

只填 `product_name` 即可全自动跑。其它参数全部走默认。

## 3. 默认搜索源权重

未指定 `source_weights` 时，使用 `templates/search-config.yaml` 中的默认配置：

| 来源              | 默认权重 | 说明                            |
| --------------- | ---- | ----------------------------- |
| 微信公众号           | 30   | 国产 SaaS 教程主阵地，最高权重           |
| 知乎              | 15   | 用户实战 + 长文                    |
| 腾讯云开发者社区 / CSDN | 15   | 技术教程沉淀                       |
| 官方文档 / 官网       | 15   | 权威性来源，用于校准事实                  |
| B 站             | 10   | 视频教程 + 截图要点                  |
| 小红书             | 5    | 小白视角的实战截图                    |
| GitHub / Issues | 5    | 涉及 SDK / Skill 时使用            |
| 其它              | 5    | 博客园、少数派、即刻、掘金等                |

> 权重含义：用于决定**调用搜索 API 时各来源的查询次数比例**，以及最终引用条目的目标占比。
> 不是硬性配额，遇到信息缺口时 Agent 可自动加大某个来源的检索量。

## 4. 固化的工作流（Agent 必须严格按此执行）

### Step 0 · 前置检查
- 解析输入参数，缺失 `product_name` 即报错退出
- 加载 `templates/search-config.yaml`，与用户传入的 `source_weights` 合并
- 加载 `templates/outline.md`（章节骨架）和 `templates/style-guide.md`（写作风格）
- 在 `output_dir` 下创建空文件：`{product_name}完整教程.md`，写入目录骨架
- 记录 HTML 输出路径：`{product_name}完整教程.html`

### Step 1 · 资料检索（按权重并行）
按 `source_weights` 比例发起多组搜索查询。每个来源都跑下列关键词组合：

```
{product_name} 教程
{product_name} {vendor}
{product_name} 注册 安装
{product_name} API 配置
{product_name} 使用技巧
{product_name} 公众号           ← 用于发现公众号引流文章
{product_name} 保姆级
{product_name} 实战 案例
{product_name} 避坑 踩坑
{product_name} 进阶 高阶
{product_name} skill / 插件 / Bot / 工作流
```

工具优先级：`WebSearch` → `WebFetch` 兜底。WorkBuddy 支持多平台搜索和网页抓取。

### Step 2 · 真实性校验（关键安全阀）
搜索结果汇总后判断：
- 如果 `{product_name}` 在权威来源（官方 + 至少 2 个独立技术社区）都搜不到 → **立即停下来**，向用户反馈"未找到该产品，请确认名称是否正确"，不要编造
- 如果搜到的是同名其他产品 → 反馈分歧，请用户澄清

### Step 3 · 精读 Top 3-5 篇正文
对相关度最高的 3–5 篇文章使用 `WebFetch` 拉全文。

### Step 4 · 事实交叉验证
建立一张"事实表"，每条事实标注：值 + 至少 2 个独立来源 + 发布日期。
出现冲突时：列出分歧，标注"以官方文档为准"。

### Step 5 · 按骨架填章节
按 `templates/outline.md` 的 10 章 + 附录，**逐节使用 Edit 工具填充**，不要一次性 Write 大文件。
每章末尾必须有"一句话总结"或"操作清单"。

### Step 6 · 自查
- 字数是否落在 `target_words ± 20%`
- 是否每章都填了
- 引用来源是否 ≥ 6 篇且标注出处
- 是否有 `[占位]` 未替换
- API Key / Secret 是否全部用 `xxx` 占位
- 如果 `html_report=true`，运行 `scripts/build-tutorial-html.py` 生成独立 HTML 报告
- HTML 报告必须能离线打开，包含首屏视觉锚点、目录、正文、代码块、表格层级、移动端适配；原始 HTML 必须被转义，不能把 Markdown 里的 `<script>` 当脚本执行
- HTML 报告默认使用暖色编辑教程版式，避免旧的蓝白系统后台感排版；不要回退到 `--bg: #f6f7fb` / `--paper: #ffffff` 这类纯系统文档配色

### Step 7 · 交付
- 使用 `present_files` 把成品 Markdown 展示给用户
- 同时交付本地 HTML 报告路径（默认：`{product_name}完整教程.html`）
- 输出一段简短摘要：覆盖了哪几章 / 总字数 / 用了几个来源 / 是否生成 HTML 报告
- **如果 `skip_publish=false`**：再询问是否继续生成公众号内联版或其它发布格式。独立 HTML 报告不等于公众号内联 HTML。

## 5. 内容骨架

详见 `templates/outline.md`，固定 10 章 + 附录：

```
第 0 章 · 一句话认识 {产品名}
第 1 章 · 注册账号 & 领新人福利
第 2 章 · 下载与安装（覆盖所有支持的平台）
第 3 章 · 首次启动 & 基础设置
第 4 章 · 配置 API（内置模型 + 自定义模型）
第 5 章 · 功能全景：每个模块讲清楚
第 6 章 · {核心扩展机制} 详解：用法 + 如何创建
第 7 章 · 集成与外部接入
第 8 章 · N 个经典玩法（照抄就能用）
第 9 章 · 进阶使用技巧 & 省钱攻略
第 10 章 · 常见问题 FAQ & 避坑指南
附录 · 资源汇总 & 参考来源
```

## 6. 写作风格（详见 `templates/style-guide.md`）

- 中文 · 口语化 · "你"称呼读者
- 每段 ≤ 4 行
- 多用：**加粗** / 列表 / 表格 / 代码块 / emoji（🎯 💡 ⚠️ ✅ ❌ 📌）
- 每个技术词第一次出现时**用人话解释一句**
- 截图位置用 `[截图：xxx]` 占位
- 章节间用 `---` 分隔

## 7. 安全与合规

- **不要编造**：不确定的事实标注"待官方确认"，宁缺勿编
- API Key 示例全用 `YOUR_API_KEY` 占位
- 引用第三方文章必须给出处链接
- 不抓取需要登录 / 付费墙后的内容
- 涉及个人微信号 / 手机号等 PII，必须脱敏

## 8. 辅助脚本

`scripts/build-search-queries.py` —— 输入产品名 + 权重，输出按比例分配好的搜索查询任务清单（JSON）。
Agent 可以直接消费这份清单去并行调度搜索 API。

`scripts/build-tutorial-html.py` —— 输入 Markdown 教程，输出一个无外部依赖的独立 HTML 报告，适合本地预览、交付、打包分享。

用法：
```bash
python3 scripts/build-search-queries.py --product "WorkBuddy" --vendor "腾讯"
python3 scripts/build-search-queries.py --product "Coze" --weights '{"wechat":50,"bilibili":20,"official":30}'
python3 scripts/build-tutorial-html.py --input output/WorkBuddy完整教程.md --output output/WorkBuddy完整教程.html --title "WorkBuddy 完整教程"
```

## 9. 失败回退

- 搜索 API 全挂 → 切到 `WebFetch` + 已知官方 URL 直抓
- 仍无法获取足够资料 → 反馈用户"信息不足，建议提供官网链接或资料源"
- 不要在缺资料时硬写，宁可让用户补充

## 10. 输出样例

参见同级目录下 `templates/example-output.md`（节选自 WorkBuddy 教程，作为风格参考）。

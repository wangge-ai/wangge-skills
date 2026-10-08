---
name: ecom-product-assets-collector
description: Use when 用户提供淘宝天猫、京东、拼多多商品链接或保存的 HTML，需要采集商品主图、副图、详情页长图、证书、检测报告或成分表图片，并保留来源、状态和失败原因。
license: MIT
---

# 商品主图与详情图采集

## 核心原则

使用包内 `scripts/collect_product_assets.py` 完成确定性采集。工作台实时链接使用 `--use-current-browser` 复用当前可见浏览器中的已有登录态，再由 Python 完成图片分类、下载和 manifest；不会再打开另一套 Playwright 浏览器窗口。独立命令行和保存 HTML 仍保留 Playwright 路线。遇到登录、验证码或风险确认时，只等待使用者在可见浏览器中处理，不绕过平台限制。

## 能做什么

- 从淘宝/天猫、京东、拼多多商品链接识别并下载主图和详情图。
- 从使用者保存的可见页面 HTML 继续整理图片。
- 将主图与详情图分别保存到 `main/`、`detail/`。
- 生成 `manifest.json`、`manifest.csv` 和 `summary.md`，记录图片来源、状态、尺寸、哈希、失败原因和本次耗时。

不负责抓取评价、问大家、店铺后台数据、订单、结算价或隐藏接口。需要榜单/搜索前排样本时使用 `ecom-ranking-main-image-collector`；需要页面事实和竞品分析时使用 `ecommerce-competitor-analyzer`。

## 实时平台与登录门槛

- 实时采集前必须由用户明确选择当前链接所属的平台；每次只采一个平台，不默认扩展为“全平台”。
- `--html-file` 本地保存页面不要求平台登录；只分析保存时实际保留的可见内容和本地资源。
- 对实时 `--url`，启动业务采集前先做最小业务可用性预检：在任务自有标签打开目标商品页，立即核对当前 URL、平台域名、标题和正文。用户未登录或不愿登录时，说明主图、详情图和动态素材可能无法完整获取。
- 用户已经确认登录准备后，不能只因首页没有昵称、个人中心或订单入口就判定未登录；目标商品页可访问且没有明确登录/验证墙时继续采集，并如实记录身份是否可见。
- 标签页指针、当前 URL 或平台域名不一致属于线路错误，不属于登录失败；重新导航并复核，仍错位时切换已授权线路或写 `failed/not_available`。
- 只有目标商品页明确出现登录、扫码、验证码、滑块或风控时才直接返回 `waiting_login`，不得先运行脚本等待 60 秒或抓取登录页。
- 预检通过后若采集中出现重新登录、验证码或风控，停止当前平台并保留 manifest 阻塞状态，等待用户处理后用新的独立输出目录重跑。
- 工作台要求当前浏览器连接可用；连接未建立时返回 `not_available`，不静默回退到新的 Playwright 窗口。
- 不索要账号、密码、Cookie 或 Token，不自动登录，不绕过验证码或风控。
- 不要保存登录页、动态二维码、手机号或账号输入框截图；登录是否通过只记录业务页可访问状态。

## 运行前检查

先运行：

```powershell
python scripts\collect_product_assets.py --help
```

工作台当前浏览器路线不需要 Playwright 浏览器运行文件。只有独立命令行或保存 HTML 路线提示缺少 Playwright 时，使用者才需安装：

```powershell
pip install playwright
playwright install chromium
```

安装包不会携带分享者的浏览器资料、Cookie 或账号状态。

## 采集商品链接

工作台或已经连接 WebBridge 的当前浏览器：

```powershell
python scripts\collect_product_assets.py `
  --url "https://item.jd.com/商品ID.html" `
  --use-current-browser `
  --output ".\outputs\product-assets"
```

该路线在当前浏览器中新建任务标签页，读取页面可见图片后直接下载，不复制 Cookie、Token 或账号资料，也不关闭使用者标签页。页面要求登录或验证时返回 `waiting_login`；浏览器连接不可用时返回 `not_available`。

不加 `--use-current-browser` 的独立命令行仍会打开单独的可见 Chromium，只适合明确需要独立采集资料目录的场景。

无头模式只适合公开页面或自动化测试：

```powershell
python scripts\collect_product_assets.py `
  --url "https://example.com/product" `
  --platform generic `
  --headless `
  --output ".\outputs\product-assets"
```

## 处理保存的 HTML

```powershell
python scripts\collect_product_assets.py `
  --html-file ".\saved-pages\product.html" `
  --platform tmall `
  --output ".\outputs\product-assets"
```

保存 HTML 时应同时保留页面引用的本地资源；只保存空壳 HTML 不能恢复动态加载图片。

## 结果状态

| 状态 | 含义 |
| --- | --- |
| `completed` | 至少成功下载一张主图或详情图，仍需核对是否完整。 |
| `partial` | 页面能打开，但没有得到足够可用图片。 |
| `waiting_login` | 需要使用者登录、验证码或风险确认。 |
| `not_available` | 当前浏览器连接不可用，且没有打开备用窗口。 |
| `failed` | 依赖、网络、页面结构或下载步骤失败。 |

有效主图与详情图均为 0 时，不得仅因页面或进程可运行而写 `partial`；应按真实原因使用 `waiting_login`、`needs_input` 或 `failed`。

完成后必须核对：

1. `main/` 和 `detail/` 中是否为当前商品图片，而不是推荐、评价或店铺图标。
2. `manifest.json` 中每条记录是否有 `source_url`、`status` 和失败原因。
3. `summary.md` 的下载数量、耗时和状态是否与文件夹一致。
4. 详情页明显缺段时，报告“本次可见范围”，不要写“完整详情页已采集”。

## 工作台事实与状态门

- 不得由模型手工计算汇总数字；主图、详情图、失败项和跳过项只按 manifest 和实际文件计数。
- 工作台确定性质量门以 manifest 和实际文件、商品身份、最终 URL 与页面状态决定 `success / partial / waiting_login / not_available / failed`；进程退出正常不能覆盖业务状态。
- 当本 Skill 的图片作为市场分析样本证据时，在上游 `collection_evidence_manifest.json` 登记对应原始文件和样本编号，不把登录页、推荐图或诊断截图计为商品证据。
- 公开报告不得出现内部工具名称、调试过程或模型思索过程。

## 平台边界

- 淘宝/天猫、京东、拼多多页面结构和风控会变化，当前脚本不能保证每个链接都成功。
- 抖音电商和小红书商品页尚未纳入此脚本，不得写成已支持。
- 脚本不使用反检测参数，不解验证码，不导出账号凭据。
- 实时平台是否成功必须以本次 `manifest` 和实际图片为准；本地 HTML 夹具通过不等于实时平台通过。

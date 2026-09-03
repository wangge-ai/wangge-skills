# E-commerce Main Image Diagnosis

一个面向中国电商主图、搜索结果卡片和商品页截图的 Agent Skill。

它不只判断图片“好不好看”，而是检查目标买家能否快速看懂商品、感知利益、建立信任，并获得比相邻竞品更明确的点击理由。

## 适用场景

- 淘宝、天猫、京东、拼多多、抖音、小红书、1688 等平台
- 单张主图或 1–5 张商品图
- 搜索结果页、商品页或广告截图
- 竞品图片对比
- 主图改版、设计师 brief、AI 图片提示词
- CTR 问题排查与 A/B 测试计划

## 输出内容

- 证据范围与缺失信息
- 购买决策和平台场景判断
- 识别、利益、信任、差异、焦点与平台适配诊断
- 立即修改、下一轮测试和后续重建建议
- 按需生成设计 brief、AI 图片提示词或图片序列规划

这个 Skill 不会仅凭图片承诺 CTR 提升，也不会把看不到的后台数据当成事实。

## 安装

先克隆总仓库，再复制这个 Skill 目录：

```bash
git clone https://github.com/wangge-ai/wangge-skills.git
cp -R wangge-skills/skills/ecom-main-image-diagnosis ~/.agents/skills/ecom-main-image-diagnosis
```

也可以复制到项目级的 `.agents/skills/` 或对应 Agent 的 Skills 目录。

## 使用示例

```text
请诊断这张淘宝主图：先说明你实际看到了什么，再给出最值得优先修改的三点。
```

```text
比较这组搜索结果截图里的竞品主图，给我的产品做三个单变量 A/B 测试方向。
```

## 目录

- `SKILL.md`：核心判断与执行流程
- `references/`：输入路由、诊断框架、平台说明和输出格式
- `examples/`：脱敏示例报告
- `agents/openai.yaml`：Codex 展示信息

## 开源协议

[MIT](LICENSE)

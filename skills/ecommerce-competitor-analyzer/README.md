# E-commerce Competitor Analyzer

一个基于商品链接、表格、截图、保存页面和评论证据进行电商竞品分析的 Agent Skill。

它会先盘点证据和字段，再决定能做价格带、卖点、规格、评论 VOC、关键词还是页面表达分析。商品链接只是线索，不会被自动写成实时销量、完整评论或全市场数据。

## 适用输入

- 商品列表 CSV/JSON
- 竞品清单与历史快照
- 商品页、搜索结果页或评价截图
- 保存的公开 HTML
- 用户已经收集并授权分析的评论摘要

## 自带脚本

```bash
python scripts/analyze_ecommerce_dataset.py \
  --input products.csv \
  --out dataset-report.md \
  --category "收纳盒"
```

```bash
python scripts/analyze_competitors.py \
  --input competitors.csv \
  --out competitor-report.md \
  --json-out competitor-facts.json \
  --category "收纳盒"
```

```bash
python scripts/render_report_html.py \
  --input competitor-report.md \
  --out competitor-report.html
```

`probe_product_links.py` 只检查公开可达链接。它不会自动登录，不索要账号、密码、Cookie 或 Token，也不会绕过验证码、风控或付费接口。

## 安装

仓库发布后，可以克隆到 Agent 的 Skills 目录：

```bash
git clone https://github.com/wangge-ai/ecommerce-competitor-analyzer.git ~/.agents/skills/ecommerce-competitor-analyzer
```

也可以复制到项目级的 `.agents/skills/` 或对应 Agent 的 Skills 目录。

## 使用示例

```text
分析这份竞品 CSV：先说明样本和字段边界，再比较价格、卖点、店铺和可验证的机会。
```

```text
根据这些商品页截图做竞品对比，把观察事实、样本推断、运营建议和未知项分开。
```

## 验证

```bash
python -m unittest discover -s tests -v
```

当前测试覆盖事实来源、未知字段、广告与自然样本分母，以及登录和平台覆盖边界。

## 开源协议

[MIT](LICENSE)


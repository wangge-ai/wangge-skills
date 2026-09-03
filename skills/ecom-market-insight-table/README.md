# E-commerce Market Insight Table

一个把电商商品列表 Excel/CSV 转成可核对市场洞察的 Agent Skill。

它先生成确定性的样本事实，再让 Agent 判断价格带、店铺集中度、标题词根、卖点拥挤度和首轮测试动作。有限样本不会被写成全市场结论。

## 适用输入

- 平台、插件或内部系统导出的商品列表
- 人工整理的 CSV/XLSX
- 至少包含商品标题，并尽量提供价格、销量或评价量、店铺、品牌、类目、采集时间和排序口径

本 Skill 不负责登录平台、处理验证码或自动抓取数据。

## 标准输出

- `market_table_profile.json`：基础统计画像
- `market_table_profile.md`：人工可读摘要
- `market_facts.json`：带稳定证据编号的事实合同
- `market_decision.json`：引用事实编号的运营判断
- `market-insight-report.html`：完整可分享报告

## 确定性脚本

```bash
python scripts/profile_market_table.py \
  --input products.csv \
  --out-dir output \
  --category "收纳盒" \
  --source-note "平台、采集时间、关键词和排序口径"
```

```bash
python scripts/render_market_html_report.py \
  --profile output/market_table_profile.json \
  --facts output/market_facts.json \
  --decision output/market_decision.json \
  --out output/market-insight-report.html
```

CSV 路径使用 Python 标准库；读取 XLSX 时需要 `openpyxl`。

## 安装

仓库发布后，可以克隆到 Agent 的 Skills 目录：

```bash
git clone https://github.com/wangge-ai/ecom-market-insight-table.git ~/.agents/skills/ecom-market-insight-table
```

也可以复制到项目级的 `.agents/skills/` 或对应 Agent 的 Skills 目录。

## 使用示例

```text
分析这份商品列表，先说明样本边界，再判断价格带、店铺集中度、标题词根和最值得测试的细分机会。
```

## 验证

```bash
python -m unittest discover -s tests -v
```

当前测试覆盖事实报告渲染、编排报告结构和工作台事实一致性。正式分析仍需检查用户输入的真实字段与业务口径。

## 开源协议

[MIT](LICENSE)


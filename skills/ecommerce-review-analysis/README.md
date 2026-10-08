# 电商评价分析

按数据质量、清洗、分类、人群、归因、参照物与报告七步分析评论。

## 快速使用

从仓库复制 `skills/ecommerce-review-analysis` 整个目录到目标 Agent 的 Skills 目录，再给出实际输入和所需交付物。支持标准 SKILL.md 的环境可阅读此包；各平台的安装位置及工具能力以其官方说明为准。

```text
请用 $ecommerce-review-analysis，根据我提供的资料完成电商评价分析。
先说明输入范围和缺失信息，结论保留原始证据。
```

## 内容与依赖

- [SKILL.md](SKILL.md)：实际执行方法。
- [references/](references/)：配套方法与模板。
- [scripts/](scripts/)：配套脚本。

完整工作流由 Agent 执行；分类骨架 CLI 支持 CSV（标准库）和 XLSX（openpyxl）。骨架不自动完成全部七步。

## 来源与验证范围

来源是旺哥此前在 [飞书资料库](https://my.feishu.cn/wiki/DJMRwTyK2ifkkmk5FHPcZeP3nwc?table=tbl1SvuqTb3Vmeq4&view=vew95iuRuH) 分享的第 19 个资料包；配套 [原文章](https://mp.weixin.qq.com/s/aGtkFdsdwUofWVF1vlTGvg)。本次公开的是方法、必要参考和源码，原始压缩包、安装程序、账户配置及业务数据留在资料库。

2026-10-08 完成安装结构、引用文件、常见凭证和本机路径检查；包含脚本的包还执行帮助命令及最小样例。结构检查不证明模型分析质量；ChatLab、飞书及商业 MCP 集成需用户自己的环境，本次未在其真实业务账户上重跑。

本包原创内容采用 [MIT](LICENSE)。外部工具、服务与平台的许可和账户权限由其提供方管理，本包不授予第三方服务使用权。

## 分类骨架 CLI

```bash
python scripts/analyze_reviews_skeleton.py --input reviews.csv --output-dir output --text-column 评论内容
python scripts/analyze_reviews_skeleton.py --input reviews.xlsx --output-dir output --text-column 初评内容
```

CSV 无需第三方包；XLSX 先运行 `python -m pip install -r requirements.txt`。结果为保留原列的 `classified-reviews.csv` 和统计 `summary.json`。长编号以文本保存；输入 XLSX 已丢失的数字精度无法恢复。

默认词表是儿童牙膏示范，换品类须提供 `--lexicon lexicon.json`，可覆盖 `MAIN_CATS`、`POS_WORDS`、`NEG_WORDS`、`MIX_WORDS`、`PRIORITY`。脚本只完成分类及母表合并；清洗、人群、归因、参照物和完整报告仍按 Skill 执行。完整分析如使用 pandas、matplotlib，需另装所用库。

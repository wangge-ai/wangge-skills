# 工具新手完整教程

从产品名与官方资料生成可操作的新手教程，配搜索查询脚本和独立 HTML 渲染脚本。

## 快速使用

从仓库复制 `skills/beginner-tutorial-writer` 整个目录到目标 Agent 的 Skills 目录，再给出实际输入和所需交付物。支持标准 SKILL.md 的环境可阅读此包；各平台的安装位置及工具能力以其官方说明为准。

```text
请用 $beginner-tutorial-writer，根据我提供的资料完成工具新手完整教程。
先说明输入范围和缺失信息，结论保留原始证据。
```

## 内容与依赖

- [SKILL.md](SKILL.md)：实际执行方法。
- [scripts/](scripts/)：配套脚本。
- [templates/](templates/)：配套方法与模板。

Python 3.10+；查询清单脚本需要 PyYAML，HTML 渲染脚本仅用标准库。

## 来源与验证范围

来源是旺哥此前在 [飞书资料库](https://my.feishu.cn/wiki/DJMRwTyK2ifkkmk5FHPcZeP3nwc?table=tbl1SvuqTb3Vmeq4&view=vew95iuRuH) 分享的第 13 个资料包；配套 [原文章](https://mp.weixin.qq.com/s/wSZVr9HcvR4R0VY-PVfJZA)。本次公开的是方法、必要参考和源码，原始压缩包、安装程序、账户配置及业务数据留在资料库。

2026-10-08 完成安装结构、引用文件、常见凭证和本机路径检查；包含脚本的包还执行帮助命令及最小样例。结构检查不证明模型分析质量；ChatLab、飞书及商业 MCP 集成需用户自己的环境，本次未在其真实业务账户上重跑。

本包原创内容采用 [MIT](LICENSE)。外部工具、服务与平台的许可和账户权限由其提供方管理，本包不授予第三方服务使用权。

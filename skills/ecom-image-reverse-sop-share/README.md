# 电商图片拆解与反推提示词

把产品图和竞品图拆成图位任务、购买疑问、画面结构及自家商品提示词。

## 快速使用

从仓库复制 `skills/ecom-image-reverse-sop-share` 整个目录到目标 Agent 的 Skills 目录，再给出实际输入和所需交付物。支持标准 SKILL.md 的环境可阅读此包；各平台的安装位置及工具能力以其官方说明为准。

```text
请用 $ecom-image-reverse-sop-share，根据我提供的资料完成电商图片拆解与反推提示词。
先说明输入范围和缺失信息，结论保留原始证据。
```

## 内容与依赖

- [SKILL.md](SKILL.md)：实际执行方法。
- [references/](references/)：配套方法与模板。

支持图片阅读的 Agent；图片生成工具按用户已有环境选用。

## 来源与验证范围

来源是旺哥此前在 [飞书资料库](https://my.feishu.cn/wiki/DJMRwTyK2ifkkmk5FHPcZeP3nwc?table=tbl1SvuqTb3Vmeq4&view=vew95iuRuH) 分享的第 3 个资料包；配套 [原文章](https://mp.weixin.qq.com/s/jgsZE5JG7xryz-iPIqNckw)。本次公开的是方法、必要参考和源码，原始压缩包、安装程序、账户配置及业务数据留在资料库。

2026-10-08 完成安装结构、引用文件、常见凭证和本机路径检查；包含脚本的包还执行帮助命令及最小样例。结构检查不证明模型分析质量；ChatLab、飞书及商业 MCP 集成需用户自己的环境，本次未在其真实业务账户上重跑。

本包原创内容采用 [MIT](LICENSE)。外部工具、服务与平台的许可和账户权限由其提供方管理，本包不授予第三方服务使用权。

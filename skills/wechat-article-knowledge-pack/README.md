# 公众号文章转知识库

把公众号文章链接或本地导出文件整理为原文档案、元数据和可追溯知识卡。

## 快速使用

从仓库复制 `skills/wechat-article-knowledge-pack` 整个目录到目标 Agent 的 Skills 目录，再给出实际输入和所需交付物。支持标准 SKILL.md 的环境可阅读此包；各平台的安装位置及工具能力以其官方说明为准。

```text
请用 $wechat-article-knowledge-pack，根据我提供的资料完成公众号文章转知识库。
先说明输入范围和缺失信息，结论保留原始证据。
```

## 内容与依赖

- [SKILL.md](SKILL.md)：实际执行方法。


本地文件读写；联网采集工具是可选依赖，遇验证页面使用已有导出文件。

## 来源与验证范围

来源是旺哥此前在 [飞书资料库](https://my.feishu.cn/wiki/DJMRwTyK2ifkkmk5FHPcZeP3nwc?table=tbl1SvuqTb3Vmeq4&view=vew95iuRuH) 分享的第 12 个资料包；配套 [原文章](https://mp.weixin.qq.com/s/FAWNzR59uVi5Al-GRDTOEA)。本次公开的是方法、必要参考和源码，原始压缩包、安装程序、账户配置及业务数据留在资料库。

2026-10-08 完成安装结构、引用文件、常见凭证和本机路径检查；包含脚本的包还执行帮助命令及最小样例。结构检查不证明模型分析质量；ChatLab、飞书及商业 MCP 集成需用户自己的环境，本次未在其真实业务账户上重跑。

本包原创内容采用 [MIT](LICENSE)。外部工具、服务与平台的许可和账户权限由其提供方管理，本包不授予第三方服务使用权。

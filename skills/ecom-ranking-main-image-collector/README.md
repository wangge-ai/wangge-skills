# 排行与搜索主图采集

从公开榜单、保存页面或导出的商品卡片整理主图样本、位置、来源、联系表和报告。

## 开始使用

将本目录完整复制到 Agent 使用的 Skills 目录，然后请求：

> 使用 $ecom-ranking-main-image-collector。从这份导出商品卡片中整理主图样本，区分广告和自然位，标明排序口径并生成报告。

详细步骤：[SKILL.md](SKILL.md)。[安装说明](../../README.md#安装)。

## 输入与依赖

Python + Pillow。实时采集需网络及用户授权的浏览器；保存页面和结构化 JSON 可离线处理。

以用户指定的项目目录保存输出。示例中的 `inputs/`、`outputs/` 是可替换位置。包内不附带业务数据、个人账号、客户端安装程序或 API 密钥。

## 随包脚本

- [build_main_image_report.py](scripts/build_main_image_report.py)：先运行 `python scripts/build_main_image_report.py --help` 查看参数。
- [build_sample_manifest.py](scripts/build_sample_manifest.py)：先运行 `python scripts/build_sample_manifest.py --help` 查看参数。
- [collect_main_images.py](scripts/collect_main_images.py)：先运行 `python scripts/collect_main_images.py --help` 查看参数。

## 参考资料

- [references/platform-public-sources.md ](references/platform-public-sources.md)

## 来源与验证边界

由维护者本地持续维护的方法整理为公开版本，包含必要脚本、参考资料或模板；已调整本机路径和默认账号名称。独立安装、文件引用、脚本入口及离线样例的验证记录见[扩充检查记录](../../docs/audits/2026-10-08-local-expansion.md)。外部服务、模型输出、真实平台采集和业务效果须在使用环境中实际验证，不能由离线样例推定。

原创方法和脚本采用 [MIT License](LICENSE)。第三方平台、工具、字体及资料仍遵循各自许可和服务条款。

下载脚本复用仓库已有的公开 HTTP 地址校验，拒绝内嵌凭证、本机/内网地址及跳转到这些地址。商品素材包的 `--allow-local-assets` 仅用于用户明确指定的回环 WebBridge 同源测试素材，默认关闭。浏览器页面自身子资源仍由浏览器权限控制，本包不是网络隔离沙箱。

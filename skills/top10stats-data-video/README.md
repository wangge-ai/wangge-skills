# 数据动态排行视频

把热点映射到可核验的数据来源与视频形态，清洗数据并制作排行、分镜、封面及 MP4。

## 开始使用

将本目录完整复制到 Agent 使用的 Skills 目录，然后请求：

> 使用 $top10stats-data-video。根据这份有来源和单位的数据规划动态排行视频，核对同口径后再制作，未实际渲染时仅交方案。

详细步骤：[SKILL.md](SKILL.md)。[安装说明](../../README.md#安装)。

## 输入与依赖

Python + pandas + numpy + Pillow + openpyxl，FFmpeg/FFprobe；在线数据来源需使用时重新核验，种子库不是现时数据。

以用户指定的项目目录保存输出。示例中的 `inputs/`、`outputs/` 是可替换位置。包内不附带业务数据、个人账号、客户端安装程序或 API 密钥。

## 随包脚本

- [hotspot_video_router.py](scripts/hotspot_video_router.py)：先运行 `python scripts/hotspot_video_router.py --help` 查看参数。
- [make_professional_data_videos.py](scripts/make_professional_data_videos.py)：先运行 `python scripts/make_professional_data_videos.py --help` 查看参数。
- [make_rank_videos.py](scripts/make_rank_videos.py)：先运行 `python scripts/make_rank_videos.py --help` 查看参数。
- [refresh_reference_tables.py](scripts/refresh_reference_tables.py)：先运行 `python scripts/refresh_reference_tables.py --help` 查看参数。

## 参考资料

- [references/TOP10stats_数据源和路由表_Excel版.xlsx ](references/TOP10stats_数据源和路由表_Excel版.xlsx)
- [references/data-sources.md ](references/data-sources.md)
- [references/hotspot-to-video-routing.csv ](references/hotspot-to-video-routing.csv)
- [references/hotspot-workflow.md ](references/hotspot-workflow.md)
- [references/official-data-source-library.csv ](references/official-data-source-library.csv)
- [references/style-teardown.md ](references/style-teardown.md)
- [references/video-form-library.md ](references/video-form-library.md)
- [references/官方专业数据源库.xlsx ](references/官方专业数据源库.xlsx)
- [references/热点到数据视频路由表.xlsx ](references/热点到数据视频路由表.xlsx)

## 来源与验证边界

由维护者本地持续维护的方法整理为公开版本，包含必要脚本、参考资料或模板；已调整本机路径和默认账号名称。独立安装、文件引用、脚本入口及离线样例的验证记录见[扩充检查记录](../../docs/audits/2026-10-08-local-expansion.md)。外部服务、模型输出、真实平台采集和业务效果须在使用环境中实际验证，不能由离线样例推定。

原创方法和脚本采用 [MIT License](LICENSE)。第三方平台、工具、字体及资料仍遵循各自许可和服务条款。

视频脚本默认输出到当前工作目录的 `outputs/data-video/`，可用环境变量 `WANGGE_VIDEO_OUTPUT` 指定目录。包内数据源是带记录日期的种子清单，使用前要重新核验。

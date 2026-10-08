# 电商视频分析与策划

从本地视频提取时长与证据索引，形成单条脚本、分镜及营销视频矩阵。

## 开始使用

将本目录完整复制到 Agent 使用的 Skills 目录，然后请求：

> 使用 $ecom-video-workflow。分析这个本地产品视频，再提出一条新脚本，区分看见的画面与尚未证实的卖点。

详细步骤：[SKILL.md](SKILL.md)。[安装说明](../../README.md#安装)。

## 输入与依赖

Python + openpyxl；提取真实时长需要 FFprobe。脚本输出证据脚手架，画面和字幕须由 Agent 实际检查。

以用户指定的项目目录保存输出。示例中的 `inputs/`、`outputs/` 是可替换位置。包内不附带业务数据、个人账号、客户端安装程序或 API 密钥。

## 随包脚本

- [analyze_video_evidence.py](scripts/analyze_video_evidence.py)：先运行 `python scripts/analyze_video_evidence.py --help` 查看参数。
- [build_planning_artifact.py](scripts/build_planning_artifact.py)：先运行 `python scripts/build_planning_artifact.py --help` 查看参数。

## 参考资料

- [references/ecom-marketing-video-planner.md ](references/ecom-marketing-video-planner.md)
- [references/ecom-video-evidence-analysis.md ](references/ecom-video-evidence-analysis.md)
- [references/ecom-video-planner.md ](references/ecom-video-planner.md)

## 来源与验证边界

由维护者本地持续维护的方法整理为公开版本，包含必要脚本、参考资料或模板；已调整本机路径和默认账号名称。独立安装、文件引用、脚本入口及离线样例的验证记录见[扩充检查记录](../../docs/audits/2026-10-08-local-expansion.md)。外部服务、模型输出、真实平台采集和业务效果须在使用环境中实际验证，不能由离线样例推定。

原创方法和脚本采用 [MIT License](LICENSE)。第三方平台、工具、字体及资料仍遵循各自许可和服务条款。

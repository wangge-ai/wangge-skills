# 视频制作总流程

组织选题、脚本、分镜、素材、音频与渲染验证，连接不同视频工具。

## 开始使用

将本目录完整复制到 Agent 使用的 Skills 目录，然后请求：

> 使用 $video-producer-core。为这个主题制作视频方案，先交脚本、分镜和素材表，说明音频与成片验证方法。

详细步骤：[SKILL.md](SKILL.md)。[安装说明](../../README.md#安装)。

## 输入与依赖

环境检查脚本适用 Windows PowerShell；成片依任务选用 FFmpeg、TTS 和渲染工具，HyperFrames/Remotion 插件另装。

以用户指定的项目目录保存输出。示例中的 `inputs/`、`outputs/` 是可替换位置。包内不附带业务数据、个人账号、客户端安装程序或 API 密钥。

## 随包脚本

- [check_video_environment.ps1](scripts/check_video_environment.ps1)：Windows PowerShell 脚本，使用前检查参数与依赖。

## 参考资料

- [references/production-template.md ](references/production-template.md)

## 来源与验证边界

由维护者本地持续维护的方法整理为公开版本，包含必要脚本、参考资料或模板；已调整本机路径和默认账号名称。独立安装、文件引用、脚本入口及离线样例的验证记录见[扩充检查记录](../../docs/audits/2026-10-08-local-expansion.md)。外部服务、模型输出、真实平台采集和业务效果须在使用环境中实际验证，不能由离线样例推定。

原创方法和脚本采用 [MIT License](LICENSE)。第三方平台、工具、字体及资料仍遵循各自许可和服务条款。

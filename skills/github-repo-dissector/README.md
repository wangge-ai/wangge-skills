# GitHub Repository Dissector

一个用于理解、评估和试跑 GitHub 仓库的 Agent Skill。

它会先回答“这是什么、怎么用、值不值得继续看”，再根据需要进入架构分析、安装试跑、增长信号或分享报告，而不是只复述 README 和 Star 数。

## 能做什么

- 快速识别仓库定位、技术栈、许可证和维护状态
- 区分项目宣称与已经验证的行为
- 按需分析目录、入口、依赖、Issue、Release 与风险
- 在隔离目录中记录真实试跑过程
- 生成适合普通读者或技术读者的结论与证据

## 安装

仓库发布后可以直接克隆到 Agent 的 Skills 目录：

```bash
git clone https://github.com/wangge-ai/github-repo-dissector.git ~/.agents/skills/github-repo-dissector
```

也可以把整个仓库复制到当前项目的 `.agents/skills/` 或对应 Agent 的 Skills 目录。

## 使用

安装并重启 Agent 会话后，直接发送仓库链接并说明目标：

```text
帮我快速看一下 https://github.com/owner/repo，它解决什么问题，值不值得试。
```

```text
深度拆解 owner/repo 的架构、安装方式和主要风险，并做一次隔离试跑。
```

## 目录

- `SKILL.md`：核心路由与工作流程
- `scripts/github_repo_stats.py`：可选的 GitHub 指标采集脚本
- `references/legacy-full-workflow.md`：需要完整报告或高级分析时读取
- `agents/openai.yaml`：Codex 中的展示信息

脚本在未设置 `GITHUB_TOKEN` 时也能使用 GitHub 公共 API，但更容易受到匿名速率限制。不要把访问令牌写进仓库。

## 开源协议

[MIT](LICENSE)

---

[旺哥开源 Skills](https://github.com/wangge-ai/wangge-skills) · [旺哥 AI 电商实战群](https://t2vq6a99kv.feishuapp.com/app/app_17a7exe7wzv/)


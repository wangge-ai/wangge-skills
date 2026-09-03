# GitHub Content Radar

一个用于发现、去重和筛选 GitHub 项目的 Agent Skill。它把仓库事实、公开传播信号、试用成本和内容价值分开记录，适合建立项目观察池、试跑队列和公众号素材卡。

## 安装

```bash
git clone https://github.com/wangge-ai/wangge-skills.git
cp -R wangge-skills/skills/github-content-radar ~/.agents/skills/github-content-radar
```

Windows PowerShell 可使用：

```powershell
Copy-Item -Recurse wangge-skills/skills/github-content-radar "$HOME/.agents/skills/github-content-radar"
```

## 行为边界

- 只把公开网页和 GitHub 数据当作候选证据；需要登录或无法访问时明确标记，不绕过访问控制。
- Star、社媒提及和作者推荐不等于真实可用，仓库入选后仍应交给 `github-repo-dissector` 做技术核验。
- 参考目录包含公开来源线索和历史试用记录，不包含账号密码、Cookie、Token 或私有浏览器数据。
- 本 Skill 没有可执行脚本，不会自行联网、下载、写入或删除文件；是否调用外部工具由使用它的 Agent 和用户授权共同决定。

## 开源协议

[MIT](LICENSE)

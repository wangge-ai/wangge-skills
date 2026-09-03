# 2026-09-03 公开发布审计

审计对象：`wangge-ai/wangge-skills`，代码基线 `83b74cf6f603c4153c0e5f9c053c87f7f2bd4e7d`。

## 结论

本轮检查未发现真实 Token、Cookie 值、邮箱、手机号、本地用户绝对路径或大于 1 MB 的历史 Blob。7 个 Skill 均可从隔离副本安装并通过结构校验；26 项单元测试、11 个脚本入口和 CSV/XLSX 最小运行路径通过。

本结论表示“在本轮检查范围内未发现问题”，不等于未来版本没有风险。每次正式公开或发布仍需执行 [发布检查表](../release-checklist.md)。

## 敏感信息与历史

- 扫描范围：当前文件和全部 6 个可达 Git 提交。
- 检查类型：常见云/API Token、私钥头、带值密码字段、Cookie 值、邮箱、中国大陆手机号、Windows/macOS/Linux 用户绝对路径。
- 结果：上述类别均为 0 个命中。
- 大文件：全部可达历史中没有超过 1 MB 的 Blob。
- 限制：模式扫描不能识别所有自定义密钥，也不能撤回已经被第三方复制的公开内容。

## 行为审查

| Skill | 联网 | 本地读写 | 下载/删除 | 登录/浏览器 | 结论 |
|---|---|---|---|---|---|
| `ecom-main-image-diagnosis` | 无脚本 | 无脚本 | 无 | 仅由宿主 Agent 按用户输入查看图片 | 文档型 Skill |
| `ecom-market-insight-table` | 无 | 读取 CSV/XLSX；写入 JSON、Markdown、HTML 到指定目录 | 不下载、不删除 | 不登录、不启动浏览器 | XLSX 可选依赖为 `openpyxl` |
| `ecommerce-competitor-analyzer` | 链接探测器访问用户指定的公开 HTTP/HTTPS 页面 | 读取 CSV/JSON/Markdown；写入报告和公开页面响应副本 | 保存响应，不删除文件 | 不使用浏览器登录态，不绕过验证码 | 已拒绝本机、内网、保留地址、非 HTTP 协议、内嵌凭证及不安全重定向 |
| `frontend-design-system` | 脚本不联网 | 读取清单/路径；写入指定 HTML | 不下载、不删除 | 不启动浏览器；若输出引用远程图片，打开页面时由浏览器加载 | 本地比较页生成器 |
| `github-content-radar` | 无自带脚本；宿主 Agent 可按授权查询公开来源 | 无自带脚本 | 无 | 不绕过登录或访问控制 | 文档与参考资料型 Skill |
| `github-repo-dissector` | 只构造 GitHub API 与 GitHub Trending 请求 | 不写文件 | 不下载仓库、不删除 | 不登录浏览器；可从环境读取 `GITHUB_TOKEN` 并只发往 GitHub API | 已拒绝非 GitHub 和带内嵌凭证的仓库 URL |
| `rpa-flow-architect` | 无 | 读取日志、状态和规范；仅在给出输出路径时写入结果 | 不下载、不删除 | 只审计 RPA 证据，不执行登录或浏览器自动化 | 8 项审计器测试通过 |

代码中未发现 `subprocess`、Shell 执行、动态 `eval/exec`、递归删除或静默上传本地文件的实现。

## 一致性修复

- 将通用市场报告里的特定公司名称和专用字段改为 `own_brand_label`、`own_brand_rows`、`own_brand_share` 和 `own_skus`。
- 修复 `github-content-radar` 中 11 个失效的参考资料路径，并在入口 Skill 中补充按任务读取的路由。
- 为 `frontend-design-system` 和 `github-content-radar` 补齐独立 README 与 MIT 许可证。
- 为两个数据分析 Skill 增加虚构 CSV 样例；明确 Python 3.10+ 和 XLSX 可选依赖。
- 为商品链接探测器增加公网 URL 校验及回归测试。
- 为 GitHub 仓库参数增加域名、路径和内嵌凭证校验。
- 增加仓库级测试，核对目录与索引、公开包文件、相对链接和已知私有品牌残留。

## 隔离环境复验

- 系统：Windows，独立 Git 克隆、独立 Skills 安装目录、全新 Python 虚拟环境。
- Python：3.12.13。
- 运行依赖：`openpyxl 3.1.5`；结构校验工具单独使用 `PyYAML 6.0.3`。
- Skill 结构校验：7/7 通过。
- 单元测试：26/26 通过。
- 脚本命令入口：11/11 的 `--help` 通过。
- 运行样例：市场 CSV、市场 XLSX、竞品 CSV、HTML 渲染、视觉比较页、GitHub 公共 API 和公开 URL 探测均通过。
- 边界样例：`127.0.0.1` 商品链接被拒绝，未创建目标输出目录。

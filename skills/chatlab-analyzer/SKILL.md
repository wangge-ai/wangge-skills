---
name: chatlab-analyzer
description: 使用 ChatLab 分析用户已有聊天导出，组织统计、搜索、SQL 和证据报告。
license: MIT
metadata:
  source_pack: '16'
---

# ChatLab 聊天记录深度分析 Skill

本包是原创分析方法，不包含 ChatLab 程序。本次对照官方 npm `chatlab-cli@0.37.5` 的命令定义更新示例（2026-10-08）。安装前检查 [npm 包信息](https://www.npmjs.com/package/chatlab-cli)；当前发布包要求 Node.js ≥ 22.19.0。`clb` 和 `chatlab` 都是官方命令别名，下面统一用 `clb`。真实聊天导入和模型调用未在本次发布中重跑。

先运行 `clb --help`、`clb formats`、`clb manifest` 核对所装版本。官方项目与文档入口见 [ChatLab](https://github.com/ChatLab/ChatLab)。

## 概述

用 ChatLab CLI 对导入的聊天记录做全自动深度分析：统计总览 → 成员排行 → 关键词搜索 → SQL 自由查询 → AI Agent 智能分析 → 生成结构化报告。

## 前置条件

1. **ChatLab CLI 已安装**（`clb --version` 可运行）
2. **聊天记录文件已准备好**（具体格式以所安装版本的帮助为准，下面是原分享包的格式示例）
3. **LLM 已配置**（可选，用于 AI Agent 功能；不配也能用统计/搜索/SQL）

### 安装 ChatLab CLI（如未安装）

```bash
npm install -g chatlab-cli
```

使用用户选择的 Node 环境安装，运行 `clb --version` 确认可执行文件可用。

### 配置 LLM（可选）

先用 `clb config path` 查看当前配置位置，或用 `clb web --no-open` 打开本地管理界面配置模型。下面是原分享包的 OpenAI 兼容模型配置示例；具体字段和存储位置以当前版本为准，不直接覆盖已有配置：

```json
{
  "configs": [{
    "id": "deepseek-main",
    "provider": "openai",
    "model": "deepseek-chat",
    "apiKey": "你的DeepSeek API Key",
    "baseUrl": "https://api.deepseek.com/v1"
  }],
  "defaultAssistant": { "configId": "deepseek-main", "modelId": "deepseek-chat" }
}
```

支持的 provider: `openai`（用于兼容接口；各提供方的字段和能力需分别核验）。按提供方的官方配置填写 `baseUrl` 和 `model`，再用用户批准的最小问题验证。

## 支持的导入格式

| 格式 ID | 来源 | 文件扩展名 |
|---|---|---|
| `weflow` | WeFlow 导出（微信） | `.json` |
| `ycccccccy-echotrace` | echotrace 导出（微信） | `.json` |
| `shuakami-qq-exporter` | Shuakami QQ 导出 | `.json` |
| `qq-native-txt` | QQ 官方 TXT 导出 | `.txt` |
| `telegram-native` | Telegram 官方 JSON 导出 | `.json` |
| `tyrrrz-discord-exporter` | DiscordChatExporter | `.json` |
| `whatsapp-native-txt` | WhatsApp 官方 TXT | `.txt` |
| `line-native-txt` | LINE 官方 TXT | `.txt` |
| `instagram-native` | Instagram 官方导出 | - |
| `google-chat-takeout` | Google Chat Takeout | - |
| `chatlab` | ChatLab 标准格式 | `.json` / `.jsonl` |

**微信导出来源示例**：原分享包使用 WeFlow。只使用用户有权处理的已有导出文件，工具和格式兼容性以各自当前官方文档为准。本仓库不分发导出客户端。

## 执行流程

### Step 1: 导入数据

```bash
clb import <文件路径> [--format <格式ID>] [--session-id <自定义ID>]
```

- 不指定 `--format` 时自动检测格式
- 不指定 `--session-id` 时自动生成
- 成功后返回 Session ID，后续所有命令都需要它

**验证导入成功**：
```bash
clb sessions list --format json          # 列出所有会话
clb stats overview --session <session-id> --format json # 查看统计总览
```

### Step 2: 统计总览

```bash
clb stats overview --session <session-id> --format json
```

输出：
- 会话名称、平台、类型
- 总消息数、成员数
- 时间范围
- Top 10 活跃成员排行

### Step 3: 成员分析

```bash
clb members list --session <session-id> --format json
```

输出所有成员及其消息数量。

### Step 4: 关键词搜索

```bash
clb messages search <关键词> --session <session-id> --format json
```

返回匹配的消息列表（含时间戳、发送者、内容）。

建议多维度搜索：
- 人名/昵称 — 看某人说了什么
- 技术词（AI/RAG/MCP）— 追踪技术讨论
- 情绪词（哈哈/好的/感谢）— 判断氛围
- 链接/文件 — 追踪资源分享

### Step 5: SQL 自由查询

```bash
clb sql "<SQL语句>" --session <session-id> [--format agent|json|text]
```

**查询前先核对实际表结构**：运行 `clb schema --session <session-id> --format json`。以下是原资料中的表与 SQL 示例，按当前结构适配；只执行读取查询，不修改聊天库。

**数据库表结构示例**:

| 表名 | 说明 | 主要字段 |
|---|---|---|
| `message` | 消息表 | id, sender_id, sender_account_name, sender_group_nickname, ts, type, content, reply_to_message_id, platform_message_id |
| `member` | 成员表 | id, platform_id, account_name, group_nickname, roles |
| `meta` | 元信息表 | name, platform, type, group_id |
| `segment` | 分段表 | 用于时间分段统计 |
| `message_context` | 消息上下文 | 用于上下文关联查询 |
| `message_fts*` | 全文索引表 | FTS5 全文搜索索引 |

**常用 SQL 模板**:

```sql
-- 每小时消息量分布
SELECT strftime('%H', datetime(ts, 'unixepoch')) AS hour, COUNT(*) AS cnt
FROM message GROUP BY hour ORDER BY hour;

-- 发言排行 TOP 10
SELECT sender_account_name, COUNT(*) AS msg_count
FROM message GROUP BY sender_id, sender_account_name
ORDER BY msg_count DESC LIMIT 10;

-- 每人每天发言量热力图基础
SELECT sender_account_name,
       date(datetime(ts, 'unixepoch')) AS day,
       COUNT(*) AS cnt
FROM message GROUP BY sender_account_name, day
ORDER BY day, cnt DESC;

-- 最长消息 TOP 10
SELECT sender_account_name, length(content) AS len, substr(content, 1, 50) AS preview
FROM message WHERE content IS NOT NULL
ORDER BY len DESC LIMIT 10;

-- 回复关系（谁回复谁最多）
SELECT m1.sender_account_name AS replier,
       m2.sender_account_name AS target,
       COUNT(*) AS reply_count
FROM message m1 JOIN message m2 ON m1.reply_to_message_id = m2.platform_message_id
GROUP BY replier, target ORDER BY reply_count DESC LIMIT 15;

-- 消息类型分布
SELECT CASE type
  WHEN 0 THEN '文本' WHEN 1 THEN '图片' WHEN 3 THEN '视频'
  WHEN 4 THEN '文件' WHEN 8 THEN '链接' WHEN 25 THEN '引用'
  ELSE CAST(type AS TEXT) END AS type_name,
  COUNT(*) AS cnt FROM message GROUP BY type ORDER BY cnt DESC;
```

### Step 6: AI Agent 分析（需要 LLM 已配置）

```bash
# 单次提问
clb chat --session-id <session-id> -q "<问题>" [--no-stream]

# 多维度自动分析（依次执行多个问题）
clb chat --session-id <session-id> -q "这个群的核心话题是什么？列出前5个"
clb chat --session-id <session-id> -q "谁是群里最活跃的人？分析他的发言特点"
clb chat --session-id <session-id> -q "群里有哪些关键讨论？总结每个讨论的结论"
clb chat --session-id <session-id> -q "分析群的活跃时间段和作息规律"
clb chat --session-id <session-id> -q "有没有潜在的冲突或分歧？"
```

**推荐的分析维度**:

| 维度 | 推荐提问 |
|---|---|
| 话题概览 | 这个群主要在聊什么？按热度排列话题 |
| 人物画像 | 谁最活跃？每个人的角色和风格是什么？ |
| 时间规律 | 大家什么时候最活跃？有规律吗？ |
| 关系图谱 | 谁跟谁互动最多？有没有小圈子？ |
| 内容质量 | 有价值的讨论有哪些？垃圾信息占比？ |
| 情绪氛围 | 整体氛围如何？积极还是消极？ |
| 决策追踪 | 有哪些决策或共识是怎么达成的？ |
| 未解决问题 | 还有什么问题没有结论？ |

### Step 7: 生成报告

将以上所有结果汇总为一份结构化 Markdown 或 HTML 报告。

**报告模板结构**:

```
# [群名] 聊天记录分析报告

## 一、概览
- 基本信息（平台/类型/时间范围/人数/消息数）
- KPI 卡片（总消息数/日均消息数/活跃率/高峰时段）

## 二、成员分析
- 活跃度排行榜
- 角色识别（群主/管理员/活跃分子/潜水者）
- 发言特征分析

## 三、内容分析
- 话题分类与热度
- 关键词云
- 高价值对话摘要
- 链接与资源清单

## 四、时间分析
- 日/周/月活跃趋势
- 24 小时热力图
- 间歇期识别

## 五、关系分析
- 互动网络（谁回复谁）
- 小圈子识别
- 桥梁节点（跨圈子连接者）

## 六、AI 洞察
- （来自 chat 命令的 AI 分析结果）

## 七、附录
- 原始数据统计
- 搜索结果详情
- SQL 查询原始输出
```

## 完整执行示例

```bash
# 1. 导入
clb import /path/to/my-group.json --format weflow

# 输出: Import succeeded! Session ID: chat_xxx_yyy

# 2. 统计
clb stats overview --session chat_xxx_yyy --format json

# 3. 搜索关键词
clb messages search "AI" --session chat_xxx_yyy --format json
clb messages search "项目" --session chat_xxx_yyy --format json

# 4. SQL 分析
clb sql "SELECT sender_account_name, COUNT(*) FROM message GROUP BY sender_id ORDER BY COUNT(*) DESC LIMIT 10" --session chat_xxx_yyy --format json

# 5. AI 分析（如果 LLM 已配置）
clb chat --session-id chat_xxx_yyy -q "分析这个群的讨论重点和人物关系"
```

## 注意事项

1. **首次导入会触发中文分词器初始化**（jieba），看到 `[NLP] jieba dict missing` 提示是正常的，会 fallback 到内置分词器
2. **大文件（100万+条消息）建议用 JSONL 格式**，内存占用更稳定
3. **AI Agent 需要 API Key 和网络连通性**，纯统计分析不需要
4. **外部模型会收到所选上下文**，调用前明确用户允许发送的范围；本地处理和外部模型调用分别说明
5. **实际数据与配置位置**使用 `clb config path` 和当前官方文档核对，不依赖原分享包的固定目录
6. **如果 LLM 超时，检查 baseUrl 是否可达、API Key 是否有效**

## 微信导出流程的历史示例

以下是原分享时的客户端操作快照，不作为当前版本的安装或兼容性承诺。使用用户已有且合法取得的导出文件即可从 Step 1 开始。

```
1. 安装 WeFlow（下载 exe，双击运行）
   → 要求：微信版本 ≥ 4.0

2. 打开 WeFlow，连接微信数据库
   → 注意：首次获取解密密钥需要先退出微信登录，再回 WeFlow 点获取，最后重新扫码登录

3. 选择要分析的群聊

4. 导出为 ChatLab 格式 (.json)
   → 设置 → 导出 → 格式选 "ChatLab 专属格式"

5. 用本 skill 的 Step 1-7 进行分析
```

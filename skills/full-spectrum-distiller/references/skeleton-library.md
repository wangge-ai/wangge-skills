# Skeleton Library — 行业骨架库（v2.1：关键词精确匹配版）

每次蒸馏新对象前**必读此文件**，按关键词**精确匹配**到骨架文件。蒸馏结束后回写"已研究行业"清单。

---

## 一、命中规则

按下表顺序匹配，**命中关键词（任一即匹配）→ 对应骨架文件**。命中即停。匹配不到落回 `_generic.md`。

| 命中关键词（任一即匹配） | 骨架文件 | 适用范围 |
|---|---|---|
| 补充剂 / supplement / 维生素 / vitamin / 保健品 / nutraceutical / 蛋白粉 / protein / 减肥 / weight-loss / GLP-1 / 益生菌 / probiotic | `consumer-supplements.md` | 补剂/保健品/功能性食品 |
| 宠物 / pet / 母婴 / baby / 美妆 / beauty / 护肤 / skincare / 服饰 / apparel / 家居 / home / 食品 / food / DTC / shopify | `ecommerce-dtc.md` | 实物消费品 DTC |
| SaaS / B2B / CRM / ERP / API / developer-tool / 企业服务 / enterprise / workflow / automation | `saas-b2b.md` | 企业软件/API工具 |
| AI / LLM / agent / coding-assistant / 多模态 / 大模型 / model / 推理 / inference / MCP | `ai-tools.md` | AI/LLM/Agent/Coding |
| 自媒体 / creator / influencer / KOL / newsletter / podcast / youtube-channel / 知识付费 / course | `content-creator.md` | 创作者经济 |
| **其他所有输入** | `_generic.md` | 通用兜底 |

> URL 输入特殊处理：先用 `WebFetch` 抓首页 hero/标语提取关键词，再用上表匹配。

---

## 二、骨架文件清单

| 骨架 | 文件路径 | 适用 |
|---|---|---|
| 通用 | `assets/skeletons/_generic.md` | 兜底 |
| 消费品补剂 | `assets/skeletons/consumer-supplements.md` | 补剂/保健品/功能食品 |
| DTC 电商 | `assets/skeletons/ecommerce-dtc.md` | 实物消费品DTC |
| SaaS B2B | `assets/skeletons/saas-b2b.md` | 企业软件/API工具 |
| AI 工具 | `assets/skeletons/ai-tools.md` | AI/LLM/Agent/Coding |
| 内容创作者 | `assets/skeletons/content-creator.md` | 自媒体/Newsletter/KOL |

---

## 三、骨架文件的内部结构约定

每个骨架文件内含：
1. **目录树**（带 emoji 注释，复制即可建目录）
2. **该行业特殊字段表**（覆盖默认模板的额外字段）
3. **该行业特殊数据源建议**
4. **该行业典型机会角度**

---

## 四、已研究行业记录（自动沉淀）

每次跑完蒸馏追加一行。累计 ≥ 3 次频繁打补丁 → 新增专用骨架。

| 日期 | 输入 | mode | 命中骨架 | 是否打补丁 | 备注 |
|---|---|---|---|---|---|
| (示例) 2026-06-25 | 美国减肥补充剂 | industry | consumer-supplements | 否 | — |

---

## 五、跨行业资产复用规则

- **同一行业第 2 次**：用上次 `_MAP.md` 底图增量更新
- **共享上下游**（如"宠物零食"+"宠物保健品"）：相互链接 `_MAP.md`
- **骨架升级后**：提示用户可用最新骨架重蒸馏

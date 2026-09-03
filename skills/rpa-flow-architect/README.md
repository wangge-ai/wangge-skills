# RPA Flow Architect

一个用于设计、诊断、改造和验收 GUI RPA 流程的 Agent Skill。

它把 RPA 看成围绕脆弱界面操作构建的可恢复状态机，而不是一长串点击步骤。适用于影刀、UiBot、Power Automate Desktop、UiPath 等平台。

## 适用场景

- 只有业务需求和少量关键截图，需要设计完整流程
- 已有流程运行异常，需要还原控制流并定位根因
- 根据单个节点截图提供逐步修改指导
- 为现有流程增加批处理、重试、幂等和调度
- 使用日志、状态文件和输出文件验收真实运行结果
- 把当前进展整理成另一位开发者可以继续执行的交接文档

## 核心能力

- 区分已确认事实、有限推断和待补证据
- 重建循环、子流程、异常处理与资源清理关系
- 设计可结束的状态、稳定错误码和分层重试
- 检查下载、归档、状态写入和成功提交的先后关系
- 为验证码、登录和访问控制保留官方验证或人工处理边界

## 自带审计脚本

```bash
python scripts/parse_run_log.py <log>
python scripts/audit_state.py <state.json> --artifact-root <directory>
python scripts/validate_rpa_spec.py <spec.json>
```

这些脚本只负责规范化证据和检查明确约束，不能替代对真实业务流程的判断。

运行测试：

```bash
python scripts/test_auditors.py
```

## 安装

仓库发布后，可以克隆到 Agent 的 Skills 目录：

```bash
git clone https://github.com/wangge-ai/rpa-flow-architect.git ~/.agents/skills/rpa-flow-architect
```

也可以复制到项目级的 `.agents/skills/` 或对应 Agent 的 Skills 目录。

## 使用示例

```text
根据这些影刀流程截图和运行日志，先还原控制流，再判断为什么有任务一直停在 running。
```

```text
根据这份业务需求设计一套可恢复的批量下载 RPA，给出状态、重试、清理和验收方案。
```

## 开源协议

[MIT](LICENSE)


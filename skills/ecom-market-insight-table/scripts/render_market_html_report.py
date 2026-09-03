#!/usr/bin/env python
"""Render the canonical two-layer ecommerce market insight report."""

from __future__ import annotations

import argparse
import json
from html import escape
from pathlib import Path
from typing import Any


def text(value: Any, fallback: str = "-") -> str:
    if value is None:
        return fallback
    cleaned = str(value).strip()
    return cleaned if cleaned else fallback


def num(value: Any) -> str:
    if value is None or value == "":
        return "-"
    try:
        number = float(value)
    except (TypeError, ValueError):
        return text(value)
    if number >= 10000:
        return f"{number / 10000:.1f}万"
    if number.is_integer():
        return f"{int(number):,}"
    return f"{number:,.2f}"


def pct(value: Any) -> str:
    if value is None or value == "":
        return "-"
    try:
        return f"{float(value) * 100:.1f}%"
    except (TypeError, ValueError):
        return text(value)


def file_label(profile: dict[str, Any]) -> str:
    raw = text(profile.get("input_file"), "用户上传表格")
    try:
        return Path(raw).name or raw
    except Exception:
        return raw


def table(headers: list[str], rows: list[list[Any]], label: str = "数据表") -> str:
    if not rows:
        return '<p class="empty-data">暂无可用数据</p>'
    head = "".join(f'<th scope="col">{escape(header)}</th>' for header in headers)
    body = []
    for row in rows:
        cells = "".join(f"<td>{escape(text(cell))}</td>" for cell in row)
        body.append(f"<tr>{cells}</tr>")
    return (
        f'<div class="table-scroll" role="region" aria-label="{escape(label)}" tabindex="0">'
        f"<table><thead><tr>{head}</tr></thead><tbody>{''.join(body)}</tbody></table></div>"
    )


def metric(title: str, value: str, note: str) -> str:
    return (
        '<div class="metric-card">'
        f'<p class="metric-label">{escape(title)}</p>'
        f'<p class="metric-value">{escape(value)}</p>'
        f'<p class="metric-note">{escape(note)}</p>'
        "</div>"
    )


def section(title: str, body: str, class_name: str = "") -> str:
    classes = "report-section" + (f" {class_name}" if class_name else "")
    return f'<section class="{classes}"><h2>{escape(title)}</h2>{body}</section>'


def evidence_tags(ids: list[str]) -> str:
    return '<span class="evidence-list">' + "".join(
        f'<span class="evidence" data-evidence-id="{escape(evidence_id)}">{escape(evidence_id)}</span>'
        for evidence_id in ids
    ) + "</span>"


def evidence_block(item: dict[str, Any], title_key: str, body_keys: list[str]) -> str:
    body = "".join(
        f'<p><strong>{escape(label)}：</strong>{escape(text(item.get(key)))}</p>'
        for key, label in body_keys
    )
    return (
        '<article class="decision-item">'
        f'<h3>{escape(text(item.get(title_key)))}</h3>'
        f"{body}{evidence_tags(item.get('evidence_ids') or [])}</article>"
    )


def html_list(items: list[Any], empty: str = "无") -> str:
    values = [text(item) for item in items if text(item, "")]
    if not values:
        return f'<p class="empty-data">{escape(empty)}</p>'
    return '<ul class="report-list">' + "".join(f"<li>{escape(item)}</li>" for item in values) + "</ul>"


def labeled_html_rows(rows: list[tuple[str, Any]]) -> str:
    return '<dl class="task-grid">' + "".join(
        f'<div><dt>{escape(label)}</dt><dd>{escape(text(value))}</dd></div>'
        for label, value in rows
    ) + "</dl>"


def build_orchestrated_sections(report: dict[str, Any]) -> str:
    task = report.get("task_card") or {}
    audit = report.get("evidence_audit") or {}
    plan = report.get("analysis_plan") or {}
    generation = report.get("generation") or {}
    summary = report.get("executive_summary") or {}

    task_body = labeled_html_rows([
        ("决策目标", task.get("decision_goal")),
        ("报告类型", task.get("report_type")),
        ("业务对象", task.get("business_object")),
        ("阅读者", task.get("reader")),
        ("时间与范围", task.get("time_scope")),
        ("主任务", task.get("main_task")),
        ("子模块", task.get("submodules")),
    ])
    audit_body = (
        '<div class="orchestrator-grid">'
        f'<article><h3>已有资料</h3>{html_list(audit.get("available") or [])}</article>'
        f'<article><h3>缺失资料</h3>{html_list(audit.get("missing") or [])}</article>'
        f'<article><h3>口径冲突</h3>{html_list(audit.get("conflicts") or [])}</article>'
        f'<article><h3>证据边界</h3>{html_list(audit.get("boundaries") or [])}</article>'
        '</div>'
    )
    plan_body = labeled_html_rows([
        ("采用模型", "；".join(plan.get("models") or [])),
        ("数据方法", "；".join(plan.get("data_methods") or [])),
        ("分析步骤", " → ".join(plan.get("steps") or [])),
        ("报告深度", plan.get("depth")),
        ("报告目录", "；".join(plan.get("directory") or [])),
        ("可回答的问题", "；".join(plan.get("can_answer") or [])),
        ("暂时不能回答的问题", "；".join(plan.get("cannot_answer") or [])),
        ("预期可信度", plan.get("confidence")),
        ("预期产出", "；".join(plan.get("outputs") or [])),
    ])
    generation_body = (
        '<div class="generation-line">'
        f'<span class="status status-enter">{escape(text(generation.get("status")))}</span>'
        f'<strong>{escape(text(generation.get("handling")))}</strong>'
        f'<p>{escape(text(generation.get("confirmation")))}</p>'
        '</div>'
    )
    summary_body = (
        '<div class="summary-grid">'
        + metric("结论", text(summary.get("conclusion")), "证据约束后的经营判断")
        + metric("依据", text(summary.get("basis")), "仅使用当前可见证据")
        + metric("建议动作", text(summary.get("action")), "先验证，再扩量")
        + metric("可信度", text(summary.get("confidence")), text(summary.get("limitation")))
        + '</div>'
    )

    finding_blocks = []
    for index, item in enumerate(report.get("findings") or [], start=1):
        finding_blocks.append(
            '<article class="finding-block">'
            f'<p class="finding-index">发现 {index}</p><h3>{escape(text(item.get("title")))}</h3>'
            f'<p><strong>事实：</strong>{escape(text(item.get("fact")))}</p>'
            f'<p><strong>证据：</strong>{escape(text(item.get("evidence")))}</p>'
            f'<p><strong>解释：</strong>{escape(text(item.get("explanation")))}</p>'
            f'<p><strong>边界：</strong>{escape(text(item.get("boundary")))}</p>'
            f'{evidence_tags(item.get("evidence_ids") or [])}</article>'
        )
    findings_body = '<div class="finding-stack">' + "".join(finding_blocks) + '</div>'

    mechanism_blocks = []
    for item in report.get("mechanisms") or []:
        mechanism_blocks.append(
            '<article class="mechanism-block">'
            f'<p class="kind-label">{escape(text(item.get("status")))}</p>'
            f'<h3>{escape(text(item.get("title")))}</h3>'
            f'<p>{escape(text(item.get("analysis")))}</p>'
            f'{evidence_tags(item.get("evidence_ids") or [])}</article>'
        )
    mechanisms_body = '<div class="decision-grid">' + "".join(mechanism_blocks) + '</div>'

    conclusion_blocks = []
    for item in report.get("conclusions") or []:
        conclusion_blocks.append(
            '<article class="conclusion-row">'
            f'<span class="kind-label">{escape(text(item.get("type")))}</span>'
            f'<p>{escape(text(item.get("statement")))}</p>'
            f'{evidence_tags(item.get("evidence_ids") or [])}</article>'
        )
    conclusions_body = '<div class="finding-stack">' + "".join(conclusion_blocks) + '</div>'

    action_rows = [[
        item.get("action"), item.get("basis"), item.get("priority"), item.get("owner"),
        item.get("time"), item.get("metric"), item.get("risk"), item.get("fallback"),
    ] for item in report.get("actions") or []]
    action_body = table(
        ["动作", "依据", "优先级", "负责人", "时间", "指标", "风险", "后手"],
        action_rows,
        "行动建议",
    )
    quality = report.get("quality_review") or {}
    appendix_body = (
        html_list(report.get("appendix") or [])
        + '<div class="quality-strip">'
        f'<strong>语义质量复核：{escape(text(quality.get("score")))} / 100</strong>'
        f'<span>{escape(text(quality.get("result")))}</span></div>'
    )

    return (
        section("报告任务识别", task_body, "orchestrator-stage")
        + section("资料审计", audit_body, "orchestrator-stage")
        + section("分析方案", plan_body, "orchestrator-stage")
        + section("生成状态", generation_body, "orchestrator-stage")
        + section("执行摘要", summary_body, "formal-section")
        + section("任务与分析范围", html_list(report.get("scope") or []), "formal-section")
        + section("数据与方法", html_list(report.get("methods") or []), "formal-section")
        + section("关键发现", findings_body, "formal-section")
        + section("原因或机制分析", mechanisms_body, "formal-section")
        + section("结论", conclusions_body, "formal-section")
        + section("行动建议", action_body, "formal-section")
        + section("风险与未知项", html_list(report.get("risks") or []), "formal-section")
        + section("附录说明", appendix_body, "formal-section")
    )


def markdown_cell(value: Any) -> str:
    return text(value).replace("|", "\\|").replace("\n", "<br>")


def build_analysis_markdown(report: dict[str, Any], title: str) -> str:
    task = report.get("task_card") or {}
    audit = report.get("evidence_audit") or {}
    plan = report.get("analysis_plan") or {}
    generation = report.get("generation") or {}
    summary = report.get("executive_summary") or {}

    def bullets(items: list[Any]) -> str:
        return "；".join(text(item) for item in items) if items else "无"

    lines = [
        f"# {title}", "",
        "## 报告任务识别", "",
        f'- 决策目标：{text(task.get("decision_goal"))}',
        f'- 报告类型：{text(task.get("report_type"))}',
        f'- 业务对象：{text(task.get("business_object"))}',
        f'- 阅读者：{text(task.get("reader"))}',
        f'- 时间与范围：{text(task.get("time_scope"))}',
        f'- 主任务：{text(task.get("main_task"))}',
        f'- 子模块：{text(task.get("submodules"))}', "",
        "## 资料审计", "",
        f'- 已有资料：{bullets(audit.get("available") or [])}',
        f'- 缺失资料：{bullets(audit.get("missing") or [])}',
        f'- 口径冲突：{bullets(audit.get("conflicts") or [])}',
        f'- 证据边界：{bullets(audit.get("boundaries") or [])}', "",
        "## 分析方案", "",
        f'- 采用模型：{bullets(plan.get("models") or [])}',
        f'- 数据方法：{bullets(plan.get("data_methods") or [])}',
        f'- 分析步骤：{bullets(plan.get("steps") or [])}',
        f'- 报告深度：{text(plan.get("depth"))}',
        f'- 报告目录：{bullets(plan.get("directory") or [])}',
        f'- 可回答的问题：{bullets(plan.get("can_answer") or [])}',
        f'- 暂时不能回答的问题：{bullets(plan.get("cannot_answer") or [])}',
        f'- 预期可信度：{text(plan.get("confidence"))}',
        f'- 预期产出：{bullets(plan.get("outputs") or [])}', "",
        "## 生成状态", "",
        f'- 状态：{text(generation.get("status"))}',
        f'- 处理方式：{text(generation.get("handling"))}',
        f'- 确认记录：{text(generation.get("confirmation"))}', "",
        "## 执行摘要", "",
        f'- 结论：{text(summary.get("conclusion"))}',
        f'- 依据：{text(summary.get("basis"))}',
        f'- 建议行动：{text(summary.get("action"))}',
        f'- 可信度：{text(summary.get("confidence"))}',
        f'- 限制：{text(summary.get("limitation"))}', "",
        "## 任务与分析范围", "",
    ]
    lines.extend(f"- {text(item)}" for item in report.get("scope") or [])
    lines.extend(["", "## 数据与方法", ""])
    lines.extend(f"- {text(item)}" for item in report.get("methods") or [])
    lines.extend(["", "## 关键发现", ""])
    for index, item in enumerate(report.get("findings") or [], start=1):
        lines.extend([
            f'### 发现{index}：{text(item.get("title"))}', "",
            f'- 事实：{text(item.get("fact"))}',
            f'- 证据：{text(item.get("evidence"))}',
            f'- 解释：{text(item.get("explanation"))}',
            f'- 边界：{text(item.get("boundary"))}', "",
        ])
    lines.extend(["## 原因或机制分析", ""])
    for item in report.get("mechanisms") or []:
        lines.extend([
            f'### {text(item.get("title"))}', "",
            f'- 证据状态：{text(item.get("status"))}',
            f'- 分析：{text(item.get("analysis"))}',
            f'- 证据编号：{", ".join(item.get("evidence_ids") or [])}', "",
        ])
    lines.extend(["## 结论", ""])
    for item in report.get("conclusions") or []:
        lines.append(
            f'- {text(item.get("type"))}：{text(item.get("statement"))} '
            f'[证据：{", ".join(item.get("evidence_ids") or [])}]'
        )
    lines.extend(["", "## 行动建议", "", "| 动作 | 依据 | 优先级 | 负责人 | 时间 | 指标 | 风险 | 后手 |", "|---|---|---|---|---|---|---|---|"])
    for item in report.get("actions") or []:
        values = [item.get(key) for key in ("action", "basis", "priority", "owner", "time", "metric", "risk", "fallback")]
        lines.append("| " + " | ".join(markdown_cell(value) for value in values) + " |")
    lines.extend(["", "## 风险与未知项", ""])
    lines.extend(f"- {text(item)}" for item in report.get("risks") or [])
    lines.extend(["", "## 附录", ""])
    lines.extend(f"- {text(item)}" for item in report.get("appendix") or [])
    quality = report.get("quality_review") or {}
    lines.extend([
        f'- 语义质量复核：{text(quality.get("score"))} / 100',
        f'- 复核结果：{text(quality.get("result"))}', "",
    ])
    return "\n".join(lines)


def deep_analysis_sections(facts_view: dict[str, Any]) -> tuple[str, str]:
    deep = facts_view.get("deep_analysis") or {}
    if not deep:
        return "", ""

    snapshot = deep.get("executive_snapshot") or {}
    snapshot_html = (
        '<section class="executive-snapshot" aria-label="执行摘要">'
        '<article class="snapshot-card snapshot-conclusion"><p>核心结论</p>'
        f'<strong>{escape(text(snapshot.get("strongest_conclusion")))}</strong></article>'
        '<article class="snapshot-card snapshot-limit"><p>最大限制</p>'
        f'<strong>{escape(text(snapshot.get("biggest_limitation")))}</strong></article>'
        '<article class="snapshot-card snapshot-action"><p>下一步动作</p>'
        f'<strong>{escape(text(snapshot.get("next_action")))}</strong></article>'
        "</section>"
    )

    source_rows = [[
        item.get("name"), item.get("evidence_type"), item.get("scope"), item.get("source"), item.get("usage")
    ] for item in deep.get("source_inventory", [])]
    source_body = (
        '<div class="evidence-explainer"><strong>FACT_* 是机器证据编号，不是图片。</strong>'
        '<p>编号用于让结论能回指到确定性事实。表格类证据展示计算来源和关键结果；'
        '只有标记为“图片证据”的项目才必须同时展示原图。</p></div>'
        + table(
            ["数据源", "证据形态", "样本范围", "本地来源", "在报告中的用途"],
            source_rows,
            "报告数据源",
        )
    )

    target = deep.get("target_band") or {}
    band_rows = [[
        item.get("band"), item.get("rows"), pct(item.get("share")), num(item.get("median_price")),
        num(item.get("median_sales_signal")), pct(item.get("ad_share")), item.get("wolongsen_rows"),
    ] for item in deep.get("business_price_bands", [])]
    ad_rows = [[
        item.get("channel"), item.get("rows"), pct(item.get("share")), num(item.get("median_price")),
        num(item.get("median_sales_signal")), num(item.get("median_rank")), item.get("target_band_rows"),
        item.get("wolongsen_rows"),
    ] for item in deep.get("ad_comparison", [])]
    structure_body = (
        '<div class="audit-strip">'
        + metric("目标价格带商品", num(target.get("rows")), f"占固定样本 {pct(target.get('share'))}")
        + metric("目标带中位价", f"¥{num(target.get('median_price'))}", "30 元与 50 元均纳入")
        + metric("沃朗森占位", num(target.get("wolongsen_rows")), f"目标价格带占比 {pct(target.get('wolongsen_share'))}")
        + "</div>"
        + '<h3>经营价格带</h3>'
        + table(
            ["页面展示价区间", "商品数", "占比", "中位价", "付款信号中位下限", "广告占比", "沃朗森商品数"],
            band_rows,
            "经营价格带",
        )
        + '<h3>广告与自然位对照</h3>'
        + table(
            ["位置类型", "商品数", "占比", "中位价", "付款信号中位下限", "中位排名", "目标带商品", "沃朗森商品"],
            ad_rows,
            "广告与自然位对照",
        )
        + '<p class="boundary-note">广告标记只说明页面是否明确标注广告；付款信号是页面可见下限，不能据此推断投放效率、销量或 GMV。</p>'
    )

    claim_rows = [[
        item.get("claim"), item.get("rows"), pct(item.get("share")), item.get("role")
    ] for item in deep.get("claim_taxonomy", [])]
    pair_rows = [[
        item.get("pair"), item.get("rows"), pct(item.get("share"))
    ] for item in deep.get("claim_cooccurrence", [])]
    claim_body = (
        '<h3>卖点分类</h3>'
        + table(["卖点类型", "商品数", "样本占比", "经营角色"], claim_rows, "卖点分类")
        + '<h3>高频卖点共现</h3>'
        + table(["共现组合", "商品数", "样本占比"], pair_rows, "卖点共现")
        + '<p class="boundary-note">这里分析的是商家供给侧表达。没有评价正文时，不能把高频标题词直接解释为用户需求或购买动机。</p>'
    )

    brand_rows = [[
        item.get("brand"), item.get("rows"), pct(item.get("share")), item.get("target_band_rows"),
        num(item.get("median_price")), num(item.get("median_sales_signal")), item.get("ad_rows"),
    ] for item in deep.get("brand_map", [])]
    sku_rows = [[
        item.get("rank"), item.get("product_id"), num(item.get("price")), num(item.get("sales_signal")),
        "是" if item.get("is_ad") else "否", item.get("claims"),
    ] for item in deep.get("wolongsen_skus", [])]
    brand_body = (
        '<h3>品牌货架地图</h3>'
        + table(
            ["品牌/识别主体", "商品数", "占比", "目标带商品", "中位价", "付款信号中位下限", "广告商品"],
            brand_rows,
            "品牌货架地图",
        )
        + '<h3>沃朗森内部 SKU</h3>'
        + table(
            ["搜索位次", "商品 ID", "展示价", "付款信号下限", "广告", "标题卖点分类"],
            sku_rows,
            "沃朗森内部 SKU",
        )
        + '<p class="boundary-note">同价和卖点重叠代表潜在内部竞争，需要结合投放与成交归因验证，不能直接等同于实际流量蚕食。</p>'
    )

    competitor_rows = [[
        item.get("product_id"), item.get("brand"), item.get("archetype"), num(item.get("search_price")),
        num(item.get("live_price")), num(item.get("price_delta")), item.get("services"),
        item.get("sku_groups"), item.get("assets"), item.get("reviews"),
    ] for item in deep.get("competitor_matrix", [])]
    competitor_body = (
        table(
            ["商品 ID", "品牌", "竞争原型", "搜索价", "详情价", "价差", "服务项", "SKU 组", "首屏图", "评价正文"],
            competitor_rows,
            "前 10 竞品核验",
        )
        + '<p class="boundary-note">详情展示价仍不等于会员价、券后价、红包价或最终结算价；评价为 0 的商品不输出用户声音结论。</p>'
    )

    image_cards = []
    for index, item in enumerate(deep.get("image_diagnostics", []), start=1):
        href = text(item.get("asset_href"), "")
        image_html = (
            f'<img src="{escape(href, quote=True)}" '
            f'alt="{escape(text(item.get("brand")))}：{escape(text(item.get("role")))}" loading="lazy">'
            if href
            else '<div class="image-missing">图片文件未进入报告，已删除空图片占位。</div>'
        )
        image_cards.append(
            '<figure class="evidence-image-card">'
            f'{image_html}<figcaption><p class="image-kicker">图片 {index} · {escape(text(item.get("brand")))}</p>'
            f'<h3>{escape(text(item.get("role")))}</h3>'
            f'<p><strong>可用优势：</strong>{escape(text(item.get("strength")))}</p>'
            f'<p><strong>表达弱点：</strong>{escape(text(item.get("weakness")))}</p>'
            f'<p class="compliance-copy"><strong>证据/合规关注：</strong>{escape(text(item.get("compliance_watch")))}</p>'
            '</figcaption></figure>'
        )
    image_body = (
        f'<div class="evidence-image-grid">{"".join(image_cards)}</div>'
        + '<p class="boundary-note">以上为全部已保存并实际用于分析的首屏图片。视觉诊断不推断点击率、转化率，也不代表完整详情页表现。</p>'
    )

    sections = (
        section("数据源与证据说明", source_body)
        + section("经营结构诊断", structure_body)
        + section("卖点供给与共现", claim_body)
        + section("品牌与店铺竞争", brand_body)
        + section("前 10 竞品核验", competitor_body)
        + section("主图证据诊断", image_body)
    )
    return snapshot_html, sections


def facts_or_profile(profile: dict[str, Any], facts: dict[str, Any] | None) -> dict[str, Any]:
    if facts:
        return facts
    columns = profile.get("detected_columns") or {}
    total = profile.get("row_count", 0)
    return {
        "field_coverage": {
            logical: {
                "column": column,
                "non_empty": total,
                "total": total,
                "coverage": 1 if total else 0,
            }
            for logical, column in columns.items()
        },
        "ad_summary": {"yes": 0, "no": 0, "unknown": total, "total": total},
        "duplicate_summary": {"key": None, "unique_rows": total, "duplicate_rows": 0, "duplicate_groups": 0},
        "title_phrases": profile.get("top_title_terms") or [],
        "facts": [],
    }


def build_html(
    profile: dict[str, Any],
    title: str,
    facts: dict[str, Any] | None = None,
    decision: dict[str, Any] | None = None,
    analysis_report: dict[str, Any] | None = None,
) -> str:
    facts_view = facts_or_profile(profile, facts)
    price_summary = profile.get("price_summary") or {}
    sales_summary = profile.get("sales_summary") or {}
    coverage = facts_view.get("field_coverage") or {}
    shop_coverage = coverage.get("shop") or {}
    ad_summary = facts_view.get("ad_summary") or {}
    duplicate_summary = facts_view.get("duplicate_summary") or {}
    complete = decision is not None
    verdict = decision.get("verdict", {}) if decision else {}
    status_label = {"enter": "可进入", "conditional": "有条件验证", "hold": "暂缓进入"}.get(verdict.get("status"), "事实层已完成")
    if analysis_report:
        lead = (analysis_report.get("executive_summary") or {}).get("conclusion")
    else:
        lead = verdict.get("summary") if complete else "基础数据检查和可复核事实已就绪，运营决策层正在生成。"

    field_names = {
        "title": "商品标题", "price": "页面展示价", "price_label": "页面价格标签", "sales": "付款/销量信号",
        "shop": "店铺/卖家", "brand": "品牌", "category": "类目", "is_ad": "广告标记", "product_id": "商品 ID",
    }
    field_rows = []
    for logical in field_names:
        item = coverage.get(logical) or {"column": None, "non_empty": 0, "total": profile.get("row_count", 0), "coverage": 0}
        field_rows.append([field_names[logical], item.get("column") or "未识别", f"{item.get('non_empty', 0)}/{item.get('total', 0)}", pct(item.get("coverage"))])

    sample_audit = (
        table(["字段", "对应列", "非空/总数", "覆盖率"], field_rows, "字段覆盖率")
        + '<div class="audit-strip">'
        + metric("广告样本", num(ad_summary.get("yes")), "仅统计明确广告标记")
        + metric("重复样本", num(duplicate_summary.get("duplicate_rows")), f"去重键：{text(duplicate_summary.get('key'), '未识别')}")
        + metric("店铺字段覆盖", pct(shop_coverage.get("coverage")), f"{shop_coverage.get('non_empty', 0)}/{shop_coverage.get('total', 0)} 条")
        + "</div>"
    )

    price_labels = [[item.get("label"), item.get("rows")] for item in profile.get("price_label_counts", [])]
    price_bands = [[item.get("band"), item.get("rows"), num(item.get("avg_sales_signal"))] for item in profile.get("price_bands", [])]
    price_body = (
        '<h3>页面价格标签分布</h3>' + table(["页面价格标签", "商品数"], price_labels, "页面价格标签分布")
        + '<h3>页面展示价格带</h3>' + table(["页面展示价区间", "商品数", "平均付款信号下限"], price_bands, "页面展示价格带")
        + '<p class="boundary-note">价格必须按页面标签分开理解；付款信号中的“万+”按展示下限解析，不等于精确销量。</p>'
    )

    shop_rows = [[item.get("name"), item.get("rows")] for item in profile.get("top_shops", [])]
    competition_body = (
        table(["店铺", "样本商品数"], shop_rows, "店铺分布")
        + f'<p class="boundary-note">样本店铺 HHI：{escape(num(profile.get("shop_hhi")))}。仅按店铺字段非空的样本计算。</p>'
    )

    phrase_rows = []
    for item in facts_view.get("title_phrases", []):
        phrase_rows.append([item.get("phrase", item.get("term")), item.get("rows"), pct(item.get("share"))])
    claim_rows = [[item.get("claim"), item.get("rows"), pct(item.get("share"))] for item in profile.get("claim_counts", [])]
    saturation_body = (
        '<h3>重复标题短语</h3>' + table(["连续短语", "出现商品数", "样本占比"], phrase_rows, "标题短语")
        + '<h3>固定卖点词命中</h3>' + table(["卖点词", "出现商品数", "样本占比"], claim_rows, "卖点词命中")
    )
    executive_snapshot, deep_sections = deep_analysis_sections(facts_view)
    orchestrated_sections = build_orchestrated_sections(analysis_report) if analysis_report else ""

    verdict_body = ""
    decision_sections = ""
    if complete:
        findings = "".join(evidence_block(item, "title", [("finding", "事实判断"), ("implication", "运营含义")]) for item in decision.get("key_findings", []))
        verdict_body = (
            '<div class="verdict-line">'
            f'<span class="status status-{escape(text(verdict.get("status"), "conditional"))}">{escape(status_label)}</span>'
            f'<p>{escape(text(verdict.get("rationale")))}</p>{evidence_tags(verdict.get("evidence_ids") or [])}</div>'
            f'<div class="decision-grid">{findings}</div>'
        )
        opportunity_rows = [[
            item.get("name"), item.get("target_segment"), item.get("price_position"), item.get("differentiation"), item.get("risk"),
            ", ".join(item.get("evidence_ids") or [])
        ] for item in decision.get("opportunities", [])]
        position_rows = [[
            item.get("name"), item.get("audience"), item.get("promise"), item.get("proof"), ", ".join(item.get("evidence_ids") or [])
        ] for item in decision.get("positioning_candidates", [])]
        plan_rows = [[
            item.get("day_range"), item.get("objective"), item.get("action"), item.get("metric"), item.get("stop_rule"),
            ", ".join(item.get("evidence_ids") or [])
        ] for item in decision.get("experiment_plan", [])]
        decision_sections = (
            section("机会矩阵", table(["机会", "人群", "价格位置", "差异化", "主要风险", "证据"], opportunity_rows, "机会矩阵"))
            + section("定位候选", table(["定位", "目标人群", "承诺", "证据表达", "证据"], position_rows, "定位候选"))
            + section("14 天验证计划", table(["时间", "目标", "动作", "观察指标", "停止条件", "证据"], plan_rows, "14 天验证计划"))
        )
    else:
        verdict_body = (
            '<div class="facts-ready"><span class="status status-facts">事实层已完成</span>'
            '<p>当前可先核对字段、价格口径、广告与重复项；完整进入建议尚未生成。</p></div>'
        )

    if analysis_report:
        legacy_main_sections = (
            section("确定性样本审计", sample_audit)
            + deep_sections
        )
    else:
        legacy_main_sections = (
            executive_snapshot
            + section("结论与进入条件", verdict_body, "verdict-section")
            + section("样本审计", sample_audit)
            + section("价格与需求信号", price_body)
            + section("竞争格局", competition_body)
            + section("标题与卖点饱和度", saturation_body)
            + deep_sections
            + decision_sections
        )

    catalog = (facts_view.get("deep_analysis") or {}).get("evidence_catalog") or []
    if catalog:
        evidence_headers = ["证据编号", "中文名称", "证据类型", "直接来源", "关键结果", "边界"]
        evidence_rows = [[
            item.get("id"), item.get("display_name"), item.get("evidence_type"),
            item.get("source"), item.get("summary"), item.get("boundary"),
        ] for item in catalog]
    else:
        evidence_headers = ["证据编号", "主题", "分母", "边界"]
        evidence_rows = [
            [fact.get("id"), fact.get("topic"), fact.get("denominator"), fact.get("boundary")]
            for fact in facts_view.get("facts", [])
            if fact.get("value") not in (None, [], {})
        ]

    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape(title)}</title>
  <style>
    :root {{
      --color-page: hsl(210, 20%, 96%); --color-surface: hsl(210, 20%, 99%); --color-surface-alt: hsl(210, 18%, 94%);
      --color-ink: hsl(215, 34%, 16%); --color-ink-soft: hsl(214, 18%, 34%); --color-muted: hsl(214, 12%, 45%);
      --color-border: hsl(212, 18%, 82%); --color-navy: hsl(214, 42%, 24%); --color-navy-hover: hsl(214, 44%, 20%);
      --color-on-navy: hsl(210, 20%, 97%); --color-orange: hsl(18, 82%, 52%); --color-orange-soft: hsl(18, 70%, 94%);
      --color-teal: hsl(170, 54%, 30%); --color-teal-soft: hsl(168, 38%, 92%); --color-red: hsl(5, 66%, 43%);
      --color-red-soft: hsl(5, 56%, 94%); --color-row-hover: hsl(210, 46%, 93%); --color-focus: hsl(18, 82%, 52%);
      --font-body: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Microsoft YaHei", sans-serif;
      --text-xs: 0.75rem; --text-sm: 0.875rem; --text-base: 1rem; --text-lg: 1.125rem; --text-xl: 1.25rem;
      --text-2xl: 1.5rem; --text-3xl: 1.875rem; --metric-size: 1.75rem;
      --leading-tight: 1.25; --leading-normal: 1.55; --leading-relaxed: 1.75;
      --space-1: 0.25rem; --space-2: 0.5rem; --space-3: 0.75rem; --space-4: 1rem; --space-5: 1.25rem;
      --space-6: 1.5rem; --space-8: 2rem; --space-10: 2.5rem; --space-12: 3rem;
      --radius-sm: 0.375rem; --radius-md: 0.625rem; --border-width: 1px; --focus-width: 3px;
      --max-report: 76rem; --table-min-width: 42rem;
    }}
    * {{ box-sizing: border-box; }}
    html {{ background: var(--color-page); color: var(--color-ink); }}
    body {{ margin: 0; background: var(--color-page); color: var(--color-ink); font-family: var(--font-body); }}
    main, section, article, .metric-grid, .decision-grid, .audit-strip {{ min-width: 0; }}
    .report {{ width: min(100%, var(--max-report)); margin: 0 auto; padding: var(--space-10) var(--space-8) var(--space-12); }}
    .report-hero {{ padding: var(--space-8); border-left: var(--space-1) solid var(--color-orange); background: var(--color-navy); color: var(--color-on-navy); }}
    .report-eyebrow {{ margin: 0 0 var(--space-3); color: var(--color-on-navy); font-size: var(--text-xs); letter-spacing: 0.12em; }}
    .report-hero h1 {{ max-width: 24ch; margin: 0; font-size: var(--text-3xl); line-height: var(--leading-tight); overflow-wrap: anywhere; }}
    .report-lead {{ max-width: 38em; margin: var(--space-3) 0 0; font-size: var(--text-lg); line-height: var(--leading-relaxed); }}
    .executive-snapshot {{ display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: var(--space-3); margin-top: var(--space-4); }}
    .snapshot-card {{ padding: var(--space-4); border: var(--border-width) solid var(--color-border); border-top: var(--space-1) solid var(--color-navy); background: var(--color-surface); }}
    .snapshot-card p {{ margin: 0 0 var(--space-2); color: var(--color-muted); font-size: var(--text-xs); font-weight: 800; letter-spacing: .08em; }}
    .snapshot-card strong {{ display: block; font-size: var(--text-base); line-height: var(--leading-relaxed); }}
    .snapshot-limit {{ border-top-color: var(--color-red); }} .snapshot-action {{ border-top-color: var(--color-teal); }}
    .metric-grid, .audit-strip {{ display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: var(--space-3); margin-top: var(--space-6); }}
    .audit-strip {{ grid-template-columns: repeat(3, minmax(0, 1fr)); }}
    .metric-card {{ padding: var(--space-4); border: var(--border-width) solid var(--color-border); border-radius: var(--radius-sm); background: var(--color-surface); }}
    .metric-label, .metric-note {{ margin: 0; color: var(--color-muted); font-size: var(--text-sm); line-height: var(--leading-normal); }}
    .metric-value {{ margin: var(--space-2) 0; color: var(--color-navy); font-size: var(--metric-size); font-weight: 800; line-height: var(--leading-tight); overflow-wrap: anywhere; }}
    .report-section {{ margin-top: var(--space-6); padding: var(--space-6); border: var(--border-width) solid var(--color-border); border-radius: var(--radius-md); background: var(--color-surface); }}
    .report-section h2 {{ margin: 0 0 var(--space-4); font-size: var(--text-2xl); line-height: var(--leading-tight); }}
    .report-section h3 {{ margin: var(--space-6) 0 var(--space-3); font-size: var(--text-lg); line-height: var(--leading-normal); }}
    .report-section h2 + h3 {{ margin-top: 0; }}
    .table-scroll {{ max-width: 100%; overflow-x: auto; border: var(--border-width) solid var(--color-border); border-radius: var(--radius-sm); }}
    .table-scroll:focus-visible {{ outline: var(--focus-width) solid var(--color-focus); outline-offset: var(--space-1); }}
    table {{ width: 100%; min-width: var(--table-min-width); border-collapse: collapse; background: var(--color-surface); }}
    th, td {{ padding: var(--space-3) var(--space-4); border-right: var(--border-width) solid var(--color-border); border-bottom: var(--border-width) solid var(--color-border); text-align: left; vertical-align: top; font-size: var(--text-sm); line-height: var(--leading-normal); overflow-wrap: anywhere; }}
    th {{ background: var(--color-navy); color: var(--color-on-navy); font-weight: 700; }}
    th:last-child, td:last-child {{ border-right: 0; }} tbody tr:last-child td {{ border-bottom: 0; }}
    tbody tr:nth-child(even) {{ background: var(--color-surface-alt); }} tbody tr:hover {{ background: var(--color-row-hover); }}
    .boundary-note, .report-footnote, .empty-data {{ color: var(--color-muted); font-size: var(--text-sm); line-height: var(--leading-relaxed); }}
    .boundary-note {{ margin: var(--space-4) 0 0; }} .empty-data {{ margin: 0; }}
    .verdict-line, .facts-ready {{ padding: var(--space-4); border-left: var(--space-1) solid var(--color-orange); background: var(--color-orange-soft); }}
    .verdict-line p, .facts-ready p {{ margin: var(--space-3) 0; line-height: var(--leading-relaxed); }}
    .status {{ display: inline-block; padding: var(--space-1) var(--space-2); border-radius: var(--radius-sm); font-size: var(--text-sm); font-weight: 700; }}
    .status-enter, .status-facts {{ background: var(--color-teal-soft); color: var(--color-teal); }}
    .status-conditional {{ background: var(--color-orange-soft); color: var(--color-orange); }} .status-hold {{ background: var(--color-red-soft); color: var(--color-red); }}
    .decision-grid {{ display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: var(--space-3); margin-top: var(--space-4); }}
    .decision-item {{ padding: var(--space-4); border: var(--border-width) solid var(--color-border); border-radius: var(--radius-sm); }}
    .decision-item h3 {{ margin: 0 0 var(--space-3); }} .decision-item p {{ margin: var(--space-2) 0; line-height: var(--leading-relaxed); }}
    .task-grid {{ display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 0; margin: 0; border: var(--border-width) solid var(--color-border); }}
    .task-grid div {{ padding: var(--space-4); border-right: var(--border-width) solid var(--color-border); border-bottom: var(--border-width) solid var(--color-border); }}
    .task-grid div:nth-child(2n) {{ border-right: 0; }} .task-grid div:nth-last-child(-n+2) {{ border-bottom: 0; }}
    .task-grid dt {{ color: var(--color-muted); font-size: var(--text-xs); font-weight: 800; letter-spacing: .06em; }}
    .task-grid dd {{ margin: var(--space-2) 0 0; font-size: var(--text-base); line-height: var(--leading-relaxed); }}
    .orchestrator-grid {{ display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: var(--space-4); }}
    .orchestrator-grid article, .mechanism-block {{ padding: var(--space-4); border: var(--border-width) solid var(--color-border); }}
    .orchestrator-grid h3, .mechanism-block h3 {{ margin: 0 0 var(--space-3); }}
    .report-list {{ margin: 0; padding-left: var(--space-5); }} .report-list li {{ margin: var(--space-2) 0; line-height: var(--leading-relaxed); }}
    .generation-line {{ display: flex; flex-wrap: wrap; align-items: center; gap: var(--space-3); padding: var(--space-4); border-left: var(--space-1) solid var(--color-teal); background: var(--color-teal-soft); }}
    .generation-line p {{ flex-basis: 100%; margin: 0; color: var(--color-ink-soft); }}
    .summary-grid {{ display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: var(--space-3); }}
    .summary-grid .metric-value {{ font-size: var(--text-lg); line-height: var(--leading-normal); }}
    .finding-stack {{ display: grid; gap: var(--space-4); }}
    .finding-block, .conclusion-row {{ padding: var(--space-5); border: var(--border-width) solid var(--color-border); border-left: var(--space-1) solid var(--color-navy); }}
    .finding-block h3 {{ margin: 0 0 var(--space-3); }} .finding-block p, .conclusion-row p, .mechanism-block p {{ line-height: var(--leading-relaxed); }}
    .finding-index, .kind-label {{ margin: 0 0 var(--space-2); color: var(--color-teal); font-size: var(--text-xs); font-weight: 800; letter-spacing: .08em; }}
    .conclusion-row p {{ margin: var(--space-2) 0; }}
    .quality-strip {{ display: flex; justify-content: space-between; gap: var(--space-4); margin-top: var(--space-4); padding: var(--space-4); background: var(--color-surface-alt); }}
    .evidence-list {{ display: flex; flex-wrap: wrap; gap: var(--space-2); margin-top: var(--space-3); }}
    .evidence {{ display: inline-block; padding: var(--space-1) var(--space-2); border: var(--border-width) solid var(--color-border); border-radius: var(--radius-sm); color: var(--color-muted); font-size: var(--text-xs); }}
    .evidence-explainer {{ margin-bottom: var(--space-4); padding: var(--space-4); border-left: var(--space-1) solid var(--color-teal); background: var(--color-teal-soft); }}
    .evidence-explainer p {{ margin: var(--space-2) 0 0; line-height: var(--leading-relaxed); }}
    .evidence-image-grid {{ display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: var(--space-4); }}
    .evidence-image-card {{ margin: 0; overflow: hidden; border: var(--border-width) solid var(--color-border); border-radius: var(--radius-sm); background: var(--color-surface); }}
    .evidence-image-card img {{ display: block; width: 100%; height: 22rem; object-fit: contain; background: var(--color-surface-alt); }}
    .evidence-image-card figcaption {{ padding: var(--space-4); }}
    .evidence-image-card h3 {{ margin: 0 0 var(--space-3); }}
    .evidence-image-card figcaption p {{ margin: var(--space-2) 0; color: var(--color-ink-soft); font-size: var(--text-sm); line-height: var(--leading-relaxed); }}
    .evidence-image-card .image-kicker {{ color: var(--color-muted); font-size: var(--text-xs); font-weight: 800; letter-spacing: .08em; }}
    .evidence-image-card .compliance-copy {{ padding-top: var(--space-2); border-top: var(--border-width) solid var(--color-border); }}
    .image-missing {{ padding: var(--space-8); color: var(--color-muted); background: var(--color-surface-alt); text-align: center; }}
    .report-footnote {{ margin: var(--space-6) 0 0; }}
    @media (max-width: 900px) {{ .metric-grid {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }} .executive-snapshot {{ grid-template-columns: minmax(0, 1fr); }} .evidence-image-grid {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }} }}
    @media (max-width: 640px) {{
      .report {{ padding: var(--space-4); }} .report-hero, .report-section {{ padding: var(--space-4); }}
      .report-hero h1 {{ font-size: var(--text-2xl); }} .report-lead {{ font-size: var(--text-base); }}
      .metric-grid, .audit-strip, .decision-grid, .orchestrator-grid, .summary-grid, .task-grid {{ grid-template-columns: minmax(0, 1fr); }}
      .task-grid div, .task-grid div:nth-child(2n), .task-grid div:nth-last-child(-n+2) {{ border-right: 0; border-bottom: var(--border-width) solid var(--color-border); }} .task-grid div:last-child {{ border-bottom: 0; }}
      .evidence-image-grid {{ grid-template-columns: minmax(0, 1fr); }} .evidence-image-card img {{ height: auto; max-height: 32rem; }}
      .report-section h2 {{ font-size: var(--text-xl); }} th, td {{ padding: var(--space-3); }}
    }}
    @media (prefers-reduced-motion: reduce) {{ *, *::before, *::after {{ scroll-behavior: auto; }} }}
  </style>
</head>
<body>
  <main class="report">
    <header class="report-hero">
      <p class="report-eyebrow">电商市场洞察表 · 双层证据报告</p>
      <h1>{escape(title)}</h1>
      <p class="report-lead">{escape(text(lead))}</p>
      <div class="metric-grid">
        {metric("商品样本", num(profile.get("row_count")), profile.get("sample_grade", "按现有样本分析"))}
        {metric("页面展示价中位数", num(price_summary.get("median")), "不同页面价格标签需分开理解")}
        {metric("付款信号中位数", num(sales_summary.get("median")), "按展示下限解析")}
        {metric("店铺字段覆盖", pct(shop_coverage.get("coverage")), "缺失值不进入店铺集中度分母")}
      </div>
    </header>
    {orchestrated_sections}
    {legacy_main_sections}
    {section("证据与边界", table(evidence_headers, evidence_rows, "证据与边界"))}
    <p class="report-footnote">样本：{escape(file_label(profile))}；来源：{escape(text(profile.get("source_note"), "未填写"))}；生成时间：{escape(text(profile.get("generated_at")))}。本报告不代表全平台市场份额、真实 GMV、搜索量、点击率、转化率或收益承诺。</p>
  </main>
</body>
</html>
"""


def load_optional(path_value: str) -> dict[str, Any] | None:
    if not path_value:
        return None
    return json.loads(Path(path_value).expanduser().read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser(description="Render canonical two-layer market insight HTML.")
    parser.add_argument("--profile", required=True, help="Path to market_table_profile.json")
    parser.add_argument("--facts", default="", help="Optional path to market_facts.json")
    parser.add_argument("--decision", default="", help="Optional path to market_decision.json")
    parser.add_argument("--analysis-report", default="", help="Optional path to orchestrated analysis report JSON")
    parser.add_argument("--markdown-out", default="", help="Optional Markdown output for the orchestrated report")
    parser.add_argument("--out", default="", help="Output HTML path")
    parser.add_argument("--title", default="", help="Optional report title")
    args = parser.parse_args()

    profile_path = Path(args.profile).expanduser()
    profile = json.loads(profile_path.read_text(encoding="utf-8"))
    facts = load_optional(args.facts)
    decision = load_optional(args.decision)
    analysis_report = load_optional(args.analysis_report)
    if decision and not facts:
        raise SystemExit("--decision requires --facts")
    if analysis_report and not facts:
        raise SystemExit("--analysis-report requires --facts")
    out_path = Path(args.out).expanduser() if args.out else profile_path.with_name("market_insight_report.html")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    title = args.title or f"{profile.get('category') or '电商品类'}｜电商市场洞察表"
    out_path.write_text(build_html(profile, title, facts, decision, analysis_report), encoding="utf-8")
    if args.markdown_out:
        if not analysis_report:
            raise SystemExit("--markdown-out requires --analysis-report")
        markdown_path = Path(args.markdown_out).expanduser()
        markdown_path.parent.mkdir(parents=True, exist_ok=True)
        markdown_path.write_text(build_analysis_markdown(analysis_report, title), encoding="utf-8")
        print(f"Wrote {markdown_path}")
    print(f"Wrote {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

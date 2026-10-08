#!/usr/bin/env python3
"""从商品页或保存网页采集主图、详情图，并保留来源与状态。"""

from __future__ import annotations

import argparse
import csv
import hashlib
import ipaddress
import socket
import urllib.parse
import urllib.request
import json
import re
import sys
import time
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import unquote, urljoin, urlparse
from urllib.request import Request, urlopen



def validate_public_http_url(url: str, allowed_local_origin: str | None = None) -> str:
    """Reject local, private, credential-bearing, and non-HTTP targets."""
    parsed = urllib.parse.urlsplit(url.strip())
    if parsed.scheme not in {"http", "https"}:
        raise ValueError("only http:// and https:// product URLs are allowed")
    if not parsed.hostname:
        raise ValueError("product URL must include a hostname")
    if parsed.username or parsed.password:
        raise ValueError("product URL must not include embedded credentials")

    hostname = parsed.hostname.rstrip(".").lower()
    if allowed_local_origin:
        origin = urllib.parse.urlsplit(allowed_local_origin)
        try:
            loopback = ipaddress.ip_address(hostname).is_loopback
        except ValueError:
            loopback = False
        if loopback and (parsed.scheme, hostname, parsed.port) == (origin.scheme, origin.hostname, origin.port):
            return urllib.parse.urlunsplit(parsed)

    if hostname == "localhost" or hostname.endswith(".localhost"):
        raise ValueError("local or private network URLs are not allowed")

    try:
        addresses = {ipaddress.ip_address(hostname)}
    except ValueError:
        try:
            addresses = {
                ipaddress.ip_address(item[4][0])
                for item in socket.getaddrinfo(hostname, parsed.port or 443, type=socket.SOCK_STREAM)
            }
        except socket.gaierror as exc:
            raise ValueError(f"product URL hostname could not be resolved: {hostname}") from exc

    if not addresses or any(not address.is_global for address in addresses):
        raise ValueError("local, private, reserved, or non-routable network URLs are not allowed")
    return urllib.parse.urlunsplit(parsed)


class PublicOnlyRedirectHandler(urllib.request.HTTPRedirectHandler):
    """Apply the same public-network checks to every redirect target."""

    def __init__(self, allowed_local_origin=None):
        super().__init__()
        self.allowed_local_origin = allowed_local_origin

    def redirect_request(self, req, fp, code, msg, headers, newurl):  # noqa: ANN001, D102
        safe_url = validate_public_http_url(newurl, self.allowed_local_origin)
        return super().redirect_request(req, fp, code, msg, headers, safe_url)



if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")


PLATFORM_DOMAINS = {
    "tmall": ("tmall.com", "taobao.com", "tmall.hk"),
    "jd": ("jd.com", "jd.hk"),
    "pdd": ("yangkeduo.com", "pinduoduo.com", "pdd.com"),
}

MAIN_HINTS = (
    "gallery", "main-pic", "mainpic", "main-img", "preview", "thumbnail",
    "swiper", "carousel", "商品主图", "主图", "轮播",
)
DETAIL_HINTS = (
    "description", "detail", "desc", "rich-content", "商品详情", "图文详情",
    "详情图", "详情", "成分", "证书", "检测", "报告",
)
REJECT_HINTS = (
    "logo", "icon", "avatar", "header", "footer", "toolbar", "recommend",
    "related", "comment", "review", "rate", "评价", "评论", "晒单", "猜你喜欢",
)

EXTRACT_JS = r"""
() => {
  const rows = [];
  const attrs = ['src', 'data-src', 'data-original', 'data-lazy-src', 'data-ks-lazyload'];
  const absolute = (raw) => {
    if (!raw || String(raw).startsWith('data:') || String(raw).startsWith('blob:')) return null;
    try { return new URL(String(raw), document.baseURI).href; } catch (_) { return null; }
  };
  const context = (node) => {
    const parts = [];
    let current = node;
    for (let i = 0; current && i < 5; i += 1, current = current.parentElement) {
      parts.push(`${current.tagName || ''}#${current.id || ''}.${typeof current.className === 'string' ? current.className : ''}`);
    }
    const box = node.getBoundingClientRect();
    return {
      chain: parts.join(' '),
      alt: node.getAttribute('alt') || '',
      top: Math.round(box.top + window.scrollY),
      width: Math.round(node.naturalWidth || box.width || Number(node.getAttribute('width')) || 0),
      height: Math.round(node.naturalHeight || box.height || Number(node.getAttribute('height')) || 0)
    };
  };
  for (const image of document.querySelectorAll('img')) {
    const found = new Set();
    if (image.currentSrc) found.add(image.currentSrc);
    for (const attr of attrs) {
      const value = image.getAttribute(attr);
      if (value) found.add(value);
    }
    const srcset = image.getAttribute('srcset') || image.getAttribute('data-srcset') || '';
    for (const item of srcset.split(',')) {
      const value = item.trim().split(/\s+/)[0];
      if (value) found.add(value);
    }
    for (const raw of found) {
      const url = absolute(raw);
      if (url) rows.push({ url, source: 'dom-img', context: context(image) });
    }
  }
  for (const entry of performance.getEntriesByType('resource')) {
    if (entry.initiatorType === 'img') rows.push({
      url: entry.name,
      source: 'performance',
      context: { chain: '', alt: '', top: 999999, width: 0, height: 0 }
    });
  }
  return rows;
}
"""


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(
        description="从商品链接或保存网页采集主图、详情图，并生成带来源状态的清单。"
    )
    source = result.add_mutually_exclusive_group(required=True)
    source.add_argument("--url", help="淘宝天猫、京东、拼多多商品链接，或公开测试页面")
    source.add_argument("--html-file", help="从可见浏览器保存的本地 HTML 文件")
    result.add_argument("--platform", choices=["auto", "tmall", "jd", "pdd", "generic"], default="auto")
    result.add_argument("--output", required=True, help="输出目录；包含 main、detail、manifest.json/csv 和 summary.md")
    result.add_argument("--headless", action="store_true", help="无头运行；不能用于需要人工登录的页面")
    result.add_argument("--profile-dir", help="可选的 Playwright 用户资料目录；不指定时使用工作台本机目录")
    result.add_argument("--use-current-browser", action="store_true", help="通过已连接 WebBridge 复用当前可见浏览器，不打开 Playwright 窗口")
    result.add_argument("--allow-local-assets", action="store_true", help="仅授权从明确指定的回环 WebBridge 同源下载测试素材；默认拒绝内网素材")
    result.add_argument("--webbridge-endpoint", default="http://127.0.0.1:10086/command", help="当前浏览器 WebBridge 命令地址")
    result.add_argument("--webbridge-session", help="当前任务的 WebBridge 会话名")
    result.add_argument("--login-timeout", type=int, default=180, help="可见浏览器等待使用者登录的秒数")
    result.add_argument("--scroll-rounds", type=int, default=8, help="触发懒加载的滚动轮数")
    result.add_argument("--max-main", type=int, default=12)
    result.add_argument("--max-detail", type=int, default=80)
    return result


def detect_platform(url: str, requested: str) -> str:
    if requested != "auto":
        return requested
    lowered = url.lower()
    for platform, domains in PLATFORM_DOMAINS.items():
        if any(domain in lowered for domain in domains):
            return platform
    return "generic"


def looks_blocked(page) -> bool:
    sample = ""
    try:
        sample = page.locator("body").inner_text(timeout=3000)[:5000]
    except Exception:
        pass
    haystack = f"{page.url} {page.title()} {sample}".lower()
    return any(word in haystack for word in (
        "login", "passport", "验证码", "安全验证", "请登录", "扫码登录", "访问受限", "风险验证"
    ))


def wait_for_user_login(page, timeout_seconds: int) -> bool:
    deadline = time.time() + timeout_seconds
    print(f"页面需要使用者登录或验证。请在已打开的浏览器中完成操作；最多等待 {timeout_seconds} 秒。")
    while time.time() < deadline:
        if not looks_blocked(page):
            print("检测到页面已进入可读取状态，继续采集。")
            return True
        time.sleep(2)
    return False


def click_detail_entry(page) -> None:
    try:
        page.evaluate("""() => {
          const labels = ['图文详情', '商品详情', '详情介绍'];
          const nodes = [...document.querySelectorAll('a,button,li,div,span')];
          const node = nodes.find((item) => labels.some((label) => (item.innerText || '').trim() === label));
          if (node) { node.scrollIntoView({block:'center'}); node.click(); return true; }
          return false;
        }""")
        time.sleep(1)
    except Exception:
        return


def scroll_page(page, rounds: int) -> None:
    for index in range(max(0, rounds)):
        page.evaluate("(y) => window.scrollTo(0, y)", (index + 1) * 1400)
        time.sleep(0.45)
    page.evaluate("window.scrollTo(0, 0)")
    time.sleep(0.4)


def webbridge_command(endpoint: str, session: str, action: str, args: dict, timeout: float = 20) -> dict:
    payload = json.dumps(
        {"action": action, "args": args, "session": session},
        ensure_ascii=False,
    ).encode("utf-8")
    request = Request(
        endpoint,
        data=payload,
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST",
    )
    try:
        with urlopen(request, timeout=timeout) as response:
            envelope = json.loads(response.read().decode("utf-8"))
    except (HTTPError, URLError, TimeoutError, OSError, json.JSONDecodeError) as error:
        raise RuntimeError(f"当前浏览器连接不可用：{error}") from error
    data = envelope.get("data") if isinstance(envelope, dict) and isinstance(envelope.get("data"), dict) else envelope
    if not isinstance(data, dict) or data.get("success") is False:
        message = data.get("error") if isinstance(data, dict) else None
        raise RuntimeError(f"当前浏览器操作失败：{message or '未返回有效结果'}")
    return data


def webbridge_evaluate_code(scroll_rounds: int) -> str:
    return (
        "(async()=>{"
        "await new Promise(r=>setTimeout(r,800));"
        "const labels=['图文详情','商品详情','详情介绍'];"
        "const node=[...document.querySelectorAll('a,button,li,div,span')]"
        ".find(x=>labels.some(label=>(x.innerText||'').trim()===label));"
        "if(node){node.scrollIntoView({block:'center'});node.click();await new Promise(r=>setTimeout(r,500));}"
        f"for(let i=0;i<{max(0, scroll_rounds)};i++){{window.scrollTo(0,(i+1)*1400);await new Promise(r=>setTimeout(r,350));}}"
        "window.scrollTo(0,0);"
        f"const extract={EXTRACT_JS};"
        "const candidates=extract();"
        "const text=(document.body?.innerText||'').slice(0,5000);"
        "const haystack=`${location.href} ${document.title} ${text}`.toLowerCase();"
        "const blocked=['login','passport','验证码','安全验证','请登录','扫码登录','访问受限','风险验证']"
        ".some(word=>haystack.includes(word));"
        "return JSON.stringify({url:location.href,title:document.title,text,blocked,candidates});"
        "})()"
    )


def collect_from_current_browser(args: argparse.Namespace, source_url: str) -> dict:
    session = args.webbridge_session or f"product-assets-{int(time.time())}"
    webbridge_command(
        args.webbridge_endpoint,
        session,
        "navigate",
        {"url": source_url, "newTab": True, "group_title": "商品主图详情图采集"},
    )
    result = webbridge_command(
        args.webbridge_endpoint,
        session,
        "evaluate",
        {"code": webbridge_evaluate_code(args.scroll_rounds)},
        timeout=max(20, args.scroll_rounds + 1),
    )
    value = result.get("value")
    if isinstance(value, str):
        try:
            value = json.loads(value)
        except json.JSONDecodeError as error:
            raise RuntimeError("当前浏览器没有返回可解析的页面证据") from error
    if not isinstance(value, dict):
        raise RuntimeError("当前浏览器没有返回页面证据")
    value["session"] = session
    return value


def normalize_url(raw: str, base_url: str) -> str | None:
    if not raw or raw.startswith(("data:", "blob:")):
        return None
    value = urljoin(base_url, raw.strip())
    parsed = urlparse(value)
    if parsed.scheme not in ("http", "https", "file"):
        return None
    if re.search(r"\.(css|js|json|woff2?|ttf)(?:$|[?#])", parsed.path, flags=re.I):
        return None
    return value


def classify(candidate: dict) -> tuple[str, int, str]:
    context = candidate.get("context") or {}
    blob = " ".join((
        candidate.get("url", ""), context.get("chain", ""), context.get("alt", "")
    )).lower()
    if any(word.lower() in blob for word in REJECT_HINTS):
        return "rejected", -100, "排除评论、推荐、图标或导航上下文"
    main_score = 0
    detail_score = 0
    if any(word.lower() in blob for word in MAIN_HINTS):
        main_score += 60
    if any(word.lower() in blob for word in DETAIL_HINTS):
        detail_score += 60
    width = int(context.get("width") or 0)
    height = int(context.get("height") or 0)
    top = int(context.get("top") or 999999)
    if width and height:
        ratio = max(width, height) / max(1, min(width, height))
        if ratio <= 1.5:
            main_score += 18
        if height > width * 1.35:
            detail_score += 22
    if top < 1600:
        main_score += 10
    elif top < 999999:
        detail_score += 8
    if "pcpubliccms" in blob or "mms-material-img" in blob:
        detail_score += 50
    if re.search(r"/(n0|n1)/", blob) or "mms-goods-image" in blob or "imgextra" in blob:
        main_score += 18
    if main_score == 0 and detail_score == 0:
        return "rejected", 0, "没有主图或详情图上下文证据"
    if detail_score > main_score:
        return "detail", detail_score, "详情上下文或长图特征"
    return "main", main_score, "主图上下文、首屏或近方图特征"


def image_info(data: bytes) -> tuple[str, int, int]:
    if data.startswith(b"BM") and len(data) >= 26:
        return ".bmp", int.from_bytes(data[18:22], "little", signed=True), abs(int.from_bytes(data[22:26], "little", signed=True))
    if data.startswith(b"\x89PNG\r\n\x1a\n") and len(data) >= 24:
        return ".png", int.from_bytes(data[16:20], "big"), int.from_bytes(data[20:24], "big")
    if data[:3] == b"GIF" and len(data) >= 10:
        return ".gif", int.from_bytes(data[6:8], "little"), int.from_bytes(data[8:10], "little")
    if data[:2] == b"\xff\xd8":
        offset = 2
        while offset + 9 < len(data):
            if data[offset] != 0xFF:
                offset += 1
                continue
            marker = data[offset + 1]
            if marker in range(0xC0, 0xD0) and marker not in (0xC4, 0xC8, 0xCC):
                height = int.from_bytes(data[offset + 5:offset + 7], "big")
                width = int.from_bytes(data[offset + 7:offset + 9], "big")
                return ".jpg", width, height
            if marker in (0xD8, 0xD9):
                offset += 2
                continue
            size = int.from_bytes(data[offset + 2:offset + 4], "big")
            offset += max(2, size + 2)
        return ".jpg", 0, 0
    if data[:4] == b"RIFF" and data[8:12] == b"WEBP":
        return ".webp", 0, 0
    return ".img", 0, 0


def fetch_bytes(request_context, url: str, local_root: Path | None = None, referer: str | None = None, allowed_local_origin: str | None = None) -> bytes:
    if url.startswith("file://"):
        parsed = urlparse(url)
        if local_root is None or parsed.netloc:
            raise RuntimeError("本地资源越界：仅允许读取保存 HTML 所在目录内的文件")
        local_path = unquote(parsed.path)
        if re.match(r"^/[A-Za-z]:/", local_path):
            local_path = local_path[1:]
        candidate = Path(local_path).resolve()
        allowed_root = local_root.resolve()
        try:
            candidate.relative_to(allowed_root)
        except ValueError as error:
            raise RuntimeError("本地资源越界：仅允许读取保存 HTML 所在目录内的文件") from error
        return candidate.read_bytes()
    url = validate_public_http_url(url, allowed_local_origin)
    if request_context is not None:
        response = request_context.get(url, timeout=35_000, fail_on_status_code=False, max_redirects=0)
        if not response.ok:
            raise RuntimeError(f"HTTP {response.status}")
        return response.body()
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/126 Safari/537.36",
        "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
    }
    if referer:
        headers["Referer"] = referer
    try:
        opener = urllib.request.build_opener(PublicOnlyRedirectHandler(allowed_local_origin))
        with opener.open(Request(url, headers=headers), timeout=35) as response:
            return response.read()
    except HTTPError as error:
        raise RuntimeError(f"HTTP {error.code}") from error
    except (URLError, TimeoutError, OSError) as error:
        raise RuntimeError(f"网络请求失败：{error}") from error


def write_outputs(output: Path, manifest: dict) -> None:
    (output / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    fields = ["group", "source_url", "local_path", "status", "reason", "width", "height", "bytes", "sha256"]
    with (output / "manifest.csv").open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(manifest["records"])
    summary = [
        "# 商品主图与详情图采集结果",
        "",
        f"- 业务状态：{manifest['status']}",
        f"- 页面：{manifest['page_url']}",
        f"- 平台：{manifest['platform']}",
        f"- 主图：{manifest['download']['main']} 张",
        f"- 详情图：{manifest['download']['detail']} 张",
        f"- 跳过/失败：{manifest['download']['skipped']} 条",
        f"- 耗时：{manifest['elapsed_ms']} 毫秒",
        "",
        "结果只代表本次页面可见并成功下载的图片；登录、懒加载和平台风控可能造成缺失。",
    ]
    (output / "summary.md").write_text("\n".join(summary) + "\n", encoding="utf-8")


def print_result_summary(manifest: dict, output: Path) -> None:
    status = "success" if manifest["status"] == "completed" else manifest["status"]
    counts = manifest["download"]
    total = counts["main"] + counts["detail"]
    if status == "success":
        conclusion = f"本次页面成功归档 {total} 张商品图片，其中主图 {counts['main']} 张、详情图 {counts['detail']} 张。"
        next_step = "先打开中文采集报告核对图片；如页面仍有懒加载内容，可在同一已登录页面补采。"
    elif status == "waiting_login":
        conclusion = "当前商品页要求登录或验证，尚未取得可确认的商品图片。"
        next_step = "请在当前可见浏览器完成该平台登录或验证，再从工作台重试本任务。"
    elif status == "not_available":
        conclusion = "当前浏览器连接不可用，本次没有打开备用浏览器，也没有取得商品图片。"
        next_step = "请先恢复工作台与当前浏览器的连接，再重试本任务。"
    else:
        conclusion = f"已保留本次可用图片 {total} 张，但仍有 {counts['skipped']} 条跳过或失败记录。"
        next_step = "先核对中文采集报告中的失败原因，再补充登录、页面或素材条件后重试。"
    print(f"业务状态：{status}")
    print()
    print("## 一句话结论")
    print()
    print(conclusion)
    print()
    print("## 关键结果")
    print()
    print(f"- 主图：{counts['main']} 张。")
    print(f"- 详情图：{counts['detail']} 张。")
    print(f"- 跳过或失败：{counts['skipped']} 条。")
    print("- 数量仅代表本次页面可见且成功下载的图片，不代表平台完整素材量。")
    print()
    print("## 主要产物")
    print()
    print(f"- [中文采集报告]({output / 'summary.md'})")
    if counts["main"]:
        print(f"- [主图文件夹]({output / 'main'})")
    if counts["detail"]:
        print(f"- [详情图文件夹]({output / 'detail'})")
    print()
    print("## 下一步")
    print()
    print(f"- {next_step}")


def launch_browser_context(playwright, *, headless: bool, profile: Path | None):
    errors = []
    for channel in ("chrome", "msedge", None):
        label = channel or "playwright-chromium"
        try:
            if profile is None:
                browser = playwright.chromium.launch(headless=headless, channel=channel)
                return browser, browser.new_context(locale="zh-CN", viewport={"width": 1440, "height": 1000}), label
            context = playwright.chromium.launch_persistent_context(
                str(profile), headless=headless, channel=channel, locale="zh-CN",
                viewport={"width": 1440, "height": 1000}
            )
            return None, context, label
        except Exception as error:
            errors.append(f"{label}: {error}")
    raise RuntimeError(
        "未找到可由 Playwright 使用的 Chrome、Edge 或 Chromium。"
        "请安装 Chrome/Edge，或运行 playwright install chromium。\n" + "\n".join(errors)
    )


def download_candidates(
    *,
    candidates: list[dict],
    page_url: str,
    source_url: str,
    platform: str,
    output: Path,
    main_dir: Path,
    detail_dir: Path,
    local_root: Path | None,
    request_context,
    browser_route: str,
    max_main: int,
    max_detail: int,
    started: float,
    allowed_local_origin: str | None = None,
) -> tuple[str, dict]:
    records: list[dict] = []
    deduped = {}
    for candidate in candidates:
        normalized = normalize_url(candidate.get("url", ""), page_url)
        if not normalized:
            continue
        candidate["url"] = normalized
        current = deduped.get(normalized)
        current_area = ((current or {}).get("context") or {}).get("width", 0) * ((current or {}).get("context") or {}).get("height", 0)
        new_area = (candidate.get("context") or {}).get("width", 0) * (candidate.get("context") or {}).get("height", 0)
        if current is None or new_area > current_area:
            deduped[normalized] = candidate

    selected = {"main": [], "detail": []}
    for candidate in deduped.values():
        group, score, evidence = classify(candidate)
        if group in selected:
            candidate["score"] = score
            candidate["evidence"] = evidence
            selected[group].append(candidate)
    selected["main"].sort(key=lambda item: (-item["score"], (item.get("context") or {}).get("top", 999999)))
    selected["detail"].sort(key=lambda item: ((item.get("context") or {}).get("top", 999999), -item["score"]))
    selected["main"] = selected["main"][:max_main]
    main_urls = {item["url"] for item in selected["main"]}
    selected["detail"] = [item for item in selected["detail"] if item["url"] not in main_urls][:max_detail]

    seen_hashes = set()
    counts = {"main": 0, "detail": 0, "skipped": 0}
    for group in ("main", "detail"):
        folder = main_dir if group == "main" else detail_dir
        for candidate in selected[group]:
            record = {
                "group": group, "source_url": candidate["url"], "local_path": "", "status": "failed",
                "reason": candidate["evidence"], "width": 0, "height": 0, "bytes": 0, "sha256": "",
            }
            try:
                data = fetch_bytes(request_context, candidate["url"], local_root, referer=page_url, allowed_local_origin=allowed_local_origin)
                extension, width, height = image_info(data)
                digest = hashlib.sha256(data).hexdigest()
                record.update({"width": width, "height": height, "bytes": len(data), "sha256": digest})
                if digest in seen_hashes:
                    record.update({"status": "skipped", "reason": "重复图片"})
                    counts["skipped"] += 1
                elif len(data) < 10_000 or (width and height and (width < 120 or height < 120)):
                    record.update({"status": "skipped", "reason": "图片尺寸或文件大小不足"})
                    counts["skipped"] += 1
                else:
                    seen_hashes.add(digest)
                    counts[group] += 1
                    filename = f"{group}_{counts[group]:02d}{extension}"
                    target = folder / filename
                    target.write_bytes(data)
                    record.update({"status": "downloaded", "local_path": str(target.relative_to(output))})
            except Exception as error:
                record["reason"] = f"下载失败：{error}"
                counts["skipped"] += 1
            records.append(record)

    status = "completed" if counts["main"] + counts["detail"] > 0 else "partial"
    manifest = {
        "status": status, "platform": platform, "page_url": page_url, "source_input": source_url,
        "browser_route": browser_route,
        "elapsed_ms": round((time.perf_counter() - started) * 1000),
        "candidate_count": len(deduped), "download": counts, "records": records,
    }
    write_outputs(output, manifest)
    return status, counts


def run(args: argparse.Namespace) -> int:
    started = time.perf_counter()
    output = Path(args.output).resolve()
    main_dir = output / "main"
    detail_dir = output / "detail"
    main_dir.mkdir(parents=True, exist_ok=True)
    detail_dir.mkdir(parents=True, exist_ok=True)

    source_url = Path(args.html_file).resolve().as_uri() if args.html_file else args.url
    local_root = Path(args.html_file).resolve().parent if args.html_file else None
    platform = detect_platform(source_url, args.platform)
    if args.use_current_browser:
        browser_route = "current-browser-webbridge"
        if not args.url:
            print("当前浏览器路线只用于实时商品链接；保存 HTML 请移除 --use-current-browser。", file=sys.stderr)
            return 6
        try:
            page_state = collect_from_current_browser(args, source_url)
        except Exception as error:
            manifest = {
                "status": "not_available", "platform": platform, "page_url": source_url,
                "source_input": source_url, "elapsed_ms": round((time.perf_counter() - started) * 1000),
                "browser_route": browser_route,
                "download": {"main": 0, "detail": 0, "skipped": 0}, "records": [],
                "message": "当前浏览器连接不可用；未打开备用浏览器窗口。",
            }
            write_outputs(output, manifest)
            print_result_summary(manifest, output)
            print("当前浏览器连接不可用；未打开备用浏览器窗口。", file=sys.stderr)
            return 5
        page_url = page_state.get("url") or source_url
        if page_state.get("blocked"):
            manifest = {
                "status": "waiting_login", "platform": platform, "page_url": page_url,
                "source_input": source_url, "elapsed_ms": round((time.perf_counter() - started) * 1000),
                "browser_route": browser_route,
                "download": {"main": 0, "detail": 0, "skipped": 0}, "records": [],
                "message": "当前浏览器商品页需要使用者登录、验证码或风险确认。",
            }
            write_outputs(output, manifest)
            print_result_summary(manifest, output)
            return 2
        status, counts = download_candidates(
            candidates=page_state.get("candidates") or [],
            page_url=page_url,
            source_url=source_url,
            platform=platform,
            output=output,
            main_dir=main_dir,
            detail_dir=detail_dir,
            local_root=None,
            request_context=None,
            browser_route=browser_route,
            allowed_local_origin=args.webbridge_endpoint if getattr(args, "allow_local_assets", False) else None,
            max_main=args.max_main,
            max_detail=args.max_detail,
            started=started,
        )
    else:
        try:
            from playwright.sync_api import sync_playwright
        except ImportError:
            print("缺少 Python Playwright。请运行：pip install playwright；然后运行：playwright install chromium", file=sys.stderr)
            return 4

        with sync_playwright() as playwright:
            if args.headless:
                browser, context, browser_route = launch_browser_context(playwright, headless=True, profile=None)
            else:
                profile = Path(args.profile_dir).resolve() if args.profile_dir else Path.home() / "Documents" / "EcommerceAIWorkstation" / "browser-profile" / "product-assets"
                profile.mkdir(parents=True, exist_ok=True)
                browser, context, browser_route = launch_browser_context(playwright, headless=False, profile=profile)
            try:
                page = context.pages[0] if context.pages else context.new_page()
                page.goto(source_url, wait_until="domcontentloaded", timeout=60_000)
                time.sleep(1)

                if looks_blocked(page):
                    if args.headless or not wait_for_user_login(page, args.login_timeout):
                        manifest = {
                            "status": "waiting_login", "platform": platform, "page_url": page.url,
                            "source_input": source_url, "elapsed_ms": round((time.perf_counter() - started) * 1000),
                            "browser_route": browser_route,
                            "download": {"main": 0, "detail": 0, "skipped": 0}, "records": [],
                            "message": "页面需要使用者登录、验证码或风险确认。",
                        }
                        write_outputs(output, manifest)
                        print_result_summary(manifest, output)
                        return 2

                click_detail_entry(page)
                scroll_page(page, args.scroll_rounds)
                status, counts = download_candidates(
                    candidates=page.evaluate(EXTRACT_JS),
                    page_url=page.url,
                    source_url=source_url,
                    platform=platform,
                    output=output,
                    main_dir=main_dir,
                    detail_dir=detail_dir,
                    local_root=local_root,
                    request_context=context.request,
                    browser_route=browser_route,
                    max_main=args.max_main,
                    max_detail=args.max_detail,
                    started=started,
                )
            finally:
                context.close()
                if browser:
                    browser.close()

    manifest = json.loads((output / "manifest.json").read_text(encoding="utf-8"))
    print_result_summary(manifest, output)
    return 0 if status == "completed" else 3


def main() -> None:
    args = parser().parse_args()
    raise SystemExit(run(args))


if __name__ == "__main__":
    main()

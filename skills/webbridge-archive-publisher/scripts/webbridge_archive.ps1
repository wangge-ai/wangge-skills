param(
  [Parameter(Mandatory = $true)]
  [string]$Url,
  [string]$OutDir = (Join-Path 'D:\codex' ('webbridge-archive-' + (Get-Date -Format 'yyyyMMdd-HHmmss'))),
  [ValidateSet('auto', 'single', 'feishu-wiki')]
  [string]$Mode = 'auto',
  [int]$MaxPages = 0,
  [int]$JpegQuality = 82,
  [switch]$NoScreenshots,
  [switch]$BuildReader,
  [switch]$MakeShareable,
  [string]$Title = '',
  [string]$SessionName = 'webbridge-archive',
  [int]$CommandTimeoutSec = 60,
  [int]$MaxScreenshotFailures = 2,
  [int]$ScreenshotRetries = 1,
  [int]$ScreenshotDelayMs = 700,
  [switch]$ResumeScreenshots
)

$ErrorActionPreference = 'Stop'
[Console]::OutputEncoding = New-Object System.Text.UTF8Encoding($false)
$OutputEncoding = [Console]::OutputEncoding
$Utf8NoBom = New-Object System.Text.UTF8Encoding($false)

New-Item -ItemType Directory -Force -Path $OutDir | Out-Null
$PagesDir = Join-Path $OutDir 'pages'
$ShotDir = Join-Path $OutDir 'screenshots'
New-Item -ItemType Directory -Force -Path $PagesDir | Out-Null
if (-not $NoScreenshots) { New-Item -ItemType Directory -Force -Path $ShotDir | Out-Null }

function Write-Utf8NoBom {
  param([string]$Path, [string]$Text)
  $parent = Split-Path -Parent $Path
  if ($parent) { New-Item -ItemType Directory -Force -Path $parent | Out-Null }
  [System.IO.File]::WriteAllText($Path, $Text, $Utf8NoBom)
}

function ConvertTo-SafeFileName {
  param([string]$Name)
  $safe = $Name -replace '[\\/:*?"<>|]', '_'
  $safe = $safe -replace '\s+', ' '
  $safe = $safe.Trim()
  if ($safe.Length -gt 120) { $safe = $safe.Substring(0, 120).Trim() }
  if (-not $safe) { $safe = 'untitled' }
  return $safe
}

function Start-WebBridgeIfNeeded {
  $exe = Join-Path $env:USERPROFILE '.kimi-webbridge\bin\kimi-webbridge.exe'
  if (Test-Path -LiteralPath $exe) {
    & $exe start | Out-Null
    Start-Sleep -Milliseconds 800
  }
}

function Invoke-WebBridgeCommand {
  param([string]$Action, [hashtable]$ArgHash)
  $body = @{ action = $Action; args = $ArgHash; session = $SessionName }
  $tmp = Join-Path $env:TEMP ('webbridge-req-' + [guid]::NewGuid().ToString() + '.json')
  $json = $body | ConvertTo-Json -Depth 100 -Compress
  [System.IO.File]::WriteAllText($tmp, $json, $Utf8NoBom)
  try {
    $raw = curl.exe --max-time $CommandTimeoutSec -s -X POST 'http://127.0.0.1:10086/command' -H 'Content-Type: application/json' --data-binary "@$tmp"
  } finally {
    Remove-Item -LiteralPath $tmp -Force -ErrorAction SilentlyContinue
  }
  if (-not $raw) { throw "Empty response from WebBridge for action=$Action" }
  $obj = $raw | ConvertFrom-Json
  if (-not $obj.ok) {
    $msg = if ($obj.error.message) { $obj.error.message } else { $raw }
    throw "WebBridge $Action failed: $msg"
  }
  return $obj.data
}

function Invoke-WebBridgeCommandWithStart {
  param([string]$Action, [hashtable]$ArgHash)
  try {
    return Invoke-WebBridgeCommand -Action $Action -ArgHash $ArgHash
  } catch {
    if ($_.Exception.Message -match 'Empty response|Failed to connect|could not connect|refused') {
      Start-WebBridgeIfNeeded
      return Invoke-WebBridgeCommand -Action $Action -ArgHash $ArgHash
    }
    throw
  }
}

function Invoke-WebBridgeEvaluateJson {
  param([string]$Code)
  $data = Invoke-WebBridgeCommandWithStart -Action 'evaluate' -ArgHash @{ code = $Code }
  if ($data.type -ne 'string') { throw "Expected string result from evaluate, got $($data.type)" }
  return $data.value | ConvertFrom-Json
}

function Wait-PageReady {
  param([string]$Contains)
  for ($i = 0; $i -lt 40; $i++) {
    Start-Sleep -Milliseconds 500
    try {
      $state = Invoke-WebBridgeEvaluateJson -Code "(() => JSON.stringify({url: location.href, title: document.title, ready: document.readyState}))()"
      if (-not $Contains -or $state.url -like "*$Contains*" -or $state.ready -eq 'complete') { return $state }
    } catch {
      Start-Sleep -Milliseconds 500
    }
  }
  throw "Timed out waiting for page ready"
}

$detectModeCode = @'
(() => {
  const host = location.host;
  const feishuNodes = document.querySelectorAll('.workspace-tree-view-node[data-node-uid]').length;
  return JSON.stringify({
    url: location.href,
    title: document.title,
    host,
    feishuNodes,
    isFeishuWiki: /feishu\.cn|larksuite\.com/.test(host) && feishuNodes > 0
  });
})()
'@

$collectFeishuManifestCode = @'
(async () => {
  const clean = (s) => (s || '')
    .replace(/[\u200B-\u200F\u202A-\u202E\u2060-\u206F\uFEFF]/g, '')
    .replace(/\s+/g, ' ')
    .trim();
  const wait = (ms) => new Promise(r => setTimeout(r, ms));
  const sidebar = document.querySelector('.sidebar-styled__ScrollableContainer-czoANO')
    || document.querySelector('.workspace-scroll-area')
    || document.querySelector('.workspace-next-sidebar-wrapper')
    || document.scrollingElement;
  const items = new Map();
  const parseUid = (uid) => {
    const m = String(uid || '').match(/(?:^|&)wikiToken=([^&]+)/);
    return m ? decodeURIComponent(m[1]) : '';
  };
  const parsePos = (pos) => String(pos || '').split(',').map(x => Number(x)).filter(x => Number.isFinite(x));
  const collect = () => {
    document.querySelectorAll('.workspace-tree-view-node[data-node-uid]').forEach(node => {
      const title = clean(node.innerText || node.textContent);
      const uid = node.getAttribute('data-node-uid') || '';
      const wikiToken = parseUid(uid);
      if (!title || !wikiToken) return;
      const posText = node.getAttribute('data-node-pos') || '';
      items.set(wikiToken, {
        title,
        wikiToken,
        url: `${location.origin}/wiki/${wikiToken}`,
        posText,
        pos: parsePos(posText),
        level: node.getAttribute('data-node-level') || ''
      });
    });
  };
  const maxTop = Math.max(0, sidebar.scrollHeight - sidebar.clientHeight);
  const step = Math.max(240, Math.floor(sidebar.clientHeight * 0.55));
  const positions = [];
  for (let y = 0; y <= maxTop; y += step) positions.push(y);
  if (!positions.includes(maxTop)) positions.push(maxTop);
  for (const y of positions) {
    sidebar.scrollTop = y;
    await wait(450);
    collect();
  }
  sidebar.scrollTop = 0;
  await wait(200);
  const arr = Array.from(items.values()).sort((a, b) => {
    const al = a.pos.length ? a.pos[a.pos.length - 1] : 0;
    const bl = b.pos.length ? b.pos[b.pos.length - 1] : 0;
    return al - bl || a.title.localeCompare(b.title, 'zh-Hans-CN');
  }).map((item, index) => ({ ...item, index: index + 1 }));
  return JSON.stringify({
    pageTitle: clean(document.title),
    pageUrl: location.href,
    mode: 'feishu-wiki',
    sidebar: { clientHeight: sidebar.clientHeight, scrollHeight: sidebar.scrollHeight, maxTop, sampledPositions: positions.length },
    count: arr.length,
    items: arr
  });
})()
'@

$singleManifestCode = @'
(() => {
  const clean = (s) => (s || '').replace(/\s+/g, ' ').trim();
  return JSON.stringify({
    pageTitle: clean(document.title),
    pageUrl: location.href,
    mode: 'single',
    count: 1,
    items: [{ index: 1, title: clean(document.title) || location.href, url: location.href, wikiToken: '', posText: '', pos: [], level: '' }]
  });
})()
'@

$extractPageCode = @'
(async () => {
  const cleanLine = (s) => (s || '')
    .replace(/[\u200B-\u200F\u202A-\u202E\u2060-\u206F\uFEFF]/g, '')
    .replace(/[ \t]+/g, ' ')
    .trim();
  const wait = (ms) => new Promise(r => setTimeout(r, ms));
  const container = document.querySelector('.bear-web-x-container')
    || document.querySelector('main')
    || document.scrollingElement;
  const seen = new Set();
  const lines = [];
  const collect = () => {
    const raw = container.innerText || document.body.innerText || '';
    for (const line of raw.split('\n').map(cleanLine).filter(Boolean)) {
      if (!seen.has(line)) {
        seen.add(line);
        lines.push(line);
      }
    }
  };
  const maxTop = Math.max(0, container.scrollHeight - container.clientHeight);
  const step = Math.max(500, Math.floor(container.clientHeight * 0.75));
  const positions = [];
  for (let y = 0; y <= maxTop; y += step) positions.push(y);
  if (!positions.includes(maxTop)) positions.push(maxTop);
  for (const y of positions) {
    container.scrollTop = y;
    await wait(550);
    collect();
  }
  container.scrollTop = 0;
  await wait(150);
  return JSON.stringify({
    title: cleanLine(document.title.replace(/\s*-\s*飞书云文档$/, '')),
    url: location.href,
    extractedAt: new Date().toISOString(),
    scroll: { clientHeight: container.clientHeight, scrollHeight: container.scrollHeight, maxTop, samples: positions.length },
    lineCount: lines.length,
    textLength: lines.join('\n').length,
    imageCount: container.querySelectorAll('img').length,
    text: lines.join('\n')
  });
})()
'@

$measureCode = @'
(() => {
  const container = document.querySelector('.bear-web-x-container')
    || document.querySelector('main')
    || document.scrollingElement;
  const maxTop = Math.max(0, container.scrollHeight - container.clientHeight);
  const step = Math.max(580, Math.floor(container.clientHeight * 0.78));
  const positions = [];
  for (let y = 0; y <= maxTop; y += step) positions.push(y);
  if (!positions.includes(maxTop)) positions.push(maxTop);
  return JSON.stringify({
    title: document.title,
    url: location.href,
    clientHeight: container.clientHeight,
    scrollHeight: container.scrollHeight,
    maxTop,
    positions,
    imageCount: container.querySelectorAll('img').length
  });
})()
'@

function Set-ScrollCode {
  param([int]$Y)
  return "(() => { const c = document.querySelector('.bear-web-x-container') || document.querySelector('main') || document.scrollingElement; c.scrollTop = $Y; return JSON.stringify({scrollTop:c.scrollTop, scrollHeight:c.scrollHeight}); })()"
}

Write-Host "Opening URL..."
Invoke-WebBridgeCommandWithStart -Action 'navigate' -ArgHash @{ url = $Url; newTab = $false; group_title = '网页归档' } | Out-Null
Wait-PageReady -Contains '' | Out-Null

$detected = Invoke-WebBridgeEvaluateJson -Code $detectModeCode
$actualMode = $Mode
if ($Mode -eq 'auto') {
  if ($detected.isFeishuWiki) { $actualMode = 'feishu-wiki' } else { $actualMode = 'single' }
}

Write-Host ("Archive mode: {0}" -f $actualMode)
if ($actualMode -eq 'feishu-wiki') {
  $manifest = Invoke-WebBridgeEvaluateJson -Code $collectFeishuManifestCode
} else {
  $manifest = Invoke-WebBridgeEvaluateJson -Code $singleManifestCode
}

$manifestPath = Join-Path $OutDir 'manifest.json'
Write-Utf8NoBom -Path $manifestPath -Text ($manifest | ConvertTo-Json -Depth 100)

$items = @($manifest.items)
if ($MaxPages -gt 0) { $items = @($items | Select-Object -First $MaxPages) }

$results = @()
$i = 0
foreach ($item in $items) {
  $i++
  $index = if ($item.index) { [int]$item.index } else { $i }
  $titleForFile = [string]$item.title
  $safeTitle = ConvertTo-SafeFileName ("{0:D3}-{1}" -f $index, $titleForFile)
  $pagePath = Join-Path $PagesDir ($safeTitle + '.md')
  $jsonPath = Join-Path $PagesDir ($safeTitle + '.json')
  Write-Host ("[{0}/{1}] extract {2}" -f $i, $items.Count, $titleForFile)
  try {
    Invoke-WebBridgeCommandWithStart -Action 'navigate' -ArgHash @{ url = $item.url; newTab = $false } | Out-Null
    Wait-PageReady -Contains ([string]$item.wikiToken) | Out-Null
    Start-Sleep -Milliseconds 500
    $page = Invoke-WebBridgeEvaluateJson -Code $extractPageCode
    $page | Add-Member -NotePropertyName index -NotePropertyValue $index -Force
    $markdown = @(
      "# $($page.title)",
      "",
      "- 来源：$($page.url)",
      "- 原目录标题：$titleForFile",
      "- 抽取时间：$($page.extractedAt)",
      "- 行数：$($page.lineCount)",
      "- 字符数：$($page.textLength)",
      "- 图片节点数：$($page.imageCount)",
      "",
      "## 正文",
      "",
      $page.text
    ) -join "`n"
    Write-Utf8NoBom -Path $pagePath -Text $markdown
    Write-Utf8NoBom -Path $jsonPath -Text ($page | ConvertTo-Json -Depth 80)
    $results += [pscustomobject]@{
      index = $index
      title = $titleForFile
      url = $item.url
      status = 'ok'
      pageFile = $pagePath
      jsonFile = $jsonPath
      lineCount = $page.lineCount
      textLength = $page.textLength
      imageCount = $page.imageCount
      error = ''
    }
  } catch {
    $results += [pscustomobject]@{
      index = $index
      title = $titleForFile
      url = $item.url
      status = 'failed'
      pageFile = $pagePath
      jsonFile = $jsonPath
      lineCount = 0
      textLength = 0
      imageCount = 0
      error = $_.Exception.Message
    }
    Write-Warning ("Extract failed: {0}" -f $_.Exception.Message)
  }
}

Write-Utf8NoBom -Path (Join-Path $OutDir 'crawl-results.json') -Text ($results | ConvertTo-Json -Depth 100)

if (-not $NoScreenshots) {
  $shotResults = @()
  foreach ($row in @($results | Where-Object { $_.status -eq 'ok' })) {
    $pageDir = Join-Path $ShotDir ('{0:D3}' -f [int]$row.index)
    New-Item -ItemType Directory -Force -Path $pageDir | Out-Null
    Write-Host ("[{0}] screenshots {1}" -f $row.index, $row.title)
    try {
      Invoke-WebBridgeCommandWithStart -Action 'navigate' -ArgHash @{ url = $row.url; newTab = $false } | Out-Null
      Wait-PageReady -Contains '' | Out-Null
      $measure = Invoke-WebBridgeEvaluateJson -Code $measureCode
      $shots = @()
      $shotIndex = 0
      $shotFailures = @()
      foreach ($pos in @($measure.positions)) {
        $shotIndex++
        $shotPath = Join-Path $pageDir ('{0:D3}-{1:D2}.jpg' -f [int]$row.index, $shotIndex)
        if ($ResumeScreenshots -and (Test-Path -LiteralPath $shotPath)) {
          $existing = Get-Item -LiteralPath $shotPath -ErrorAction SilentlyContinue
          if ($existing -and $existing.Length -gt 0) {
            $shots += [pscustomobject]@{
              index = $shotIndex
              scrollTop = [int]$pos
              path = $shotPath
              sizeBytes = $existing.Length
              status = 'existing'
              attempts = 0
              error = ''
            }
            continue
          }
        }

        $shotOk = $false
        $lastShotError = ''
        $maxAttempts = [Math]::Max(1, 1 + $ScreenshotRetries)
        for ($attempt = 1; $attempt -le $maxAttempts; $attempt++) {
          try {
            Invoke-WebBridgeEvaluateJson -Code (Set-ScrollCode -Y ([int]$pos)) | Out-Null
            Start-Sleep -Milliseconds $ScreenshotDelayMs
            $shot = Invoke-WebBridgeCommandWithStart -Action 'screenshot' -ArgHash @{
              format = 'jpeg'
              quality = $JpegQuality
              path = $shotPath
            }
            $shots += [pscustomobject]@{
              index = $shotIndex
              scrollTop = [int]$pos
              path = $shot.path
              sizeBytes = $shot.sizeBytes
              status = 'ok'
              attempts = $attempt
              error = ''
            }
            $shotOk = $true
            break
          } catch {
            $lastShotError = $_.Exception.Message
            if ($attempt -lt $maxAttempts) {
              Start-Sleep -Milliseconds ([Math]::Max(500, $ScreenshotDelayMs))
            }
          }
        }

        if (-not $shotOk) {
          $shotFailures += [pscustomobject]@{
            index = $shotIndex
            scrollTop = [int]$pos
            status = 'failed'
            attempts = $maxAttempts
            path = $shotPath
            error = $lastShotError
          }
          Write-Warning ("Screenshot {0} failed after {1} attempt(s): {2}" -f $shotIndex, $maxAttempts, $lastShotError)
          if ($shotFailures.Count -ge $MaxScreenshotFailures) { break }
        }
      }
      $shotResults += [pscustomobject]@{
        index = [int]$row.index
        title = $row.title
        url = $row.url
        status = if ($shotFailures.Count -eq 0) { 'ok' } elseif ($shots.Count -gt 0) { 'partial' } else { 'failed' }
        dir = $pageDir
        screenshotCount = $shots.Count
        failureCount = $shotFailures.Count
        imageCount = $measure.imageCount
        scrollHeight = $measure.scrollHeight
        shots = $shots
        failures = $shotFailures
        error = if ($shotFailures.Count -gt 0) { ($shotFailures | Select-Object -First 1).error } else { '' }
      }
    } catch {
      $shotResults += [pscustomobject]@{
        index = [int]$row.index
        title = $row.title
        url = $row.url
        status = 'failed'
        dir = $pageDir
        screenshotCount = 0
        imageCount = 0
        scrollHeight = 0
        shots = @()
        error = $_.Exception.Message
      }
      Write-Warning ("Screenshots failed: {0}" -f $_.Exception.Message)
    }
  }
  Write-Utf8NoBom -Path (Join-Path $OutDir 'screenshot-results.json') -Text ($shotResults | ConvertTo-Json -Depth 100)
}

$ok = @($results | Where-Object { $_.status -eq 'ok' })
$failed = @($results | Where-Object { $_.status -ne 'ok' })
$indexLines = New-Object System.Collections.Generic.List[string]
$indexLines.Add('# WebBridge 归档索引')
$indexLines.Add('')
$indexLines.Add("- 起始 URL：$Url")
$indexLines.Add("- 模式：$actualMode")
$indexLines.Add("- 成功：$($ok.Count)")
$indexLines.Add("- 失败：$($failed.Count)")
$indexLines.Add("- 输出目录：$OutDir")
$indexLines.Add('')
$indexLines.Add('## 页面清单')
$indexLines.Add('')
foreach ($row in $results) {
  $line = "- [$($row.status)] $($row.index). $($row.title) | 行数 $($row.lineCount) | 字符 $($row.textLength) | 图片 $($row.imageCount)"
  if ($row.error) { $line += " | 错误：$($row.error)" }
  $indexLines.Add($line)
}
Write-Utf8NoBom -Path (Join-Path $OutDir 'README.md') -Text ($indexLines -join "`n")

if ($BuildReader) {
  $builder = Join-Path $PSScriptRoot 'build_archive_reader.py'
  $readerTitle = if ($Title) { $Title } elseif ($manifest.pageTitle) { [string]$manifest.pageTitle } else { '网页归档' }
  $titleFile = Join-Path $env:TEMP ('webbridge-title-' + [guid]::NewGuid().ToString() + '.txt')
  [System.IO.File]::WriteAllText($titleFile, $readerTitle, $Utf8NoBom)
  try {
    $args = @($builder, $OutDir, '--title-file', $titleFile, '--zip')
    if ($MakeShareable) { $args += '--shareable' }
    python @args
  } finally {
    Remove-Item -LiteralPath $titleFile -Force -ErrorAction SilentlyContinue
  }
}

Write-Host ("Done. OK={0}, Failed={1}, OutDir={2}" -f $ok.Count, $failed.Count, $OutDir)

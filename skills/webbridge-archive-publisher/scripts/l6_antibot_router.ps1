param(
  [Parameter(Mandatory = $true)]
  [string]$Url,
  [string]$OutDir = (Join-Path 'D:\codex' ('l6-antibot-audit-' + (Get-Date -Format 'yyyyMMdd-HHmmss'))),
  [string]$SessionName = 'webbridge-l6-antibot-audit',
  [int]$CommandTimeoutSec = 60
)

$ErrorActionPreference = 'Stop'
[Console]::OutputEncoding = New-Object System.Text.UTF8Encoding($false)
$OutputEncoding = [Console]::OutputEncoding
$Utf8NoBom = New-Object System.Text.UTF8Encoding($false)
New-Item -ItemType Directory -Force -Path $OutDir | Out-Null

function Write-Utf8NoBom {
  param([string]$Path, [string]$Text)
  $parent = Split-Path -Parent $Path
  if ($parent) { New-Item -ItemType Directory -Force -Path $parent | Out-Null }
  [System.IO.File]::WriteAllText($Path, $Text, $Utf8NoBom)
}

function Invoke-WebBridgeCommand {
  param([string]$Action, [hashtable]$ArgHash)
  $body = @{ action = $Action; args = $ArgHash; session = $SessionName }
  $tmp = Join-Path $env:TEMP ('webbridge-req-' + [guid]::NewGuid().ToString() + '.json')
  [System.IO.File]::WriteAllText($tmp, ($body | ConvertTo-Json -Depth 100 -Compress), $Utf8NoBom)
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

function Get-CommandInfo {
  param([string[]]$Names)
  $rows = @()
  foreach ($name in $Names) {
    $cmd = Get-Command $name -ErrorAction SilentlyContinue
    $rows += [pscustomobject]@{
      command = $name
      found = [bool]$cmd
      path = if ($cmd) { $cmd.Source } else { '' }
    }
  }
  return $rows
}

function Invoke-DirectProbe {
  param([string]$TargetUrl)
  $ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
  $bodyPath = Join-Path $OutDir 'direct-probe-body.html'
  $headerPath = Join-Path $OutDir 'direct-probe-headers.txt'
  $info = [ordered]@{
    ok = $false
    httpCode = 0
    finalUrl = ''
    bytes = 0
    contentType = ''
    challengeMarkers = @()
    error = ''
    bodyPath = $bodyPath
    headerPath = $headerPath
  }
  try {
    $curlInfo = curl.exe -L --max-time 30 -s -A $ua -D $headerPath -o $bodyPath -w '%{http_code}|%{url_effective}|%{size_download}' $TargetUrl
    $parts = [string]$curlInfo -split '\|', 3
    $info.httpCode = [int]$parts[0]
    $info.finalUrl = if ($parts.Count -gt 1) { $parts[1] } else { '' }
    $info.bytes = if ($parts.Count -gt 2) { [int][double]$parts[2] } else { 0 }
    if (Test-Path -LiteralPath $headerPath) {
      $headers = [System.IO.File]::ReadAllText($headerPath, [System.Text.Encoding]::UTF8)
      $ct = [regex]::Match($headers, 'Content-Type:\s*([^\r\n]+)', 'IgnoreCase')
      if ($ct.Success) { $info.contentType = $ct.Groups[1].Value.Trim() }
    }
    $text = ''
    if (Test-Path -LiteralPath $bodyPath) {
      $bytes = [System.IO.File]::ReadAllBytes($bodyPath)
      $text = [System.Text.Encoding]::UTF8.GetString($bytes)
    }
    $markers = @()
    foreach ($pattern in @('captcha', 'verify', 'verification', 'cloudflare', 'cf-challenge', 'access denied', 'login', 'passport', 'accounts/page/login')) {
      if ($text -match $pattern -or $info.finalUrl -match $pattern) { $markers += $pattern }
    }
    $info.challengeMarkers = @($markers | Select-Object -Unique)
    $info.ok = ($info.httpCode -ge 200 -and $info.httpCode -lt 400 -and $info.challengeMarkers.Count -eq 0)
  } catch {
    $info.error = $_.Exception.Message
  }
  return [pscustomobject]$info
}

$evaluateRiskCode = @'
(() => {
  const text = (document.body && document.body.innerText || '').slice(0, 5000);
  const html = (document.documentElement && document.documentElement.innerHTML || '').slice(0, 200000);
  const haystack = `${location.href}\n${document.title}\n${text}\n${html}`.toLowerCase();
  const markerDefs = [
    ['captcha', /captcha|\u9a8c\u8bc1|\u4eba\u673a|\u5b89\u5168\u9a8c\u8bc1|\u6ed1\u5757|verify|verification/i],
    ['cloudflare', /cloudflare|cf-challenge|cf-ray|checking your browser/i],
    ['accessDenied', /access denied|forbidden|\u62d2\u7edd\u8bbf\u95ee|\u65e0\u6743\u8bbf\u95ee|\u6743\u9650\u4e0d\u8db3/i],
    ['login', /login|\u767b\u5f55|sign in|passport|accounts\/page\/login/i],
    ['rateLimit', /too many requests|rate limit|\u8bbf\u95ee\u8fc7\u4e8e\u9891\u7e41|\u8bf7\u6c42\u8fc7\u4e8e\u9891\u7e41/i],
    ['copyProtection', /clipboard|copy|selection|selectstart|contextmenu/i]
  ];
  const markers = {};
  for (const [name, rx] of markerDefs) markers[name] = rx.test(haystack);
  return JSON.stringify({
    url: location.href,
    title: document.title,
    ready: document.readyState,
    userAgent: navigator.userAgent,
    webdriver: navigator.webdriver === true,
    cookieEnabled: navigator.cookieEnabled,
    textLength: text.length,
    textPreview: text.slice(0, 500),
    markers
  });
})()
'@

$tooling = [ordered]@{
  commands = Get-CommandInfo -Names @('browseact', 'playwright', 'node', 'python')
  proxyEnv = [ordered]@{
    HTTP_PROXY = [bool]$env:HTTP_PROXY
    HTTPS_PROXY = [bool]$env:HTTPS_PROXY
    ALL_PROXY = [bool]$env:ALL_PROXY
  }
  kimiStatus = ''
}

try {
  $old = $ErrorActionPreference
  $ErrorActionPreference = 'Continue'
  $tooling.kimiStatus = (& (Join-Path $env:USERPROFILE '.kimi-webbridge\bin\kimi-webbridge.exe') status 2>$null) -join "`n"
  $ErrorActionPreference = $old
} catch {
  $tooling.kimiStatus = $_.Exception.Message
}

$direct = Invoke-DirectProbe -TargetUrl $Url
$browser = [ordered]@{ ok = $false; error = ''; data = $null }
try {
  $nav = Invoke-WebBridgeCommand -Action 'navigate' -ArgHash @{ url = $Url; newTab = $true; group_title = 'L6 anti-bot audit' }
  Start-Sleep -Seconds 2
  $eval = Invoke-WebBridgeCommand -Action 'evaluate' -ArgHash @{ code = $evaluateRiskCode }
  $browser.ok = $true
  $browser.data = [ordered]@{
    navigate = $nav
    risk = ($eval.value | ConvertFrom-Json)
  }
} catch {
  $browser.error = $_.Exception.Message
}

$browseAct = @($tooling.commands | Where-Object { $_.command -eq 'browseact' } | Select-Object -First 1)
$riskMarkers = @()
if ($browser.ok -and $browser.data.risk.markers) {
  $browser.data.risk.markers.PSObject.Properties | ForEach-Object {
    if ($_.Value -eq $true) { $riskMarkers += $_.Name }
  }
}
$hardRiskMarkers = @($riskMarkers | Where-Object { $_ -ne 'copyProtection' })

$recommended = 'L1-direct'
if (-not $direct.ok -and $browser.ok -and $hardRiskMarkers.Count -eq 0) {
  $recommended = 'L2-browser-dom-or-L4-login-session'
  if ($riskMarkers -contains 'copyProtection') {
    $recommended += '+L3-visual-archive'
  }
} elseif ($browser.ok -and $hardRiskMarkers.Count -gt 0) {
  $recommended = 'L6-manual-review-safe-mode'
} elseif (-not $browser.ok) {
  $recommended = 'manual-open-or-fix-webbridge'
}
if ($browseAct -and $browseAct.found) {
  $recommended += '+optional-external-browseact'
}

$result = [ordered]@{
  testedAt = (Get-Date -Format o)
  url = $Url
  directProbe = $direct
  browserProbe = $browser
  riskMarkers = $riskMarkers
  hardRiskMarkers = $hardRiskMarkers
  tooling = $tooling
  recommendedRoute = $recommended
  safetyPolicy = 'No captcha solving, credential extraction, access-control bypass, or proxy evasion was attempted. Use manual takeover or explicit authorized access for protected pages.'
}

$outPath = Join-Path $OutDir 'l6-antibot-router-result.json'
Write-Utf8NoBom -Path $outPath -Text ($result | ConvertTo-Json -Depth 100)
[pscustomobject]@{
  Path = $outPath
  RecommendedRoute = $recommended
  DirectOk = $direct.ok
  BrowserOk = $browser.ok
  RiskMarkers = ($riskMarkers -join ',')
  BrowseActFound = if ($browseAct) { $browseAct.found } else { $false }
} | ConvertTo-Json -Depth 5

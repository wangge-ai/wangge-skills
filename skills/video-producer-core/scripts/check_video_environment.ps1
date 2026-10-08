$ErrorActionPreference = "SilentlyContinue"

function Test-Command {
  param([string]$Name)
  $cmd = Get-Command $Name -ErrorAction SilentlyContinue
  if ($cmd) {
    [PSCustomObject]@{ Tool = $Name; Status = "OK"; Detail = $cmd.Source }
  } else {
    [PSCustomObject]@{ Tool = $Name; Status = "MISSING"; Detail = "" }
  }
}

function Test-PathTool {
  param([string]$Name, [string]$Path)
  if (Test-Path $Path) {
    [PSCustomObject]@{ Tool = $Name; Status = "OK"; Detail = $Path }
  } else {
    [PSCustomObject]@{ Tool = $Name; Status = "MISSING"; Detail = $Path }
  }
}

$rows = @()
$rows += Test-Command "ffmpeg"
$rows += Test-Command "ffprobe"
$rows += Test-Command "node"
$rows += Test-Command "npm"
$rows += Test-Command "python"

$manim = Get-Command "manim" -ErrorAction SilentlyContinue
if ($manim) {
  $rows += [PSCustomObject]@{ Tool = "manim"; Status = "OK"; Detail = $manim.Source }
} elseif (Test-Path ".\.venv\Scripts\manim.exe") {
  $rows += [PSCustomObject]@{ Tool = "manim"; Status = "OK"; Detail = (Resolve-Path ".\.venv\Scripts\manim.exe").Path }
} else {
  $rows += [PSCustomObject]@{ Tool = "manim"; Status = "MISSING"; Detail = "Not on PATH and not found at .\.venv\Scripts\manim.exe" }
}

$chrome = "C:\Program Files\Google\Chrome\Application\chrome.exe"
if (Test-Path $chrome) {
  $rows += [PSCustomObject]@{ Tool = "chrome"; Status = "OK"; Detail = $chrome }
} else {
  $rows += [PSCustomObject]@{ Tool = "chrome"; Status = "MISSING"; Detail = $chrome }
}

$miktex = Get-Command "latex" -ErrorAction SilentlyContinue
if ($miktex) {
  $rows += [PSCustomObject]@{ Tool = "latex"; Status = "OK"; Detail = $miktex.Source }
} elseif (Test-Path "$env:LOCALAPPDATA\Programs\MiKTeX\miktex\bin\x64\latex.exe") {
  $rows += [PSCustomObject]@{ Tool = "latex"; Status = "OK"; Detail = "$env:LOCALAPPDATA\Programs\MiKTeX\miktex\bin\x64\latex.exe" }
} else {
  $rows += [PSCustomObject]@{ Tool = "latex"; Status = "MISSING"; Detail = "MiKTeX/LaTeX not found on PATH" }
}

try {
  Add-Type -AssemblyName System.Speech
  $voices = (New-Object System.Speech.Synthesis.SpeechSynthesizer).GetInstalledVoices() |
    ForEach-Object { $_.VoiceInfo.Name + " (" + $_.VoiceInfo.Culture + ")" }
  $detail = if ($voices) { $voices -join "; " } else { "No installed voices" }
  $status = if ($voices) { "OK" } else { "MISSING" }
  $rows += [PSCustomObject]@{ Tool = "windows-sapi-tts"; Status = $status; Detail = $detail }
} catch {
  $rows += [PSCustomObject]@{ Tool = "windows-sapi-tts"; Status = "MISSING"; Detail = $_.Exception.Message }
}

$rows | Format-Table -AutoSize

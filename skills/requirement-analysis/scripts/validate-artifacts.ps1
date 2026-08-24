param(
    [Parameter(Mandatory = $true)]
    [string]$RunDir,
    [ValidateSet("parse", "extract", "clarify", "review", "aggregate", "all")]
    [string]$Stage = "all"
)

$ErrorActionPreference = "Stop"

function Test-Artifact {
    param(
        [string]$FileName,
        [string[]]$Required,
        [string[]]$Regex = @(),
        [bool]$Optional = $false
    )

    $filePath = Join-Path $resolvedRunDir $FileName
    if (-not (Test-Path -LiteralPath $filePath)) {
        if ($Optional) { return }
        throw "Missing artifact: $filePath"
    }

    $content = Get-Content -Encoding UTF8 -Raw -LiteralPath $filePath
    if ([string]::IsNullOrWhiteSpace($content)) { throw "Empty artifact: $filePath" }

    foreach ($needle in $Required) {
        if (-not $content.Contains($needle)) { throw "$FileName missing required marker: $needle" }
    }
    foreach ($pattern in $Regex) {
        if (-not [regex]::IsMatch($content, $pattern)) { throw "$FileName missing required section matching: $pattern" }
    }

    $placeholderPatterns = @(
        '\[N\]', '\[URL\]', '\[[^\]\r\n]*[\uFF1A\uFF0C][^\]\r\n]*\]',
        '\[\u4F4D\u7F6E\]', '\[\u5177\u4F53\u4F4D\u7F6E\]', '\[\u5177\u4F53\u95EE\u9898\]',
        '\[\u539F\u578B\u4F4D\u7F6E\]', '\[\u63CF\u8FF0\]', '\[\u6458\u8981\]', '\[\u8DEF\u5F84\]',
        '\[\u65F6\u95F4\]', '\[\u5F53\u524D\u65F6\u95F4\]', '\[\u63A2\u7D22\u65F6\u95F4\]',
        '\[\u6587\u4EF6\u540D\]', '\[\u9879\u76EE\u540D\]', '\[\u89D2\u8272\u540D\]', '\[\u9875\u9762\u540D\]'
    )
    foreach ($pattern in $placeholderPatterns) {
        if ([regex]::IsMatch($content, $pattern)) { throw "$FileName contains unresolved placeholder matching: $pattern" }
    }
    foreach ($pattern in @('\*\*\*\s+(Add|Update|Delete)\s+File:', '\*\*\*\s+(Begin|End)\s+Patch')) {
        if ([regex]::IsMatch($content, $pattern)) { throw "$FileName contains stray patch marker matching: $pattern" }
    }
}

$resolvedRunDir = (Resolve-Path -LiteralPath $RunDir).Path
$checks = @{
    parse = @{ FileName = "_parsed-content.md"; Required = @("# ", "## ", "[") }
    extract = @{ FileName = "_extraction.md"; Required = @("# ", "> ", "1.1", "1.2", "1.3", "1.4", "1.5", "2.1", "2.2", "2.3", "2.4") }
    clarify = @{ FileName = "_clarifications.md"; Required = @("# ", "## ", "| # |", "|---"); Regex = @('\u6587\u6863\u6210\u719F\u5EA6', '\u963B\u585E', '\u5F71\u54CD\u8986\u76D6', '\u4F18\u5316\u5EFA\u8BAE') }
    review = @{ FileName = "_review.md"; Required = @("# ", "## ", "| # |", "|---"); Regex = @('\u9700\u6C42\u7C7B\u578B', '\u6D41\u7A0B\u5408\u7406\u6027', '\u91CF\u5316', '\u9690\u6027\u9700\u6C42', '\u53D1\u8A00\u7A3F') }
    aggregate = @{ FileName = "final-report.md"; Required = @("# ", "## "); Regex = @('\u9879\u76EE\u6982[\u89C8\u8FF0]', '\u9700\u6C42\u8403\u53D6', '\u5206\u6790\u4E0E\u8BC4\u4EF7', '\u6F84\u6E05', '\u8BC4\u5BA1') }
}

if ($Stage -eq "all") {
    $params = $checks["parse"]
    Test-Artifact @params -Optional $true
    foreach ($name in @("extract", "clarify", "review", "aggregate")) {
        $params = $checks[$name]
        Test-Artifact @params
    }
} else {
    $params = $checks[$Stage]
    Test-Artifact @params
}

Write-Host "Artifact validation passed ($Stage): $resolvedRunDir"

[CmdletBinding()]
param([switch]$Force)
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
$root = Join-Path $env:LOCALAPPDATA 'ussmarines-security-tools'
$downloads = Join-Path $root 'downloads'
New-Item -ItemType Directory -Force -Path $root,$downloads | Out-Null
function Assert-Hash($Path,$Expected) { if ((Get-FileHash -Algorithm SHA256 $Path).Hash.ToLowerInvariant() -ne $Expected.ToLowerInvariant()) { throw "SHA-256 invalide: $Path" } }
function Get-Verified($Uri,$Path,$Hash) { if ($Force -or -not (Test-Path $Path)) { Invoke-WebRequest -UseBasicParsing $Uri -OutFile $Path }; Assert-Hash $Path $Hash }
function Expand-Clean($Archive,$Destination) { Remove-Item -Recurse -Force -ErrorAction SilentlyContinue $Destination; New-Item -ItemType Directory -Force $Destination | Out-Null; Expand-Archive $Archive $Destination -Force }
Write-Host 'Installation vérifiée des outils de sécurité partagés...' -ForegroundColor Cyan
$ogArchive = Join-Path $downloads 'opengrep-core_windows_x86.zip'
Get-Verified 'https://github.com/opengrep/opengrep/releases/download/v1.22.0/opengrep-core_windows_x86.zip' $ogArchive '53d87310653faf591d410389e04335ca3a2558fe72c3f5a949cd9a71628329e7'
$ogRoot = Join-Path $root 'opengrep-1.22.0'; Expand-Clean $ogArchive $ogRoot
$og = Get-ChildItem $ogRoot -Recurse -File | Where-Object Name -in @('opengrep.exe','opengrep-core.exe') | Select-Object -First 1
if (-not $og) { throw 'Opengrep introuvable.' }
$trivyChecks = Join-Path $downloads 'trivy_0.73.0_checksums.txt'
Get-Verified 'https://github.com/aquasecurity/trivy/releases/download/v0.73.0/trivy_0.73.0_checksums.txt' $trivyChecks '36890275ffdff13025e9bd9fe039724c6e36bf58e698499856b801f619046fe2'
$line = Get-Content $trivyChecks | Where-Object { $_ -match '(?i)windows-64bit\.zip$' } | Select-Object -First 1
$parts = $line -split '\s+',2; $trivyArchive = Join-Path $downloads $parts[1].TrimStart('*')
Get-Verified "https://github.com/aquasecurity/trivy/releases/download/v0.73.0/$($parts[1].TrimStart('*'))" $trivyArchive $parts[0]
$trivyRoot = Join-Path $root 'trivy-0.73.0'; Expand-Clean $trivyArchive $trivyRoot
$trivy = Get-ChildItem $trivyRoot -Recurse -Filter trivy.exe | Select-Object -First 1
$glChecks = Join-Path $downloads 'gitleaks_8.30.1_checksums.txt'
Get-Verified 'https://github.com/gitleaks/gitleaks/releases/download/v8.30.1/gitleaks_8.30.1_checksums.txt' $glChecks '061476c21adaf5441516f96f185c1a4706a83cd6329b9b38762271b3d4a52fae'
$pattern = if ($env:PROCESSOR_ARCHITECTURE -eq 'ARM64') {'(?i)windows_arm64\.zip$'} else {'(?i)windows_x32\.zip$'}
$line = Get-Content $glChecks | Where-Object { $_ -match $pattern } | Select-Object -First 1
$parts = $line -split '\s+',2; $glArchive = Join-Path $downloads $parts[1].TrimStart('*')
Get-Verified "https://github.com/gitleaks/gitleaks/releases/download/v8.30.1/$($parts[1].TrimStart('*'))" $glArchive $parts[0]
$glRoot = Join-Path $root 'gitleaks-8.30.1'; Expand-Clean $glArchive $glRoot
$gl = Get-ChildItem $glRoot -Recurse -Filter gitleaks.exe | Select-Object -First 1
if (-not (Get-Command py -ErrorAction SilentlyContinue)) { throw 'Python avec le lanceur py est requis.' }
$zRoot = Join-Path $root 'zizmor-1.29.0'
if ($Force) { Remove-Item -Recurse -Force -ErrorAction SilentlyContinue $zRoot }
if (-not (Test-Path $zRoot)) { & py -3.12 -m venv $zRoot; if ($LASTEXITCODE) { & py -3 -m venv $zRoot } }
& (Join-Path $zRoot 'Scripts\python.exe') -m pip install --disable-pip-version-check --no-input 'zizmor==1.29.0'
if ($LASTEXITCODE) { throw 'Installation de zizmor impossible.' }
$manifest = @{tools=@{opengrep=@{version='1.22.0';executable=$og.FullName};trivy=@{version='0.73.0';executable=$trivy.FullName};gitleaks=@{version='8.30.1';executable=$gl.FullName};zizmor=@{version='1.29.0';executable=(Join-Path $zRoot 'Scripts\zizmor.exe')}}}
$manifest | ConvertTo-Json -Depth 5 | Set-Content -Encoding UTF8 (Join-Path $root 'installed-tools.json')
Write-Host "Installation terminée dans $root" -ForegroundColor Green

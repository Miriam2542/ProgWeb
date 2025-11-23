<#
Redeploy and sync helper for App Engine (PowerShell)

This script will:
 - change to the project root (where manage.py and app.yaml live)
 - optionally sync local media/ to the configured GCS bucket
 - optionally set public-read ACL on uploaded objects
 - run collectstatic
 - deploy the app using gcloud app deploy

Usage:
  powershell -ExecutionPolicy Bypass -File .\scripts\redeploy_and_sync.ps1

It asks for PROJECT_ID and BUCKET_NAME if not provided via environment variables.
Be sure you are authenticated (gcloud auth login) and that gsutil is available.
#>

param()

function Read-YesNo([string]$msg, [bool]$default=$false){
    $suffix = if ($default) { "[S/n]" } else { "[s/N]" }
    while ($true){
        $r = Read-Host "$msg $suffix"
        if ([string]::IsNullOrWhiteSpace($r)) { return $default }
        if ($r -match '^[sS](im)?$') { return $true }
        if ($r -match '^[nN]') { return $false }
        Write-Host "Resposta inválida, digite 's' ou 'n'." -ForegroundColor Yellow
    }
}

# --- Ler configurações iniciais ---
$project = $env:GCLOUD_PROJECT
$bucket = $env:GS_BUCKET_NAME

if ([string]::IsNullOrWhiteSpace($project)){
    $project = Read-Host "Informe o PROJECT_ID (ex: impactosambientais-476601)"
}
if ([string]::IsNullOrWhiteSpace($bucket)){
    $bucket = Read-Host "Informe o GS_BUCKET_NAME (ex: impactosambientais-476601-media)"
}

# Caminho do projeto (ajuste se necessário)
# Tentamos inferir a partir do diretório do script; se falhar, usamos o diretório atual do PowerShell.
$projectRoot = $null
try {
    if ($PSScriptRoot) {
        $resolved = Resolve-Path (Join-Path $PSScriptRoot "..") -ErrorAction SilentlyContinue
        if ($resolved) { $projectRoot = $resolved.ProviderPath }
    }
} catch {
    # ignore
}

if (-not $projectRoot) {
    try {
        $cwd = Get-Location -ErrorAction SilentlyContinue
        if ($cwd) { $projectRoot = $cwd.ProviderPath }
    } catch {
        # fallback to prompt
    }
}

if (-not $projectRoot){
    $projectRoot = Read-Host "Informe o caminho absoluto para a raiz do projeto (onde está manage.py)"
}

$projectRoot = (Get-Item $projectRoot).ProviderPath

Write-Host "Usando projeto: $project" -ForegroundColor Cyan
Write-Host "Usando bucket: $bucket" -ForegroundColor Cyan
Write-Host "Projeto root: $projectRoot" -ForegroundColor Cyan

# Confirmar
if (-not (Read-YesNo "Confirmar: executar operações no projeto acima?" $true)){
    Write-Host "Cancelado pelo usuário." -ForegroundColor Yellow
    exit 1
}

# Mudar para a raiz do projeto
Push-Location $projectRoot

try{
    # Verificar app.yaml
    if (-not (Test-Path .\app.yaml)){
        Write-Host "ERRO: app.yaml não encontrado na pasta $projectRoot" -ForegroundColor Red
        exit 1
    }

    # Autenticação/seleção de projeto
    Write-Host "Configurando gcloud para o projeto $project" -ForegroundColor Cyan
    & gcloud config set project $project

    # Sincronizar media? (opcional)
    if (Read-YesNo "Deseja sincronizar a pasta local 'media/' para gs://$bucket/? (cópia recursiva)" $false){
        # caminho absoluto para media
        $mediaPath = Join-Path $projectRoot "media\*"
        Write-Host "Sincronizando $mediaPath -> gs://$bucket/ ..." -ForegroundColor Yellow
        & gsutil -m cp -r "$mediaPath" "gs://$bucket/"
        if ($LASTEXITCODE -ne 0){
            Write-Host "Aviso: Ocorreram erros durante o upload para o bucket." -ForegroundColor Red
            if (-not (Read-YesNo "Deseja continuar mesmo assim?" $false)){
                throw "Upload falhou - cancelando deploy"
            }
        }

        if (Read-YesNo "Deseja definir ACL pública (public-read) recursivamente no bucket?" $false){
            Write-Host "Definindo ACL pública recursiva em gs://$bucket/ ..." -ForegroundColor Yellow
            & gsutil -m acl set -R -a public-read "gs://$bucket/"
            if ($LASTEXITCODE -ne 0){
                Write-Host "Falha ao ajustar ACLs. Verifique permissões e tente manualmente." -ForegroundColor Red
            }
        }
    }

    # Collectstatic
    Write-Host "Executando collectstatic..." -ForegroundColor Cyan
    & py -3 manage.py collectstatic --noinput
    if ($LASTEXITCODE -ne 0){
        Write-Host "collectstatic falhou. Abortando." -ForegroundColor Red
        exit 1
    }

    # Deploy
    Write-Host "Executando gcloud app deploy app.yaml ..." -ForegroundColor Cyan
    & gcloud app deploy .\app.yaml --project=$project
    if ($LASTEXITCODE -ne 0){
        Write-Host "Deploy falhou. Verifique logs acima." -ForegroundColor Red
        exit 1
    }

    Write-Host "Deploy concluído com sucesso." -ForegroundColor Green

    if (Read-YesNo "Deseja abrir o app no navegador agora?" $true){
        & gcloud app browse --project=$project
    }

} catch {
    Write-Host "Erro: $_" -ForegroundColor Red
    exit 1
} finally {
    Pop-Location
}

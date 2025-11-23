<#
Deploy helper for Google App Engine (PowerShell)

Usage:
  - Abra PowerShell (recomendado: Administrador) na raiz do projeto (onde está manage.py)
  - Rode: powershell -ExecutionPolicy Bypass -File .\scripts\deploy_appengine.ps1

O script pede PROJECT_ID e BUCKET_NAME se não forem fornecidos como variáveis de ambiente.
Este script NÃO inclui credenciais; você deve estar autenticado com `gcloud auth login`.
#>

# --- Configurações iniciais (edite se quiser valores fixos) ---
$PROJECT_ID = $env:GCLOUD_PROJECT
$BUCKET_NAME = $env:GS_BUCKET_NAME
$APP_REGION = "southamerica-east1"  # região recomendada
$ASK_CREATE_BUCKET = $true
$ASK_CREATE_APP = $true
$RUN_MIGRATIONS = $false  # por padrão não executa migrations na produção automaticamente

function Prompt-IfEmpty([string]$name, [string]$current){
    if ([string]::IsNullOrWhiteSpace($current)){
        return Read-Host "Informe $name"
    }
    return $current
}

# --- Ler/solicitar valores ---
$PROJECT_ID = Prompt-IfEmpty "PROJECT_ID" $PROJECT_ID
$BUCKET_NAME = Prompt-IfEmpty "GCS BUCKET NAME (ex: my-bucket)" $BUCKET_NAME

Write-Host "Projeto: $PROJECT_ID" -ForegroundColor Cyan
Write-Host "Bucket: $BUCKET_NAME" -ForegroundColor Cyan

# --- 1) Autenticação gcloud ---
Write-Host "Verificando autenticação gcloud..." -ForegroundColor Yellow
$auth = gcloud auth list --format="value(account)" 2>$null
if ([string]::IsNullOrWhiteSpace($auth)){
    Write-Host "Nenhuma conta gcloud encontrada. Abrindo fluxo de login..." -ForegroundColor Yellow
    gcloud auth login
} else {
    Write-Host "Conta autenticada: $auth" -ForegroundColor Green
}

# --- 2) Setar projeto ---
Write-Host "Setando projeto gcloud para $PROJECT_ID" -ForegroundColor Yellow
gcloud config set project $PROJECT_ID

# --- 3) Criar App Engine (se necessário) ---
if ($ASK_CREATE_APP){
    $appExists = gcloud app describe --project=$PROJECT_ID 2>$null
    if ($LASTEXITCODE -ne 0) {
        $ans = Read-Host "App Engine não existe para este projeto. Deseja criar? (s/n)"
        if ($ans -match '^[sS]'){
            Write-Host "Criando App Engine na região $APP_REGION..." -ForegroundColor Yellow
            gcloud app create --project=$PROJECT_ID --region=$APP_REGION
        } else {
            Write-Host "Pulando criação de App Engine (presuma que já exista)." -ForegroundColor Yellow
        }
    } else {
        Write-Host "App Engine já configurado neste projeto." -ForegroundColor Green
    }
}

# --- 4) Criar bucket GCS (opcional) ---
if ($ASK_CREATE_BUCKET){
    Write-Host "Verificando existência do bucket gs://$BUCKET_NAME..." -ForegroundColor Yellow
    gsutil ls -b gs://$BUCKET_NAME 2>$null
    if ($LASTEXITCODE -ne 0) {
        $ans = Read-Host "Bucket não existe. Criar bucket gs://$BUCKET_NAME ? (s/n)"
        if ($ans -match '^[sS]'){
            Write-Host "Criando bucket em $APP_REGION..." -ForegroundColor Yellow
            gsutil mb -l $APP_REGION gs://$BUCKET_NAME
            if ($LASTEXITCODE -eq 0){
                Write-Host "Bucket criado." -ForegroundColor Green
            } else {
                Write-Host "Falha ao criar bucket. Cheque erros acima." -ForegroundColor Red
            }
        } else {
            Write-Host "Pulando criação de bucket." -ForegroundColor Yellow
        }
    } else {
        Write-Host "Bucket existe." -ForegroundColor Green
    }
}

# --- 5) Dar permissão ao App Engine service account para o bucket ---
Write-Host "Concedendo role roles/storage.objectAdmin ao service account do App Engine..." -ForegroundColor Yellow
$sa = "$PROJECT_ID@appspot.gserviceaccount.com"
gcloud projects add-iam-policy-binding $PROJECT_ID `
  --member="serviceAccount:$sa" `
  --role="roles/storage.objectAdmin"

# --- 6) Instalar dependências (local) ---
Write-Host "Instalando dependências locais (pip)..." -ForegroundColor Yellow
python -m pip install -r requirements.txt
if ($LASTEXITCODE -ne 0){
    Write-Host "Falha na instalação de dependências. Corrija e rode o script novamente." -ForegroundColor Red
    exit 1
}

# --- 7) Coletar estáticos ---
Write-Host "Coletando arquivos estáticos para static_gcloud/..." -ForegroundColor Yellow
py -3 manage.py collectstatic --noinput
if ($LASTEXITCODE -ne 0){
    Write-Host "collectstatic falhou. Verifique settings e permissões." -ForegroundColor Red
    exit 1
}

# --- 8) (Opcional) Migrations ---
if ($RUN_MIGRATIONS){
    Write-Host "Executando migrations (ATENÇÃO: isso afetará o DB configurado em settings)" -ForegroundColor Yellow
    $ans = Read-Host "Tem certeza que quer rodar migrations agora? (s/n)"
    if ($ans -match '^[sS]'){
        py -3 manage.py makemigrations
        py -3 manage.py migrate
    } else {
        Write-Host "Pulando migrations." -ForegroundColor Yellow
    }
}

# --- 9) Deploy para App Engine ---
Write-Host "Deploy para App Engine: deploy do app.yaml com env vars (DJANGO_DEBUG=False, GS_BUCKET_NAME)" -ForegroundColor Yellow
$deployCmd = "gcloud app deploy app.yaml --project=$PROJECT_ID --quiet --set-env-vars `"DJANGO_DEBUG=False,GS_BUCKET_NAME=$BUCKET_NAME`""
Write-Host "Executando: $deployCmd" -ForegroundColor Cyan
Invoke-Expression $deployCmd

if ($LASTEXITCODE -ne 0){
    Write-Host "Deploy falhou. Verifique erros acima e logs com 'gcloud app logs tail -s default'" -ForegroundColor Red
    exit 1
}

Write-Host "Deploy concluído (verifique com gcloud app browse)." -ForegroundColor Green

# --- 10) Dicas pós-deploy ---
Write-Host "Dica: use Secret Manager para SECRET_KEY em produção, em vez de passar diretamente via --set-env-vars." -ForegroundColor Cyan
Write-Host "Ver logs: gcloud app logs tail -s default" -ForegroundColor Cyan
Write-Host "Abrir URL do app: gcloud app browse --project=$PROJECT_ID" -ForegroundColor Cyan

# Fim do script

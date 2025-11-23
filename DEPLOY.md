Guia de deploy para Google App Engine (usando GCS para mídia)

Resumo rápido
- Este projeto está preparado para rodar no App Engine (arquivo `app.yaml` com gunicorn e handler de static).
- É necessário usar Cloud Storage para arquivos de mídia (uploads de usuário).

Passos para preparar o deploy

1) Instale as dependências locais e atualize o `requirements.txt` (já foi atualizado neste repositório):

```powershell
pip install -r requirements.txt
```

2) Crie um bucket no Google Cloud Storage:

```bash
# autentique
gcloud auth login
# selecione projeto
gcloud config set project YOUR_PROJECT_ID
# crie bucket (região recomendada: southamerica-east1)
gsutil mb -l southamerica-east1 gs://your-bucket-name
```

3) Conceda permissão ao service account do App Engine para gravar no bucket

```bash
gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
  --member="serviceAccount:YOUR_PROJECT_ID@appspot.gserviceaccount.com" \
  --role="roles/storage.objectAdmin"
```

4) Defina `GS_BUCKET_NAME` no `app.yaml` (ou via `gcloud app deploy --set-env-vars "GS_BUCKET_NAME=your-bucket-name"`).

5) Coletar arquivos estáticos localmente e subir:

```powershell
python manage.py collectstatic --noinput
```

6) Deploy para App Engine:

```bash
gcloud app deploy
```

7) Logs e debug

```bash
gcloud app logs tail -s default
```

Configuração de settings.py (já aplicada no repositório)
- Em `settings.py` foi adicionada uma seção que usa `storages.backends.gcloud.GoogleCloudStorage` quando `DEBUG` é `False`.
- Não coloque credenciais sensíveis no repositório. Utilize variáveis de ambiente ou Secret Manager.

Observações de produção
- Defina `DEBUG=False` em produção.
- Use Secret Manager para `SECRET_KEY` e outras credenciais.
- Considere usar Cloud CDN ou um bucket público configurado via CDN para servir mídia estaticamente.

Se quiser, eu posso:
- Incluir um snippet pronto para `django-storages` com `GS_PROJECT`, `GS_CREDENTIALS` usando `google.oauth2.service_account.Credentials` e exemplo de `credentials.json` (mas NÃO com credenciais reais no repo
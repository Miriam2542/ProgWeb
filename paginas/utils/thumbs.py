import logging
import os
import json
from io import BytesIO
from concurrent.futures import ThreadPoolExecutor
from django.core.files.base import ContentFile
from django.conf import settings
from PIL import Image

try:
    from google.cloud import tasks_v2
    _HAS_TASKS = True
except Exception:
    _HAS_TASKS = False

logger = logging.getLogger(__name__)

# executor global para enfileirar jobs leves de thumbnail
_executor = ThreadPoolExecutor(max_workers=2)


def generate_thumbnail(noticia_pk: int) -> None:
    """Gera um thumbnail para a Noticia com id `noticia_pk`.

    Essa função importa o modelo dinamicamente para evitar import circular
    quando usada a partir de `paginas.models`.
    """
    try:
        from paginas.models import Noticia

        noticia = Noticia.objects.get(pk=noticia_pk)
        if not noticia.imagem:
            return

        # abre via file-like (compatível com GCS/django-storages)
        noticia.imagem.open()
        img = Image.open(noticia.imagem)
        img = img.convert("RGB")
        img.thumbnail((300, 200))

        thumb_io = BytesIO()
        img.save(thumb_io, format="JPEG", quality=85)

        base_name = os.path.basename(noticia.imagem.name)
        thumb_name = f"thumb_{base_name}.jpg"

        # Nem sempre o campo `imagem_thumb` existe (pode ter sido removido por migração).
        # Checamos com hasattr para evitar que o ORM tente selecionar uma coluna inexistente
        # (erro típico: "coluna paginas_noticia.imagem_thumb não existe").
        if hasattr(noticia, 'imagem_thumb'):
            try:
                noticia.imagem_thumb.save(thumb_name, ContentFile(thumb_io.getvalue()), save=False)
                noticia.imagem.close()
                noticia.save(update_fields=["imagem_thumb"]) 
            except Exception:
                # Se falhar ao salvar thumbnail, logue e continue sem quebrar a geração
                logger.exception("Falha ao salvar imagem_thumb para Noticia %s", noticia_pk)
        else:
            # Se não existe o campo de thumb, apenas feche o arquivo fonte e finalize.
            try:
                noticia.imagem.close()
            except Exception:
                logger.debug("Fechar imagem original falhou para Noticia %s", noticia_pk)
    except Exception:
        logger.exception("Erro ao gerar thumbnail para Noticia %s", noticia_pk)


def schedule_thumbnail(noticia_pk: int) -> None:
    """Agendar geração de thumbnail em background (fire-and-forget).

    Observação: para cargas maiores, prefira um worker externo (Cloud Tasks,
    Celery, Cloud Functions) em vez de ThreadPoolExecutor local.
    """
    # Tentar enfileirar via Cloud Tasks se disponível e configurado
    queue_name = getattr(settings, 'CLOUD_TASKS_QUEUE', None)
    location = getattr(settings, 'CLOUD_TASKS_LOCATION', None)
    project = getattr(settings, 'GCP_PROJECT', None) or getattr(settings, 'GOOGLE_CLOUD_PROJECT', None)
    handler_url_base = getattr(settings, 'TASKS_HANDLER_URL', None)
    handler_secret = getattr(settings, 'TASKS_HANDLER_SECRET', None)

    if _HAS_TASKS and queue_name and location and project and handler_url_base and handler_secret:
        try:
            client = tasks_v2.CloudTasksClient()
            parent = client.queue_path(project, location, queue_name)
            url = f"{handler_url_base.rstrip('/')}/paginas/tasks/generate-thumbnail/{noticia_pk}/"
            payload = json.dumps({"pk": noticia_pk}).encode()

            task = {
                "http_request": {
                    "http_method": tasks_v2.HttpMethod.POST,
                    "url": url,
                    "headers": {"Content-Type": "application/json", "X-Task-Secret": handler_secret},
                    "body": payload,
                }
            }

            client.create_task(parent=parent, task=task)
            logger.info('Queued Cloud Task for thumbnail generation: %s', noticia_pk)
            return
        except Exception:
            logger.exception('Failed to queue Cloud Task for Noticia %s, falling back to local executor', noticia_pk)

    # Fallback local executor
    try:
        _executor.submit(generate_thumbnail, noticia_pk)
    except Exception:
        logger.exception("Falha ao agendar tarefa de thumbnail para Noticia %s", noticia_pk)

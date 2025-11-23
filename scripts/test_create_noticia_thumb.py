import os
import django
from io import BytesIO

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projetopw.settings')
django.setup()

from django.core.files.base import ContentFile
from django.core.files import File
from django.conf import settings
from paginas.models import Noticia, Categoria
from django.contrib.auth.models import User
from PIL import Image

# garantir pasta de media de teste
media_test_dir = os.path.join(settings.BASE_DIR, 'media', 'test_uploads') if hasattr(settings, 'BASE_DIR') else os.path.join(os.getcwd(), 'media', 'test_uploads')
os.makedirs(media_test_dir, exist_ok=True)

# criar imagem de 800x600 vermelha
img_path = os.path.join(media_test_dir, 'test_img.jpg')
img = Image.new('RGB', (800, 600), color=(200, 50, 50))
img.save(img_path, format='JPEG')

# garantir usuário
user, created = User.objects.get_or_create(username='test_thumb_user', defaults={'email':'test@example.com'})
if created:
    user.set_password('test1234')
    user.save()

# garantir categoria
categoria, _ = Categoria.objects.get_or_create(nome='Teste', defaults={'descricao':'Categoria de teste'})

# criar a notícia
with open(img_path, 'rb') as f:
    django_file = File(f)
    noticia = Noticia(titulo='Noticia Teste Thumb', conteudo='Conteudo de teste', categoria=categoria, postado_por=user)
    noticia.imagem.save('test_img.jpg', django_file, save=True)

# recarregar do DB
noticia.refresh_from_db()

print('Noticia ID:', noticia.pk)
print('imagem name:', noticia.imagem.name)
print('imagem_thumb name:', noticia.imagem_thumb.name)

# verificar existência dos arquivos no MEDIA_ROOT
media_root = getattr(settings, 'MEDIA_ROOT', os.path.join(os.getcwd(), 'media'))
img_full = os.path.join(media_root, noticia.imagem.name) if noticia.imagem.name else None
thumb_full = os.path.join(media_root, noticia.imagem_thumb.name) if noticia.imagem_thumb.name else None

print('MEDIA_ROOT:', media_root)
print('imagem exists:', os.path.exists(img_full) if img_full else False, img_full)
print('thumb exists:', os.path.exists(thumb_full) if thumb_full else False, thumb_full)

# imprimir URL (se disponível)
try:
    print('imagem url:', noticia.imagem.url)
except Exception as e:
    print('imagem url: (erro)', e)
try:
    print('thumb url:', noticia.imagem_thumb.url)
except Exception as e:
    print('thumb url: (erro)', e)

print('Fim do teste')

import os
import django
from django.conf import settings
from django.core.files.base import ContentFile

# Setup Django
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
import sys
sys.path.append(BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projetopw.settings')

django.setup()

from django.contrib.auth.models import User
from paginas.models import Categoria, Noticia

# Create placeholder image in memory using Pillow
try:
    from PIL import Image, ImageDraw, ImageFont
except Exception as e:
    print('Pillow não está instalado. Instale com: py -3 -m pip install Pillow')
    raise

img_w, img_h = 640, 360
bg_color = (200, 200, 200)
text_color = (40, 40, 40)

img = Image.new('RGB', (img_w, img_h), color=bg_color)
d = ImageDraw.Draw(img)
text = 'Placeholder'
# use default font
try:
    font = ImageFont.truetype('arial.ttf', 36)
except Exception:
    font = ImageFont.load_default()
text_w, text_h = d.textsize(text, font=font)
d.text(((img_w - text_w) / 2, (img_h - text_h) / 2), text, fill=text_color, font=font)

# Save to bytes
from io import BytesIO
buf = BytesIO()
img.save(buf, format='PNG')
buf.seek(0)

# Ensure a user exists
user = User.objects.first()
if not user:
    user = User.objects.create_user(username='testuser', password='testpass')
    print('Usuário criado: testuser')
else:
    print('Usando usuário:', user.username)

# Create or get category
cat, created = Categoria.objects.get_or_create(nome='Categoria Teste', defaults={'descricao':'Criada por script', 'cor':'#007bff'})
if created:
    print('Categoria criada:', cat.nome)
else:
    print('Usando categoria existente:', cat.nome)

# Create Noticia and save image
n = Noticia(titulo='Notícia placeholder', conteudo='Criada com placeholder', categoria=cat, postado_por=user)
file_name = 'placeholder_test.png'
content_file = ContentFile(buf.read(), name=file_name)
n.imagem.save(file_name, content_file, save=True)

print('Notícia criada: pk=', n.pk)
print('imagem.url ->', n.imagem.url)
try:
    print('imagem.path ->', n.imagem.path)
except Exception as e:
    print('imagem.path não disponível (storage remoto?). Exceção:', e)

print('MEDIA_ROOT =', settings.MEDIA_ROOT)
print('MEDIA_URL =', settings.MEDIA_URL)
print('\nScript finalizado.')

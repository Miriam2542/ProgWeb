import os
import django
from django.conf import settings
from django.core.files import File

# Ajuste do caminho e configuração do Django
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projetopw.settings')
import sys
sys.path.append(BASE_DIR)

django.setup()

from django.contrib.auth.models import User
from paginas.models import Categoria, Noticia

# Local do arquivo de teste (existe no repo)
static_logo = os.path.join(BASE_DIR, 'static', 'IMG', 'logodoTCC.png')
if not os.path.exists(static_logo):
    print('Arquivo de imagem de teste não encontrado em:', static_logo)
    sys.exit(1)

# pegar ou criar um usuário
user = User.objects.first()
if not user:
    user = User.objects.create_user(username='testuser', password='testpass')
    print('Usuário criado: testuser / testpass')
else:
    print('Usando usuário existente:', user.username)

# criar ou obter categoria de exemplo
cat, created = Categoria.objects.get_or_create(nome='Categoria Teste', defaults={'descricao': 'Categoria criada por script', 'cor': '#ff5722'})
if created:
    print('Categoria criada:', cat.nome)
else:
    print('Usando categoria existente:', cat.nome)

# criar Noticia de teste
n = Noticia(titulo='Notícia de teste (sem thumb)', conteudo='Conteúdo de teste criado por script.', categoria=cat, postado_por=user)
with open(static_logo, 'rb') as f:
    django_file = File(f)
    n.imagem.save('logo_test.png', django_file, save=True)

print('Notícia criada: pk=', n.pk)
print('imagem.url ->', n.imagem.url)
# tente mostrar o caminho local, se disponível
try:
    print('imagem.path ->', n.imagem.path)
except Exception as e:
    print('Não foi possível obter imagem.path (storage remoto?). Exceção:', e)

# mostrar onde está o MEDIA_ROOT configurado
print('MEDIA_ROOT =', settings.MEDIA_ROOT)
print('MEDIA_URL =', settings.MEDIA_URL)

print('\nFim do script.')

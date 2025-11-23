import os
import sys
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projetopw.settings')
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
import django
django.setup()

from paginas.models import Categoria

cats = Categoria.objects.all().order_by('nome')
print(f'Total categorias: {cats.count()}\n')
for c in cats:
    print(f'PK={c.pk} | nome={c.nome} | descricao={c.descricao} | cor={getattr(c, "cor", None)}')

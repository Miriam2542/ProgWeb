import os
import sys
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projetopw.settings')
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
import django
django.setup()

from paginas.models import Noticia
from django.db.models import Q

qs = Noticia.objects.filter(Q(titulo__icontains='thumb') | Q(titulo__icontains='teste thumb') | Q(titulo__icontains='async'))
print(f'Encontradas {qs.count()} notícias cujo título contém "thumb"/"teste"/"async":\n')
for n in qs.order_by('pk'):
    print(f'PK={n.pk} | titulo={n.titulo!r} | imagem={bool(n.imagem)}')

print('\nSe quiser apagar estes registros, responda "apagar" e eu executo um script que os remove (vou mostrar antes os PKs).')

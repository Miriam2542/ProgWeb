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
if not qs.exists():
    print('Nenhuma notícia de teste encontrada. Nada a deletar.')
else:
    print('Serão deletadas as seguintes notícias:')
    for n in qs.order_by('pk'):
        print(f' - PK={n.pk} | titulo={n.titulo!r}')
    confirm = 'apagar'
    # Já confirmado pelo usuário
    if confirm == 'apagar':
        count = qs.count()
        qs.delete()
        print(f'Foram deletados {count} registro(s).')
    else:
        print('Confirmação não recebida. Nada feito.')

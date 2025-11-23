import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projetopw.settings')
django.setup()

from paginas.models import Noticia

qs = Noticia.objects.filter(titulo__icontains='Teste Thumb Async')
count = qs.count()
if count:
    print(f"Encontradas {count} notícias correspondentes. Removendo...")
    qs.delete()
    print('Remoção concluída.')
else:
    print('Nenhuma notícia com título contendo "Teste Thumb Async" encontrada.')

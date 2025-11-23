import os
import sys
from pathlib import Path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projetopw.settings')
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
import django
django.setup()

from django.conf import settings
from paginas.models import Noticia, Midia


def gather_referenced_files():
    refs = set()
    for n in Noticia.objects.all():
        if n.imagem:
            refs.add(os.path.normpath(os.path.join(settings.MEDIA_ROOT, n.imagem.name)))

    for m in Midia.objects.all():
        if m.imagem:
            refs.add(os.path.normpath(os.path.join(settings.MEDIA_ROOT, m.imagem.name)))
        if m.arquivo_pdf:
            refs.add(os.path.normpath(os.path.join(settings.MEDIA_ROOT, m.arquivo_pdf.name)))

    return refs


def find_media_files():
    media_root = Path(settings.MEDIA_ROOT)
    files = []
    if not media_root.exists():
        return files
    for p in media_root.rglob('*'):
        if p.is_file():
            files.append(p)
    return files


def main(dry_run=True):
    refs = gather_referenced_files()
    media_files = find_media_files()

    orphans = [f for f in media_files if os.path.normpath(str(f)) not in refs]

    if not orphans:
        print('Nenhum arquivo órfão encontrado em', settings.MEDIA_ROOT)
        return

    print('Arquivos órfãos encontrados:')
    for f in orphans:
        print(' -', f)

    if dry_run:
        print('\nDry-run: nenhum arquivo será removido. Para apagar, execute com dry_run=False')
        return

    confirm = input('Deseja apagar os arquivos acima? (sim/nao) ')
    if confirm.lower().startswith('s'):
        removed = 0
        for f in orphans:
            try:
                os.remove(f)
                removed += 1
            except Exception as e:
                print('Erro ao apagar', f, e)
        print(f'Foram removidos {removed} arquivo(s).')
    else:
        print('Operação cancelada.')


if __name__ == '__main__':
    # por padrão apenas lista (safe)
    main(dry_run=True)

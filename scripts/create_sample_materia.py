import os
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projetopw.settings')
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
import django
django.setup()

from django.core.files import File
from paginas.models import Midia


def run():
    # caminhos dos arquivos de exemplo
    img_path = os.path.join(BASE_DIR, 'static', 'IMG', 'impact-Brasil.png')
    pdf_path = os.path.join(BASE_DIR, 'scripts', 'assets', 'sample.pdf')

    if not os.path.exists(img_path):
        print('Imagem de exemplo não encontrada em:', img_path)
        return
    if not os.path.exists(pdf_path):
        print('PDF de exemplo não encontrado em:', pdf_path)
        return

    m = Midia()
    m.titulo = 'Documento de Exemplo'
    m.url = ''
    m.descricao = 'Matéria complementar de teste com imagem e PDF'
    m.fonte = 'Gerado automaticamente'

    with open(img_path, 'rb') as fimg:
        m.imagem.save(os.path.basename(img_path), File(fimg), save=False)

    with open(pdf_path, 'rb') as fpdf:
        m.arquivo_pdf.save(os.path.basename(pdf_path), File(fpdf), save=False)

    m.save()
    print(f'Criada Matéria Complementar de teste: PK={m.pk} | imagem={m.imagem.url} | pdf={m.arquivo_pdf.url}')


if __name__ == '__main__':
    run()

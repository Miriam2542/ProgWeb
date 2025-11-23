import os
import sys
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projetopw.settings')
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
import django
django.setup()

from paginas.models import Categoria

# Linhas definidas pelo usuário: Nome \t NomeCurto \t Descricao \t Hex
linhas = [
    "Biodiversidade e Fauna em Risco\tVerde-oliva\tRepresenta vida, natureza e conservação\t#4C9A2A",
    "Conservação e Recuperação de Biomas\tVerde-floresta\tSimboliza equilíbrio e restauração\t#2E7D32",
    "Degradação Ambiental\tMarrom-terra\tRemete à perda e desgaste ambiental\t#8D6E63",
    "Desmatamento\tVermelho-escuro\tAlerta e urgência de destruição ambiental\t#C62828",
    "Educação Ambiental\tVerde-claro\tConhecimento, renovação e esperança\t#81C784",
    "Energias Renováveis e Transição Ecológica\tAmarelo-sol\tEnergia limpa e inovação tecnológica\t#F9A825",
    "Mudanças Climáticas e Aquecimento Global\tAzul-claro\tCéu e atmosfera — foco no clima\t#29B6F6",
    "Políticas Públicas e Legislação Ambiental\tAzul-marinho\tConfiança, estrutura e governança\t#1565C0",
]

created = []
updated = []
for l in linhas:
    parts = [p.strip() for p in l.split('\t')]
    if len(parts) < 4:
        print('Linha inválida:', l)
        continue
    nome, _nomecurto, descricao, hexcode = parts
    obj, created_flag = Categoria.objects.get_or_create(nome=nome, defaults={'descricao': descricao, 'cor': hexcode})
    if created_flag:
        created.append(obj)
        print(f'Criada categoria: {obj.nome} (cor={obj.cor})')
    else:
        changed = False
        if obj.descricao != descricao:
            obj.descricao = descricao
            changed = True
        if (not obj.cor) or (obj.cor.strip().lower() != hexcode.strip().lower()):
            obj.cor = hexcode
            changed = True
        if changed:
            obj.save()
            updated.append(obj)
            print(f'Atualizada categoria: {obj.nome} -> cor={obj.cor}')
        else:
            print(f'Já existente (sem mudanças): {obj.nome}')

print('\nResumo:')
print('Criadas:', len(created))
print('Atualizadas:', len(updated))

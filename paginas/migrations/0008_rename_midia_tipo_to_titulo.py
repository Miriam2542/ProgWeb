# Generated manually to rename field 'tipo' -> 'titulo' on Midia
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('paginas', '0007_midia_arquivo_pdf_midia_imagem_alter_midia_descricao_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='midia',
            old_name='tipo',
            new_name='titulo',
        ),
    ]

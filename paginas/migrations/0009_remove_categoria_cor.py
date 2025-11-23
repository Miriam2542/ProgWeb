# Generated manually to remove field 'cor' from Categoria
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('paginas', '0008_rename_midia_tipo_to_titulo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='categoria',
            name='cor',
        ),
    ]

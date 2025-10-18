# Adjusted for Djongo compatibility: removed unsupported ALTER TYPE operation

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interview', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='candidateprofile',
            name='full_text',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='candidateprofile',
            name='parsed_skills',
            field=models.JSONField(blank=True, null=True),
        ),
        # NOTE: Removing AlterField on 'id' because Djongo doesn't support ALTER COLUMN TYPE.
    ]

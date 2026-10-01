from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_approved_action_has_poster'),
    ]

    operations = [
        migrations.AddField(
            model_name='source',
            name='slug',
            field=models.SlugField(default='', unique=False, verbose_name='identificador'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='source',
            name='slug',
            field=models.SlugField(unique=True, verbose_name='identificador'),
        ),
        migrations.AlterField(
            model_name='source',
            name='method',
            field=models.CharField(choices=[('rss', 'RSS'), ('sitemap', 'Sitemap'), ('html', 'HTML'), ('api', 'API')], max_length=10, verbose_name='método de recolha'),
        ),
    ]

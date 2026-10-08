from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='contactmessage',
            name='mobile_number',
            field=models.CharField(default='', max_length=20),
            preserve_default=False,
        ),
    ]
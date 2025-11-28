# Generated manually to fix FieldDoesNotExist issue

from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    dependencies = [
        ('common', '0003_alter_platforminfo_options_alter_platforms_options_and_more'),
    ]

    operations = [
  
        # work フィールドを追加
        migrations.AddField(
            model_name='platforminfo',
            name='work',
            field=models.ForeignKey(
                to='common.works',
                null=True,  # 既存データが0なら NULL で問題なし
                on_delete=django.db.models.deletion.CASCADE,
                related_name='platform_infos',
                verbose_name='作品',
            ),
        ),

        # unique_together を設定
        migrations.AlterUniqueTogether(
            name='platforminfo',
            unique_together={('platform', 'work')},
        ),
    ]

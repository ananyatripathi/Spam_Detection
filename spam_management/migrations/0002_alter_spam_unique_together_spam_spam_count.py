# spam_management/migrations/0002_add_user_field.py
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    dependencies = [
        ('spam_management', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='spam',
            name='user',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='reported_spam',
                to='accounts.User',
            ),
        ),
        migrations.AlterUniqueTogether(
            name='spam',
            unique_together={('user', 'phone_number')},
        ),
    ]

# Generated by Django 4.0.3 on 2022-04-02 19:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('moneymarket', '0004_alter_client_idproof'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('UID', models.CharField(max_length=15, primary_key='True', serialize=False)),
                ('idProof', models.ImageField(upload_to='Logos/Client_ID')),
                ('DOB', models.DateField()),
                ('address', models.TextField(null='True')),
                ('available_bal', models.PositiveIntegerField(default=0)),
                ('invested_bal', models.PositiveIntegerField(default=0)),
                ('demat_ac', models.IntegerField()),
                ('bank_ac', models.IntegerField()),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Prefer not to say')], default='M', max_length=1)),
            ],
        ),
        migrations.DeleteModel(
            name='Client',
        ),
    ]

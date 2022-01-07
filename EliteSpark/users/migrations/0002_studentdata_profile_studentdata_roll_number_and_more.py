# Generated by Django 4.0 on 2022-01-07 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentdata',
            name='profile',
            field=models.ImageField(default='avatar.png', upload_to='profile/'),
        ),
        migrations.AddField(
            model_name='studentdata',
            name='roll_number',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='studentdata',
            name='standard',
            field=models.CharField(blank=True, choices=[('I', 'I'), ('II', 'II'), ('III', 'III'), ('IV', 'IV'), ('V', 'V'), ('VI', 'VI'), ('VII', 'VII'), ('VIII', 'VIII'), ('IX', 'IX'), ('X', 'X'), ('XI', 'XI'), ('XII', 'XII')], max_length=20, null=True),
        ),
    ]

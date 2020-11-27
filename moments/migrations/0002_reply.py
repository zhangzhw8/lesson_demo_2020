# Generated by Django 2.2.16 on 2020-11-13 10:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('moments', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reply',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.CharField(max_length=100)),
                ('type', models.CharField(choices=[('0', 'like'), ('1', 'comment')], max_length=20)),
                ('text', models.CharField(blank=True, max_length=280, null=True)),
                ('at_person', models.CharField(blank=True, max_length=50, null=True)),
                ('status', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='moments.Status')),
            ],
        ),
    ]

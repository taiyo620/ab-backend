# Generated by Django 3.1.3 on 2020-11-11 02:19

from django.db import migrations, models
import django.db.models.deletion
import webaccountbookapi.storage


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('genre_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Graphs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('graph', models.ImageField(blank=True, storage=webaccountbookapi.storage.OverwriteStorage(), upload_to='images/')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('price', models.IntegerField(default=0)),
                ('purchase_date', models.DateField()),
                ('genre', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webaccountbookapi.genre')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webaccountbookapi.user')),
            ],
        ),
    ]
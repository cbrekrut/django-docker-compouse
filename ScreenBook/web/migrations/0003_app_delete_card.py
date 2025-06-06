# Generated by Django 5.2.1 on 2025-05-30 16:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0002_oscategory_alter_card_os_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='App',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Название')),
                ('main_image', models.ImageField(upload_to='apps/main/', verbose_name='Главная картинка')),
                ('icon', models.ImageField(upload_to='apps/icons/', verbose_name='Иконка')),
                ('app_category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='web.appcategory', verbose_name='Категория приложения')),
                ('os_category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='web.oscategory', verbose_name='Категория OS')),
                ('screen_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='web.screentype', verbose_name='Тип экрана')),
                ('ui_element', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='web.uielement', verbose_name='UI элемент')),
            ],
        ),
        migrations.DeleteModel(
            name='Card',
        ),
    ]

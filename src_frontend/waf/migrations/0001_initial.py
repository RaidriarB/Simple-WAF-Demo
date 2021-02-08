# Generated by Django 3.1.6 on 2021-02-05 21:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

	initial = True

	dependencies = [
	]

	operations = [
		migrations.CreateModel(
			name='Log',
			fields=[
				('id', models.AutoField(primary_key=True, serialize=False, unique=True, verbose_name='id')),
				('time', models.TextField(default='')),
				('ip', models.TextField(default='')),
				('url', models.TextField(default='')),
				('action', models.TextField(default='')),
			],
		),
		migrations.CreateModel(
			name='Rule',
			fields=[
				('id', models.AutoField(primary_key=True, serialize=False, unique=True, verbose_name='id')),
				('content', models.TextField(default='', verbose_name='content')),
				('description', models.TextField(default='', verbose_name='description')),
				('action', models.TextField(default='', verbose_name='action')),
			],
		),
		migrations.CreateModel(
			name='Fulllog',
			fields=[
				('id', models.AutoField(primary_key=True, serialize=False, unique=True, verbose_name='id')),
				('content', models.TextField(default='', verbose_name='content')),
				('log', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='waf.log')),
			],
		),
	]

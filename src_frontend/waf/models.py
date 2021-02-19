
from django.db import models


class Rule(models.Model):
	id = models.AutoField('id', primary_key=True, unique=True)
	content = models.TextField('content', default='')
	description = models.TextField('description', default='')
	action = models.TextField('action', default='')

class Log(models.Model):
	id = models.AutoField("id", primary_key=True, unique=True)
	time = models.TextField(default='')
	ip = models.TextField(default='')
	url = models.TextField(default='')
	action = models.TextField(default='')

class Fulllog(models.Model):
	id = models.AutoField('id', primary_key=True, unique=True)
	log = models.ForeignKey(on_delete=models.CASCADE, to='Log')
	content = models.TextField('content', default='')

class Whitelist(models.Model):
	# 使用*作为通配
	id = models.AutoField('id', primary_key=True, unique=True)
	url = models.TextField(default='',blank=False)
	ip = models.TextField(default='',blank=False)

class Blacklist(models.Model):
	# 使用*作为通配
	id = models.AutoField('id', primary_key=True, unique=True)
	url = models.TextField(default='',blank=False)
	ip = models.TextField(default='',blank=False)
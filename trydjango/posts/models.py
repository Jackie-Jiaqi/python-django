# coding:utf-8
from __future__ import unicode_literals


from django.db import models
from django.urls import reverse


class Bugs(models.Model):
    commonname = models.CharField(max_length=32)
    academicname = models.CharField(max_length=64)
    size = models.CharField(max_length=32)
    bodycolor = models.CharField(max_length=64)
    targetfood = models.CharField(max_length=256)
    description = models.CharField(max_length=2048)

    def __str__(self):
        return self.commonname


class Post(models.Model):
    title = models.CharField(max_length=120)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now=False,auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    image = models.FileField(null=True,blank=True)
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('posts:detail',kwargs={'id':self.id})


    def get_absolute_url_result(self):
        return reverse('posts:result',kwargs={'id':self.id})

    def get_absolute_url_form(self):
        return reverse('posts:form',kwargs={'id':self.id})

    def get_absolute_url_QR(self):
        return reverse('posts:detail2',kwargs={'id':self.id})

    def get_absolute_url_QRresult(self):
        return reverse('posts:QRresult',kwargs={'id':self.id})


    # Create your models here


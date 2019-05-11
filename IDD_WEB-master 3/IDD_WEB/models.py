from django.db import models
from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import NON_FIELD_ERRORS
from django.contrib.auth.models import *
from .validators import *


# Create MongoDB model
class MongoConn(models.Model):
    dbname = models.TextField(max_length=50, null=False)
    auth_collection = models.TextField(max_length=50, null=False)
    username = models.TextField(max_length=50, null=False)
    password = models.TextField(max_length=50, null=False)
    ip = models.TextField(max_length=50, null=False)
    ssl = models.BooleanField(default=False)
    port = models.IntegerField(null=False)


class MongoForm(forms.ModelForm):
    dbname = forms.CharField(widget=forms.TextInput(attrs={'type': 'text', 'id':'mongo-form-dbname', 'name':'mongo-form-dbname', 'value':"", 'class':'form-control'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'type': 'text', 'id':'mongo-form-username', 'name':'mongo-form-username', 'value':"", 'class':'form-control'}))
    password = forms.CharField(widget=forms.TextInput(attrs={'type': 'text', 'id':'mongo-form-password', 'name':'mongo-form-password', 'value':"", 'class':'form-control'}))
    ip = forms.CharField(widget=forms.TextInput(attrs={'type': 'text', 'id':'mongo-form-ip', 'name':'mongo-form-ip', 'value':"127.0.0.1", 'class':'form-control'}))
    port = forms.IntegerField(widget=forms.TextInput(attrs={'type': 'text', 'id':'mongo-form-port', 'name':'mongo-form-port', 'value':"", 'class':'form-control'}))
    auth_collection = forms.CharField(widget=forms.TextInput( attrs={'type': 'text', 'id': 'mongo-form-auth_collection', 'name': 'mongo-form-auth_collection', 'value': "admin",'class': 'form-control'}))

    class Meta:
        model = MongoConn
        fields = ('dbname', 'username', 'password', 'ip', 'port')
        error_messages = {
            NON_FIELD_ERRORS: {
                'unique_together': "%(model_name)s's %(field_labels)s are not unique.",
            }
        }


class CSVConn(models.Model):
    filename = models.TextField(max_length=100, null=False)
    document = models.FileField(upload_to='documents/csv/', null=False, validators=[validate_csv_extension])
    document_upload_date = models.DateTimeField(auto_now_add=True)


class CSVForm(forms.ModelForm):
    filename = forms.CharField(widget=forms.TextInput(attrs={'type': 'text', 'id':'csv-form-filename', 'name':'csv-form-filename', 'value':"", 'class':'form-control'}))
    document = forms.FileField(widget=forms.FileInput(attrs={'type': 'file', 'id':'csv-form-document', 'name':'csv-form-document', 'value':".csv file", 'class':'form-control'}))

    class Meta:
        model = CSVConn
        fields = ('filename', 'document')
        error_messages = {
            NON_FIELD_ERRORS: {
                'unique_together': "%(model_name)s's %(field_labels)s are not unique.",
            }
        }


class JSONConn(models.Model):
    filename = models.TextField(max_length=100, null=False)
    document = models.FileField(upload_to='documents/json/', null=False, validators=[validate_json_extension])
    document_upload_date = models.DateTimeField(auto_now_add=True)


class JSONForm(forms.ModelForm):
    filename = forms.CharField(widget=forms.TextInput(attrs={'type': 'text', 'id': 'json-form-filename', 'name': 'json-form-filename', 'value': "", 'class': 'form-control'}))
    document = forms.FileField(widget=forms.FileInput(attrs={'type': 'file', 'id': 'json-form-document', 'name': 'json-form-document', 'value': ".json file", 'class': 'form-control'}))

    class Meta:
        model = JSONConn
        fields = ('filename', 'document')
        error_messages = {
            NON_FIELD_ERRORS: {
                'unique_together': "%(model_name)s's %(field_labels)s are not unique.",
            }
        }


class EXCELConn(models.Model):
    filename = models.TextField(max_length=100, null=False)
    document = models.FileField(upload_to='documents/excel/', null=False, validators=[validate_excel_extension])
    document_upload_date = models.DateTimeField(auto_now_add=True)


class EXCELForm(forms.ModelForm):
    filename = forms.CharField(widget=forms.TextInput(attrs={'type': 'text', 'id': 'excel-form-filename', 'name': 'excel-form-filename', 'value': "", 'class': 'form-control'}))
    document = forms.FileField(widget=forms.FileInput(attrs={'type': 'file', 'id': 'excel-form-document', 'name': 'excel-form-document', 'value': ".excel file", 'class': 'form-control'}))

    class Meta:
        model = EXCELConn
        fields = ('filename', 'document')
        error_messages = {
            NON_FIELD_ERRORS: {
                'unique_together': "%(model_name)s's %(field_labels)s are not unique.",
            }
        }

class Author(models.Model):
    name = models.CharField(max_length=100)

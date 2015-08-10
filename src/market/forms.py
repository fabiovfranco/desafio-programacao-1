# -*- coding: utf-8 -*-

from django import forms

class UploadFileForm(forms.Form):
    file  = forms.FileField()
    autoImport = forms.BooleanField(required=False)
    
class ProcessFileForm(forms.Form):
    batchId = forms.IntegerField()

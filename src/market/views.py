# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.template import RequestContext, loader

from .forms import UploadFileForm
from .models import BatchImport 

from django.views.generic.base import TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from market.forms import ProcessFileForm
import sys

class MarketEndpoint(TemplateView):
    # Create your views here.
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        form = UploadFileForm()
        batchImportList = BatchImport.objects.order_by('-created_date')
        template = loader.get_template('import_index.html')
        context = RequestContext(request, {'batchImportList': batchImportList, 'error': '', 'form': form})
        
        return HttpResponse(template.render(context))

    # Create your views here.
    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        error = ''
        success = ''
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            bi = BatchImport.create(request.FILES['file']);
            success = 'Upload realizado com sucesso.'
            if form.cleaned_data['autoImport']:
                try:
                    bi.import_data()
                    success = 'Importação realizada com sucesso.'
                except:
                    print "Erro ao processar arquivo:", sys.exc_info()[0]
                    success = ''
                    error = "Ocorreu um erro inesperado  ao processar o arquivo. Favor tentar novamente."
    
        batchImportList = BatchImport.objects.order_by('-created_date')
        template = loader.get_template('import_index.html')
        context = RequestContext(request, {'batchImportList': batchImportList, 'success': success, 'error': error, 'form': form})
        
        return HttpResponse(template.render(context))
    
class MarketProcessEndpoint(MarketEndpoint):
    # Create your views here.
    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        error = ''
        success = ''
        form = ProcessFileForm(request.POST)
        if form.is_valid():
            try:
                bi = BatchImport.objects.get(pk=form.cleaned_data['batchId']);
                bi.import_data()
                success = 'Processamento realizado com sucesso.'
            except:
                print "Erro ao processar arquivo:", sys.exc_info()[0]
                success = ''
                error = "Ocorreu um erro inesperado  ao processar o arquivo. Favor tentar novamente."
    
        batchImportList = BatchImport.objects.order_by('-created_date')
        template = loader.get_template('import_index.html')
        context = RequestContext(request, {'batchImportList': batchImportList, 'success': success, 'error': error, 'form': form})
        
        return HttpResponse(template.render(context))

import os, uuid
from datetime import datetime
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, ListView, FormView
from django.views.generic.base import RedirectView
from django.views.generic.edit import CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from sqlalchemy.exc import DBAPIError

from connectors.utils import create_connection
from trigrams import settings
from connectors.models import Connector
from .models import Dataset
from .forms import FileUploadForm, PreviewForm, QueryForm
from .utils import SourceParser


class DatasetListView(LoginRequiredMixin, ListView):
    context_object_name = 'dataset_list'
    login_url = reverse_lazy('accounts:login')

    def get_queryset(self):
        return Dataset.objects.filter(owner=self.request.user)


class DataDeleteView(LoginRequiredMixin, DeleteView):
    model = Dataset
    success_url = reverse_lazy('datasets:list')
    login_url = reverse_lazy('accounts:login')

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        if os.path.exists(os.path.join(settings.MEDIA_ROOT, instance.dataset_name)):
            os.remove(os.path.join(settings.MEDIA_ROOT, instance.dataset_name))
        return super(DataDeleteView, self).delete(request, *args, **kwargs)


class DataDetailView(LoginRequiredMixin, DetailView):
    model = Dataset
    login_url = reverse_lazy('accounts:login')

    def get_context_data(self, **kwargs):
        context = super(DataDetailView, self).get_context_data(**kwargs)
        if self.object.external:
            connection = self.create_connection_from_connector()
            columns, content, dtype, count = SourceParser.query_sql(self.object.query_string, connection)
        else:
            columns, content, dtype, count = SourceParser.read_csv(self.object.dataset_name,
                                                                   sep=self.object.sep,
                                                                   encoding=self.object.encoding)
        context['columns'] = columns
        context['sample'] = content
        context['total_count'] = count
        return context

    def create_connection_from_connector(self):
        connector = self.object.connector
        try:
            return create_connection(db_type=connector.db_type,
                                     host=connector.host,
                                     port=connector.port,
                                     user=connector.user,
                                     password=connector.password,
                                     db_instance=connector.db_instance)
        except DBAPIError as err:
            print(err.args)


class DataImportView(LoginRequiredMixin, FormView):
    template_name = 'datasets/upload_file.html'
    form_class = FileUploadForm
    login_url = reverse_lazy('accounts:login')

    def form_valid(self, form):
        self.save_uploaded_file(self.request.FILES['file'])
        return super(DataImportView, self).form_valid(form)

    def save_uploaded_file(self, f):
        self.display_name, self.extension = os.path.splitext(f.name)
        self.file_name = str(uuid.uuid5(uuid.NAMESPACE_DNS, str(datetime.now())))
        with open(os.path.join(settings.MEDIA_ROOT, self.file_name), 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)

    def get_success_url(self):
        self.extension = self.extension.lower()
        if self.extension == '.txt':
            self.extension = '.csv'
        return reverse('datasets:preview') + '?file_name=' + self.file_name\
               + '&display_name=' + self.display_name + '&extension=' + self.extension


class ImportCancelView(LoginRequiredMixin, RedirectView):
    url = reverse_lazy('datasets:list')
    permanent = False
    login_url = reverse_lazy('accounts:login')

    def get_redirect_url(self, *args, **kwargs):
        if os.path.exists(os.path.join(settings.MEDIA_ROOT, self.request.GET.get('file_name'))):
            os.remove(os.path.join(settings.MEDIA_ROOT, self.request.GET.get('file_name')))
        return super(ImportCancelView, self).get_redirect_url(*args, **kwargs)


class PreviewView(LoginRequiredMixin, CreateView):
    template_name = 'datasets/preview.html'
    login_url = reverse_lazy('accounts:login')
    form_class = PreviewForm

    def get_success_url(self):
        return reverse('datasets:list')

    def get_context_data(self, **kwargs):
        context = super(PreviewView, self).get_context_data(**kwargs)
        context['display_name'] = self.request.GET.get('display_name')
        context['file_name'] = self.request.GET.get('file_name')
        context['dtype'] = self.request.GET.get('dtype')
        context['encoding'] = self.request.GET.get('encoding', 'utf-8')
        context['description'] = self.request.GET.get('description', '')
        if self.request.GET.get('extension') == '.csv':
            context['sep'] = self.request.GET.get('sep', ',')
        else:
            context['sheet_name'] = self.request.GET.get('sheet_name')
        context['extension'] = self.request.GET.get('extension')
        return context

    def form_valid(self, form):
        dataset = form.save(commit=False)
        dataset.dataset_name = self.request.GET.get('file_name')
        dataset.owner = self.request.user
        dataset.save()
        return super(PreviewView, self).form_valid(form)


class QueryView(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('accounts:login')
    template_name = 'datasets/query.html'
    form_class = QueryForm

    def get_success_url(self):
        return reverse('datasets:list')

    def get_context_data(self, **kwargs):
        context = super(QueryView, self).get_context_data(**kwargs)
        context['conn_name'] = self.request.GET.get('conn_name')
        context['display_name'] = self.request.GET.get('display_name') if 'display_name' in self.request.GET else 'Untitiled name'
        return context

    def form_valid(self, form):
        connector = get_object_or_404(Connector, conn_name=self.request.GET.get('conn_name'))
        dataset = form.save(commit=False)
        dataset.connector = connector
        dataset.owner = self.request.user
        dataset.external = True
        dataset.dataset_name = str(uuid.uuid5(uuid.NAMESPACE_DNS, str(datetime.now())))
        dataset.save()
        return super(QueryView, self).form_valid(form)


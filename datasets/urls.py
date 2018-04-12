from django.conf.urls import url
from django.views.generic import TemplateView
from . import views, viewsets

app_name = 'datasets'

urlpatterns = [
    url(r'^$', views.DatasetListView.as_view(), name='list'),
    url(r'^import/$', TemplateView.as_view(template_name='datasets/create_dataset.html'), name='import'),
    url(r'^upload/$', views.DataImportView.as_view(), name="upload"),
    url(r'^connector/$', TemplateView.as_view(template_name='datasets/choose_connector.html'), name="connector"),
    url(r'^api/query/$', viewsets.QueryAPIView.as_view(), name='api_query'),
    url(r'^query/$', views.QueryView.as_view(), name='query'),
    url(r'^api/preview/$', viewsets.PreviewAPIView.as_view(), name="api_preview"),
    url(r'^preview/$', views.PreviewView.as_view(), name="preview"),
    url(r'^preview/cancel/$', views.ImportCancelView.as_view(), name="cancel"),
    url(r'^(?P<pk>\d+)/$', views.DataDetailView.as_view(), name="detail"),
    url(r'^(?P<pk>\d+)/delete/$', views.DataDeleteView.as_view(), name="delete"),
]

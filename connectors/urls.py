from django.conf.urls import url
from . import views, viewsets

app_name = 'connectors'

urlpatterns = [
    url(r'^$', views.ConnectorListView.as_view(), name='list'),
    url(r'^create/$', views.CreateConnectorView.as_view(), name='create'),
    url(r'^(?P<pk>\d+)/$', views.UpdateConnectorView.as_view(), name='update'),
    url(r'^api/$', viewsets.ConnectorAPIView.as_view(), name='api_list'),
]
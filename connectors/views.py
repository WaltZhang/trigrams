from django.urls import reverse_lazy, reverse
from django.views.generic.edit import UpdateView, CreateView
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Connector
from .forms import CreateConnectorForm, UpdateConnectorForm


class ConnectorListView(LoginRequiredMixin, ListView):
    context_object_name = 'connection_list'
    template_name = 'connectors/conn_list.html'
    login_url = reverse_lazy('accounts:login')

    def get_queryset(self):
        return Connector.objects.filter(owner=self.request.user)


class CreateConnectorView(LoginRequiredMixin, CreateView):
    form_class = CreateConnectorForm
    template_name = 'connectors/create_conn.html'
    login_url = reverse_lazy('accounts:login')

    def get_success_url(self):
        return reverse('connectors:list')

    def form_valid(self, form):
        connector = form.save(commit=False)
        connector.owner = self.request.user
        connector.save()
        return super(CreateConnectorView, self).form_valid(form)


class UpdateConnectorView(LoginRequiredMixin, UpdateView):
    model = Connector
    form_class = UpdateConnectorForm
    template_name = 'connectors/conn_detail.html'
    login_url = reverse_lazy('accounts:login')
    success_url = reverse_lazy('connectors:list')


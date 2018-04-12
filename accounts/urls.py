from django.conf.urls import url
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from . import views, forms

app_name = 'accounts'

urlpatterns = [
    url(r'^$', views.HomeView.as_view(), name='home'),
    url(r'^login/$', LoginView.as_view(template_name='accounts/login.html', authentication_form=forms.UserLoginForm), name='login'),
    url(r'^logout/$', LogoutView.as_view(next_page=reverse_lazy('accounts:login')), name='logout'),
    url(r'^register/$', views.RegisterView.as_view(), name='register'),
    url(r'^profile/$', views.ProfileView.as_view(), name='view_profile'),
    url(r'^profile/edit/$', views.EditProfileView.as_view(), name='edit_profile'),
    url(r'^profile/password/$', views.ProfilePasswordChangeView.as_view(), name='change_password'),
]

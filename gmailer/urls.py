from django.urls import path, include
from gmailer import views

app_name = 'gmailer'
urlpatterns = [
    path('', views.paths, name='paths'),
    path('auth', views.auth, name='auth'),
    path('verify', views.verify, name='verify'),
    path('revoke', views.revoke, name='revoke'),
    path('test_send_mail', views.test_send_mail, name='test_send_mail'),
]
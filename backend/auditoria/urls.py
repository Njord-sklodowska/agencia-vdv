from django.urls import path

from .views import LogAuditoriaListView

urlpatterns = [
    path(
        '',
        LogAuditoriaListView.as_view(),
        name='auditoria-list'
    ),
]
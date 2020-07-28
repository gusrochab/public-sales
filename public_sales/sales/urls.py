from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('<int:id>/', views.sales_list, name='sales_list'),
    path('liked/', views.liked, name='liked'),
    path('celery/', views.celery, name='celery')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)


from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('users.urls')),
    path('services/',include('services.urls')),
    path('payment/',include('payment.urls')),
    path('bids/',include('bids.urls')),
    path('reports/',include('breports.urls')),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

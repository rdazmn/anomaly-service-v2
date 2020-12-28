
from django.contrib import admin
from django.urls import path
from anomaly import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('admin/', admin.site.urls),
    path('predictJson',csrf_exempt(views.predictJson),name="SMS Application"),
    path('predictFile',csrf_exempt(views.predictFile),name="SMS File")
]

"""travel_pro URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from travel.views import home_page

error_404_view = 'travel.views.handler404'
error_500_view = 'travel.views.handler500'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('account.urls')),
    path('travel/', include('travel.urls')),
    path('destination/', include('place.urls')),
    path('moderator/', include('moderator.urls')),
    path('blogging/', include('facility.urls')),
    path('', home_page, name='home'),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

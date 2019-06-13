from django.contrib import admin
from django.conf import settings
from django.urls import path,include
# import hello.views as hello


urlpatterns = [
    path('admin/',admin.site.urls),
    path('', include('keiba.urls')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

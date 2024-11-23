from django.conf.urls.static import static  # Remove when removing TODO
from django.contrib import admin
from django.urls import path, include
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path('', include('home.urls')),
    path('', include('dashboard.urls')),
    path("", include("users.urls")),
]

# Serve static files during development
# if settings.DEBUG:
#     urlpatterns += static(settings.STATIC_URL,
#                           document_root=settings.STATIC_ROOT)

urlpatterns += static(settings.MEDIA_URL,
                      document_root=settings.MEDIA_ROOT)

# Add the custom error handlers
# handler404 = 'home.views.handler404'
# handler500 = 'home.views.handler500'
# handler403 = 'home.views.handler403'
# handler400 = 'home.views.handler400'

from django.urls import path
from .views import home, about_us, service, loan, contact

urlpatterns = [
    path('', home, name="home"),
    path('about-us/', about_us, name="about-us"),
    path('services/', service, name="services"),
    path('loan/', loan, name="loan"),
    path('contact/', contact, name="contact"),
]

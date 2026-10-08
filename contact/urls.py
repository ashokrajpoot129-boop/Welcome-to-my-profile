from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.profile, name='profile'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('contact/', views.contact_page, name='contact'),
    path('submit/', views.submit_contact, name='submit_contact'),
    path('api/contact/', views.contact_api, name='contact_api'),
]
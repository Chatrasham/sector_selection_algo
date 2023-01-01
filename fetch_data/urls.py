from django.urls import path
from fetch_data.views import landing_page,fetch_page, clean_page



urlpatterns = [
    path('', landing_page, name='landing_page'),
    path('fetch/', fetch_page, name='fetch_page'),
    path('clean/', clean_page, name='clean_page'),
]

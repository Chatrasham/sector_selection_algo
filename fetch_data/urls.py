from django.urls import path
from fetch_data.views import landing_page,fetch_page, optimize_page, performance_page



urlpatterns = [
    path('', landing_page, name='landing_page'),
    path('fetch/', fetch_page, name='fetch_page'),
    path('optimize/', optimize_page, name='optimize_page'),
    path('performance/', performance_page, name='performance_page'),
]

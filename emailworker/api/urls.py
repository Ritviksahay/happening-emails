from django.urls import path
from .views import process_data, Register
urlpatterns = [
    path('process-data/', process_data, name='process-data'),
    path('registeration-email/', Register, name='registeration-email'),
]

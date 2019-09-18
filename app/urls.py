from django.urls import path

from .views import EventListView, EventCreateView, EventDeleteView, checkout, checkin, EventUpdateView

app_name = 'app'
urlpatterns = [
    path('', EventListView.as_view(), name='list-event'),
    path('create', EventCreateView.as_view(), name='create-event'),
    path('update/<int:pk>', EventUpdateView.as_view(), name='update-event'),
    path('delete/<int:pk>', EventDeleteView.as_view(), name='delete-event'),
    path('checkin', checkin, name='checkin-event'),
    path('checkout/<int:pk>', checkout, name='checkout-event'),
]

from django.urls import path
from .views import (
    GiveKudoView,
    ReceivedKudosListView,
    GivenKudosListView,
    AvailableKudosView,
    FetchUsersListView
)

urlpatterns = [
    path('give-kudos', GiveKudoView.as_view(), name='give-kudo'),
    path('received-kudos', ReceivedKudosListView.as_view(), name='received-kudos'),
    path('given-kudos', GivenKudosListView.as_view(), name='given-kudos'),
    path('available-kudos', AvailableKudosView.as_view(), name='available-kudos'),
    path('fetch-users', FetchUsersListView.as_view(), name = 'fetch-users-list')
]
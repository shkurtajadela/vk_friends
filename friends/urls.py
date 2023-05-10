from django.urls import path, include
from .views import *


urlpatterns = [
    path('send_request/<int:to_user_id>', send_friend_request),
    path('friend_requests', FriendshipRequestListView.as_view()),
    path('incoming_friend_requests', FriendshipIncomingRequestListView.as_view()),
    path('outcoming_friend_requests', FriendshipOutcomingRequestListView.as_view()),
    path('accept_request/<int:from_user_id>', accept_friend_request),
    path('reject_request/<int:from_user_id>', reject_friend_request),
    path('my_friends', FriendshipListViewSet.as_view()),
    path('delete_friend/<int:user_id>', remove_friend),
    path('search_friends', UsersListView.as_view()),
    path('get_status/<int:user_id>', get_friendship_status),
]

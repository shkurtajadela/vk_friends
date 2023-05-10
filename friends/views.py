from rest_framework import permissions, status, generics
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from .models import Friendship, FriendRequest
from .serializers import FriendshipSerializer, FriendRequestsSerializer, UserSerializer
from django.db.models import Q
from rest_framework.decorators import api_view, permission_classes

User = get_user_model()


class UsersListView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return User.objects.all().exclude(id=self.request.user.id).exclude(is_superuser=True)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def send_friend_request(request, to_user_id):
    if int(to_user_id) == request.user.id:
        return Response({'detail': 'You cannot send a friend request to yourself.'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        to_user = User.objects.get(pk=int(to_user_id))
        if to_user.is_superuser:
            return Response({'error': 'Нельзя отправлять заявки на добавление в друзья админу'}, status=status.HTTP_400_BAD_REQUEST)
        FriendRequest.objects.create(from_user=request.user, to_user=to_user)
    except User.DoesNotExist:
        return Response({'error': 'Пользователь не найден'}, status=status.HTTP_404_NOT_FOUND)

    try:
        friendship = Friendship.objects.get(Q(from_user=request.user, to_user=to_user) | Q(from_user=to_user, to_user=request.user))
        if friendship:
            return Response({'detail': 'You are already friends.'})
    except Friendship.DoesNotExist:
        incoming_request = FriendRequest.objects.filter(to_user=request.user, from_user=to_user).first()
        outgoing_request = FriendRequest.objects.filter(to_user=to_user, from_user=request.user).first()

        if incoming_request and outgoing_request:
            incoming_request.delete()
            outgoing_request.delete()
            Friendship.objects.create(from_user=request.user, to_user=to_user)
            return Response(
                {'detail': 'You became friends automatically because the user you requested sent you a request too.'})
        return Response({'detail': 'Friend request sent.'})


@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticated])
def remove_friend(request, user_id):
    try:
        user = request.user
        friend = User.objects.get(id=user_id)
        friendship = Friendship.objects.get(Q(from_user=user, to_user=friend) | Q(from_user=friend, to_user=user))
    except User.DoesNotExist:
        return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
    except Friendship.DoesNotExist:
        return Response({'error': 'This user is not your friend.'}, status=status.HTTP_400_BAD_REQUEST)

    friendship.delete()
    return Response({'success': 'User removed from friends list.'}, status=status.HTTP_200_OK)



class FriendRequestListView(generics.ListAPIView):
    serializer_class = FriendRequestsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return FriendRequest.objects.filter(Q(from_user=self.request.user) | Q(to_user=self.request.user))


class FriendshipIncomingRequestListView(generics.ListAPIView):
    serializer_class = FriendRequestsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return FriendRequest.objects.filter(to_user=self.request.user)


class FriendshipOutcomingRequestListView(generics.ListAPIView):
    serializer_class = FriendRequestsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return FriendRequest.objects.filter(from_user=self.request.user)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def accept_friend_request(request, from_user_id):
    try:
        friend_request = FriendRequest.objects.get(to_user=request.user, from_user__id=from_user_id)
    except FriendRequest.DoesNotExist:
        return Response({'error': 'Request not found.'}, status=status.HTTP_404_NOT_FOUND)

    to_user = User.objects.get(pk=int(from_user_id))
    Friendship.objects.create(from_user=request.user, to_user=to_user)
    friend_request.delete()
    return Response({'success': 'Request was accepted.'}, status=status.HTTP_200_OK)

@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticated])
def reject_friend_request(request, from_user_id):
    try:
        friend_request = FriendRequest.objects.get(to_user=request.user, from_user__id=from_user_id)
    except FriendRequest.DoesNotExist:
        return Response({'error': 'Request not found.'}, status=status.HTTP_404_NOT_FOUND)

    friend_request.delete()
    return Response({'success': 'User request rejected.'}, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_friendship_status(request, user_id):
    user = request.user
    try:
        to_user = User.objects.get(id=user_id)
        if to_user.is_superuser:
            return Response({'error': 'Это админ'},
                            status=status.HTTP_400_BAD_REQUEST)

    except User.DoesNotExist:
        return Response({'detail': 'Could not find user with specified ID.'},
                        status=status.HTTP_400_BAD_REQUEST)

    if user.id == to_user.id:
        return Response({'detail': 'You cannot get the friendship status with yourself.'},
                        status=status.HTTP_400_BAD_REQUEST)

    # Find if exists friendship between users
    friend = Friendship.objects.filter(Q(from_user=user, to_user=to_user) | Q(from_user=to_user, to_user=user))
    if friend:
        return Response({'status': 'friends'})
    friend_request = FriendRequest.objects.filter(
        Q(from_user=user, to_user=to_user) | Q(from_user=to_user, to_user=user)).first()
    if friend_request and friend_request.from_user == user:
        return Response({'status': 'outgoing request'})
    elif friend_request and friend_request.from_user == to_user:
        return Response({'status': 'incoming request'})
    return Response({'status': 'not friends'})


class FriendshipListViewSet(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        friendships = Friendship.objects.filter((Q(to_user=self.request.user) | Q(from_user=self.request.user)))
        results = []
        for friendship in friendships:
            user_id = friendship.from_user.id if friendship.from_user != self.request.user else friendship.to_user.id
            username = friendship.from_user.username if friendship.from_user != self.request.user else friendship.to_user.username
            results.append({'id': user_id, 'username': username})
        return results

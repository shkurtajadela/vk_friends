from django.test import TestCase, Client
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import FriendRequest, Friendship


# test for the model Friend Request
class FriendRequestModelTests(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(username='testuser1', password='password123')
        self.user2 = User.objects.create_user(username='testuser2', password='password123')

    def test_create_friend_request(self):
        request = FriendRequest.objects.create(from_user=self.user1, to_user=self.user2)
        self.assertEqual(FriendRequest.objects.count(), 1)
        self.assertEqual(request.from_user, self.user1)
        self.assertEqual(request.to_user, self.user2)


# send request tests
class SendFriendRequestViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.admin = User.objects.create_superuser(username='admin', email='admin@example.com', password='password')
        self.user1 = User.objects.create_user(username='testuser1', password='password')
        self.user2 = User.objects.create_user(username='testuser2', password='password')
        self.client.force_login(self.user1)

    def test_send_request_to_self(self):
        response = self.client.post(f'/api/send_request/{self.user1.id}')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_send_request_to_admin(self):
        response = self.client.post(f'/api/send_request/{self.admin.id}')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_send_request_to_nonexistent_user(self):
        response = self.client.post('/api/send_request/999')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_send_request_already_friends(self):
        Friendship.objects.create(from_user=self.user1, to_user=self.user2)
        response = self.client.post(f'/api/send_request/{self.user2.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'detail': 'You are already friends.'})

    def test_send_request_incoming_outgoing(self):
        FriendRequest.objects.create(from_user=self.user2, to_user=self.user1)
        response = self.client.post(f'/api/send_request/{self.user2.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {
            'detail': 'You became friends automatically because the user you requested sent you a request too.'})
        friendship = Friendship.objects.filter(from_user=self.user1, to_user=self.user2).first()
        self.assertIsNotNone(friendship)
        incoming_request = FriendRequest.objects.filter(from_user=self.user2, to_user=self.user1).first()
        self.assertIsNone(incoming_request)
        outgoing_request = FriendRequest.objects.filter(from_user=self.user1, to_user=self.user2).first()
        self.assertIsNone(outgoing_request)

    def test_send_request_success(self):
        response = self.client.post(f'/api/send_request/{self.user2.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'detail': 'Friend request sent.'})
        friend_request = FriendRequest.objects.filter(from_user=self.user1, to_user=self.user2).first()
        self.assertIsNotNone(friend_request)


# accept request
class AcceptFriendRequestViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create_user(username='testuser1', password='password')
        self.user2 = User.objects.create_user(username='testuser2', password='password')
        self.friend_request = FriendRequest.objects.create(from_user=self.user2, to_user=self.user1)

    def test_accept_friend_request_success(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.post(f'/api/accept_request/{self.user2.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Friendship.objects.count(), 1)
        self.assertEqual(Friendship.objects.first().from_user, self.user1)
        self.assertEqual(Friendship.objects.first().to_user, self.user2)
        self.assertFalse(FriendRequest.objects.filter(id=self.friend_request.id).exists())
        self.assertDictEqual(response.json(), {'success': 'Request was accepted.'})

    def test_accept_friend_request_not_found(self):
        self.client.force_authenticate(self.user1)
        response = self.client.post(f'/api/accept_request/{self.user2.id + 1}')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertDictEqual(response.json(), {'error': 'Request not found.'})


# reject request
class RejectFriendRequestViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create_user(username='testuser1', password='password')
        self.user2 = User.objects.create_user(username='testuser2', password='password')
        self.friend_request = FriendRequest.objects.create(from_user=self.user2, to_user=self.user1)
        self.client.force_authenticate(user=self.user1)

    def test_reject_friend_request_success(self):
        response = self.client.delete(f'/api/reject_request/{self.user2.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Friendship.objects.count(), 0)
        self.assertDictEqual(response.json(), {'success': 'User request rejected.'})

    def test_reject_friend_request_not_found(self):
        self.client.force_authenticate(self.user1)
        response = self.client.delete(f'/api/reject_request/{self.user2.id + 1}')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertDictEqual(response.json(), {'error': 'Request not found.'})


# delete a friend
class TestRemoveFriendView(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create_user(username='testuser1', password='testpass')
        self.user2 = User.objects.create_user(username='testuser2', password='testpass')
        self.user3 = User.objects.create_user(username='testuser3', password='testpass')
        self.friendship = Friendship.objects.create(from_user=self.user1, to_user=self.user2)
        self.client.force_authenticate(user=self.user1)

    def test_remove_friend_success(self):
        # Test removing an existing friend
        response = self.client.delete(f'/api/delete_friend/{self.user2.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'success': 'User removed from friends list.'})

    def test_remove_not_friend(self):
        # Test removing a non-existing friend
        response = self.client.delete(f'/api/delete_friend/{self.user3.id}')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'error': 'This user is not your friend.'})

    def test_remove_friend_not_found(self):
        # Test removing a non-existing user
        response = self.client.delete('/api/delete_friend/999')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, {'error': 'User not found.'})


# get friendship status
class TestGetFriendshipStatusView(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create_user(username='testuser1', password='testpass1')
        self.user2 = User.objects.create_user(username='testuser2', password='testpass2')
        self.user3 = User.objects.create_superuser(username='testuser3', password='testpass3')

        self.client.force_authenticate(user=self.user1)

    def test_get_friendship_status_success(self):
        # Test if a valid friendship status is returned
        response = self.client.get(f'/api/get_status/{self.user2.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'status': 'not friends'})

        self.friendship = Friendship.objects.create(from_user=self.user1, to_user=self.user2)
        response = self.client.get(f'/api/get_status/{self.user2.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'status': 'friends'})

    def test_get_friendship_status_to_self(self):
        # Test if error is returned when trying to get friendship status with yourself
        response = self.client.get(f'/api/get_status/{self.user1.id}')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'detail': 'You cannot get the friendship status with yourself.'})

    def test_get_friendship_status_to_admin(self):
        # Test if error is returned when trying to get friendship status with a superuser
        response = self.client.get(f'/api/get_status/{self.user3.id}')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'error': 'Это админ'})


# get list of friends
class TestFriendshipListViewSet(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='testuser1', password='password1')
        self.user2 = User.objects.create_user(username='testuser2', password='password2')
        Friendship.objects.create(from_user=self.user1, to_user=self.user2)

        self.client = APIClient()
        self.client.force_authenticate(user=self.user1)

    def test_get(self):
        response = self.client.get('/api/my_friends')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [{'id': self.user2.id, 'username': self.user2.username}])


# get users list
class TestUsersListView(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.force_authenticate(user=self.user)

        self.user2 = User.objects.create_user(username='testuser2', password='testpass2')
        self.user3 = User.objects.create_superuser(username='testuser3', password='testpass3')

    def test_get_queryset(self):
        response = self.client.get('/api/search_friends')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['username'], 'testuser2')


# get incoming requests
class TestFriendshipIncomingRequestListView(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create_user(username='testuser1', password='testpass1')
        self.user2 = User.objects.create_user(username='testuser2', password='testpass2')
        self.friend_request = FriendRequest.objects.create(from_user=self.user1, to_user=self.user2)
        self.client.force_authenticate(user=self.user2)

    def test_get_queryset(self):
        response = self.client.get('/api/incoming_friend_requests')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['username'], 'testuser1')


# get outcoming requests
class TestFriendshipOutcomingRequestListView(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create_user(username='testuser1', password='testpass1')
        self.user2 = User.objects.create_user(username='testuser2', password='testpass2')
        self.friend_request = FriendRequest.objects.create(from_user=self.user1, to_user=self.user2)
        self.client.force_authenticate(user=self.user1)

    def test_get_queryset(self):
        response = self.client.get('/api/outcoming_friend_requests')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['username'], 'testuser2')

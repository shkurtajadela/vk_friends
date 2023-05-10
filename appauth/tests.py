from django.contrib.auth.models import User
from django.test import TestCase
from .serializers import MyTokenObtainPairSerializer, RegisterSerializer


class TestRegisterSerializer(TestCase):
    def test_create_user_with_valid_data(self):
        serializer = RegisterSerializer()
        user_data = {
            'username': 'test_user',
            'password': 'test_password',
            'password2': 'test_password'
        }
        validated_data = serializer.validate(user_data)
        created_user = serializer.create(validated_data)
        self.assertIsInstance(created_user, User)
        self.assertEqual(created_user.username, 'test_user')
        self.assertTrue(created_user.check_password('test_password'))

    def test_create_user_with_password_mismatch(self):
        data = {
            'username': 'testuser',
            'password': 'testpassword',
            'password2': 'testpassword2'
        }
        serializer = RegisterSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(serializer.errors['password'][0], "Password fields didn't match.")


class TestMyTokenObtainPairSerializer(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_get_token(self):
        serializer = MyTokenObtainPairSerializer()
        token = serializer.get_token(self.user)
        self.assertEqual(token['username'], self.user.username)

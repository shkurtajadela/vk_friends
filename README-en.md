### Django backend app friends 
This is a Django application that allows users to register, send friend requests to each other, if the request is accepted, they become friends.

**How to run**
```
git clone https://github.com/shkurtajadela/vk_friends.git
python -m venv venv
venv\Scripts\activate #windows .venv/bin/activate -not windows
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```
Also can be run using docker
```
docker compose up
```

**OpenAPI**

In order to see documentation OpenAPI http://127.0.0.1:8000/docs/swagger/


**Tests**

The appauth (3 tests) and friends (21 tests) folders contain tests for user registration and actions related to sending, accepting, rejecting an application, etc. respectively. To run them
```
python manage.py tests appauth
python manage.py tests friends
```

**The backend service may:**
- register new user: <b>http://127.0.0.1:8000/auth/register/</b> 
  
  <img src="https://github.com/shkurtajadela/vk_friends/blob/main/img/register.png?raw=true" width="300"/>
- send one user a friend request to another <b>http://127.0.0.1:8000/api/send_request/{to_user_id}</b>  
  Example:
  
  <img src="https://github.com/shkurtajadela/vk_friends/blob/main/img/send_suc.png?raw=true" width="300"/>
  
  If user 1 sends an application to user 2, and user 2 sends an application to user 1, then they automatically become friends, their applications are automatically accepted.

  <img src="https://github.com/shkurtajadela/vk_friends/blob/main/img/send_acc.png?raw=true" width="300"/>
- accept a friend request from another user <b>http://127.0.0.1:8000/api/accept_request/{from_user_id}</b>

  <img src="https://github.com/shkurtajadela/vk_friends/blob/main/img/request_acc.png?raw=true" width="300"/>
- refuse a friend request from another user <b>http://127.0.0.1:8000/api/reject_request/{from_user_id}</b>

  <img src="https://github.com/shkurtajadela/vk_friends/blob/main/img/request_rej.png?raw=true" width="300"/>
- view the user's list of outgoing friend requests <b>http://127.0.0.1:8000/api/outcoming_friend_requests</b>

  <img src="https://github.com/shkurtajadela/vk_friends/blob/main/img/outcoming.png?raw=true" width="300"/>
- view the user's list of incoming friend requestsя <b>http://127.0.0.1:8000/api/incoming_friend_requests</b>

  <img src="https://github.com/shkurtajadela/vk_friends/blob/main/img/incoming.png?raw=true" width="300"/>
- get the user friendship status with some other user (nothing / there is an outgoing request / there is an incoming request / already friends) <b>http://127.0.0.1:8000/api/get_status/{user_id}</b>
  
  <img src="https://github.com/shkurtajadela/vk_friends/blob/main/img/status.png?raw=true" width="300"/>
  
- view your list of friends <b>http://127.0.0.1:8000/api/my_friends</b>

  <img src="https://github.com/shkurtajadela/vk_friends/blob/main/img/friends.png?raw=true" width="300"/>
  
- remove another user from your friends list <b>http://127.0.0.1:8000/api/delete_friend/{user_id}</b>

  <img src="https://github.com/shkurtajadela/vk_friends/blob/main/img/delete.png?raw=true" width="300"/>
  
  Here is the list of friends after deleting one of them:
  
  <img src="https://github.com/shkurtajadela/vk_friends/blob/main/img/friends_after.png?raw=true" width="300"/>
  
- see list of users <b>http://127.0.0.1:8000/api/search_friends</b>

  <img src="https://github.com/shkurtajadela/vk_friends/blob/main/img/users.png?raw=true" width="300"/>




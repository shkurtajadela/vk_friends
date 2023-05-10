### Django сервис друзей 
Это приложение Django, которое позволяет пользователям регистрироваться, отправлять друг другу запросы на добавление в друзья, если этот запрос принят, они становятся друзьями.

**Для запуска**
```
git clone https://github.com/shkurtajadela/vk_friends.git
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```
Еще можно запускать через docker
```
docker compose up
```

**Сервис может:**
- зарегистрировать нового пользователя: <b>http://127.0.0.1:8000/auth/register/</b> 
Пример:
<img src="https://github.com/shkurtajadela/vk_friends/blob/main/images/register.png?raw=true" width="300"/>
- отправить одному пользователю заявку в друзья другому <b>http://127.0.0.1:8000/api/send_request/{to_user_id}</b> Если пользователь 1 отправит заявку пользователю 2, а пользователь 2 отправляет заявку пользователю 1, то они автоматически становятся друзьями, их заявки автоматом принимаются. Пример:
<img src="https://github.com/shkurtajadela/vk_friends/blob/main/images/send_suc.png?raw=true" width="300"/>
<img src="https://github.com/shkurtajadela/vk_friends/blob/main/images/send_acc.png?raw=true" width="300"/>
- принять пользователю заявку в друзья от другого пользователя <b>http://127.0.0.1:8000/api/accept_request/{from_user_id}</b>
<img src="https://github.com/shkurtajadela/vk_friends/blob/main/images/request_acc.png?raw=true" width="300"/>
- отклонить пользователю заявку в друзья от другого пользователя <b>http://127.0.0.1:8000/api/reject_request/{from_user_id}</b>
<img src="https://github.com/shkurtajadela/vk_friends/blob/main/images/request_rej.png?raw=true" width="300"/>
- посмотреть пользователю список своих исходящих заявок в друзья <b>http://127.0.0.1:8000/api/outcoming_friend_requests</b>
<img src="https://github.com/shkurtajadela/vk_friends/blob/main/images/outcoming.png?raw=true" width="300"/>
- посмотреть пользователю список своих входящих заявок в друзья <b>http://127.0.0.1:8000/api/incoming_friend_requests</b>
<img src="https://github.com/shkurtajadela/vk_friends/blob/main/images/incoming.png?raw=true" width="300"/>
- получить пользователю статус дружбы с каким-то другим пользователя (нет ничего / есть исхоящая заявка / есть входящая заявка / уже друзья)<b>http://127.0.0.1:8000/api/get_status/{user_id}</b>
<img src="https://github.com/shkurtajadela/vk_friends/blob/main/images/status.png?raw=true" width="300"/>
- посмотреть пользователю список своих друзей <b>http://127.0.0.1:8000/api/my_friends</b>
<img src="https://github.com/shkurtajadela/vk_friends/blob/main/images/friends.png?raw=true" width="300"/>
- удалить пользователю другого пользователя из своих друзей <b>http://127.0.0.1:8000/api/delete_friend/{user_id}</b>

<img src="https://github.com/shkurtajadela/vk_friends/blob/main/images/delete.png?raw=true" width="300"/>
<img src="https://github.com/shkurtajadela/vk_friends/blob/main/images/friends_after.png?raw=true" width="300"/>
- посмотреть список пользователей <b>http://127.0.0.1:8000/api/search_friends</b>

<img src="https://github.com/shkurtajadela/vk_friends/blob/main/images/users.png?raw=true" width="300"/>


**OpenAPI**

Чтобы посмотреть документацию OpenAPI http://127.0.0.1:8000/docs/swagger/


**Tests**

Папки appauth (3 tests) и friends (21 tests) содержат тесты на регистрацию пользователя и на действия, связанные с отправкой, принятием, отклонением заявки и т.д. соответственно. Чтобы их запускать
```
python manage.py tests appauth
python manage.py tests friends
```

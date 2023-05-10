from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class FriendRequest(models.Model):
    from_user = models.ForeignKey(User, related_name='request_from_user', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='request_to_user', on_delete=models.CASCADE)
    status_choices = (
        (0, 'Pending'),
        (1, 'Accepted'),
        (2, 'Rejected')
    )
    status = models.IntegerField(choices=status_choices, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.from_user} to {self.to_user}'

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'


class Friendship(models.Model):
    from_user = models.ForeignKey(User, related_name='friendship_from_user', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='friendship_to_user', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.from_user} - {self.to_user}'

    class Meta:
        verbose_name = 'Пара друзей'
        verbose_name_plural = 'Пары друзей'

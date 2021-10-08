from django.db import models
from django.contrib.auth import get_user_model




User = get_user_model()



    
class Review(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField(
    'Дата публикации', auto_now_add=True
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews'
    )
    title_id = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='Rating'
    )
    score = models.IntegerField()  

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title_id'], name='unique_follow_users'
            )
        ]
   
    
class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments'
    )
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments'
    )
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )
from django.db import models
from users.models import User
from django.contrib.auth import get_user_model
from django.conf import settings
from django.urls import reverse
User = get_user_model()

class ImageOfUsers(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='profile_pics/',null=True,blank=True)
    
    def __str__(self):
        return self.user.username
    
class AboutOfUsers(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    about = models.TextField()
    
    def __str__(self):
        return self.user.username
    
    

class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='posts/', blank=True, null=True)
    content = models.TextField() 
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_posts', blank=True)

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)]) 
    def __str__(self):
        return f"{self.user.username},{self.likes}"
    
class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)

    def __str__(self):
        return f'Comment by {self.user.username} on {self.post}'
    
class Friendship(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friends')
    friend = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'friend')
        
class Notification(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_notifications')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_notifications')
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    


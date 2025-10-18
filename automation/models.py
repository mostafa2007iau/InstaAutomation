from django.db import models
from django.contrib.auth.models import User

class InstagramAccount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=255, unique=True)
    session_data = models.TextField() # To store the session cookie

    def __str__(self):
        return self.username

class MonitoredPost(models.Model):
    account = models.ForeignKey(InstagramAccount, on_delete=models.CASCADE)
    post_id = models.CharField(max_length=255, unique=True)
    post_url = models.URLField()

    def __str__(self):
        return self.post_url

class AutomationRule(models.Model):
    REPLY_TYPE_CHOICES = [
        ('comment', 'Comment'),
        ('direct', 'Direct Message'),
    ]

    post = models.ForeignKey(MonitoredPost, on_delete=models.CASCADE)
    keywords = models.TextField(help_text="Comma-separated keywords")
    reply_text = models.TextField()
    reply_type = models.CharField(max_length=10, choices=REPLY_TYPE_CHOICES)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Rule for {self.post.post_url}"

class TaskLog(models.Model):
    rule = models.ForeignKey(AutomationRule, on_delete=models.SET_NULL, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    description = models.TextField()
    is_success = models.BooleanField(default=True)
    replied_comment_id = models.CharField(max_length=255, null=True, blank=True, help_text="The ID of the comment that was replied to.")

    def __str__(self):
        return f"Log at {self.timestamp}"
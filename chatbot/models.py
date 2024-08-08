from django.db import models

class Email(models.Model):
    email = models.EmailField(unique=True)
    thread_id = models.CharField(max_length=100)

    def __str__(self):
        return self.email

class Thread(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)

class ChatMessage(models.Model):
    thread = models.ForeignKey(Thread, related_name='messages', on_delete=models.CASCADE)
    role = models.CharField(max_length=10)  # 'user' or 'assistant'
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.role}: {self.content[:50]}..."
    
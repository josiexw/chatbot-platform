from django.db import models

class Email(models.Model):
    email = models.EmailField(unique=True)
    thread_id = models.CharField(max_length=100)

    def __str__(self):
        return self.email

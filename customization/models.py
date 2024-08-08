import shortuuid
from django.db import models

class Assistant(models.Model):
    ASSISTANT_TOOLS_CHOICES = [
        ('code_interpreter', 'Code Interpreter'),
        ('file_search', 'File Search'),
    ]

    MODEL_CHOICES = [
        # OpenAI models
        ('gpt-4o', 'gpt-4o'),
        ('gpt-4-turbo', 'gpt-4-turbo'),
        ('gpt-4-turbo-2024-04-09', 'gpt-4-turbo-2024-04-09'),
        ('gpt-4-0125-preview', 'gpt-4-0125-preview'),
        ('gpt-4-1106-preview', 'gpt-4-1106-preview'),
        ('gpt-4-0613', 'gpt-4-0613'),
        ('gpt-3.5-turbo-0125', 'gpt-3.5-turbo-0125'),
        ('gpt-3.5-turbo-1106', 'gpt-3.5-turbo-1106'),
        ('gpt-3.5-turbo-instruct', 'gpt-3.5-turbo-instruct'),
        # Groq models
        ('llama-3-sonar-small-32k-online', 'llama-3-sonar-small-32k-online'),
        ('llama-3-sonar-small-32k-chat', 'llama-3-sonar-small-32k-chat'),
        ('llama-3-sonar-large-32k-online', 'llama-3-sonar-large-32k-online'),
        ('llama-3-sonar-large-32k-chat', 'llama-3-sonar-large-32k-chat'),
        # Anthropic models
        ('claude-3-5-sonnet-20240620', 'claude-3-5-sonnet-20240620'),
        ('claude-3-opus-20240229', 'claude-3-opus-20240229'),
        ('claude-3-sonnet-20240229', 'claude-3-sonnet-20240229'),
        ('claude-3-haiku-20240307', 'claude-3-haiku-20240307')
    ]

    id = models.CharField(primary_key=True, max_length=22)
    name = models.CharField(max_length=256)
    instructions = models.TextField(max_length=2000)
    tools = models.CharField(max_length=50, choices=ASSISTANT_TOOLS_CHOICES)
    websites = models.JSONField(default=list)
    model = models.CharField(max_length=50, choices=MODEL_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Chat(models.Model):
    title = models.CharField(max_length=200)
    header_color = models.CharField(max_length=7)
    assistant_color = models.CharField(max_length=7)
    user_color = models.CharField(max_length=7)
    assistant_start_message = models.TextField(max_length=2000)
    suggested_responses = models.JSONField(default=list)
    id = models.CharField(primary_key=True, max_length=22)
    
    def __str__(self):
        return self.title
    
class File(models.Model):
    assistant = models.ForeignKey(Assistant, related_name='files', on_delete=models.CASCADE)
    file = models.FileField(upload_to='assistant_files/')
    upload_date = models.DateTimeField(auto_now_add=True)

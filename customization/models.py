from django.db import models

class Assistant(models.Model):
    ASSISTANT_TOOLS_CHOICES = [
        ('code_interpreter', 'Code Interpreter'),
        ('file_search', 'File Search'),
    ]

    OPENAI_MODEL_CHOICES = [
        ('gpt-4o', 'GPT-4o'),
        ('gpt-4-turbo', 'GPT-4 Turbo'),
        ('gpt-4-turbo-2024-04-09', 'GPT-4 Turbo with Vision'),
        ('gpt-4-0125-preview', 'GPT-4 Turbo preview 0125'),
        ('gpt-4-1106-preview', 'GPT-4 Turbo preview 1106'),
        ('gpt-4-0613', 'GPT-4 from June 13th 2023'),
        ('gpt-3.5-turbo-0125', 'GPT-3.5 Turbo'),
        ('gpt-3.5-turbo-1106', 'GPT-3.5 Turbo 1106'),
        ('gpt-3.5-turbo-instruct', 'GPT-3.5 Turbo Instruct'),
    ]

    id = models.CharField(max_length=100, primary_key=True)
    name = models.CharField(max_length=256)
    instructions = models.TextField(max_length=2000)
    tools = models.CharField(max_length=50, choices=ASSISTANT_TOOLS_CHOICES)
    vectorStore = models.CharField(max_length=100)
    model = models.CharField(max_length=50, choices=OPENAI_MODEL_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Chat(models.Model):
    title = models.CharField(max_length=200)
    header_color = models.CharField(max_length=7)
    assistant_color = models.CharField(max_length=7)
    user_color = models.CharField(max_length=7)
    assistant_start_message = models.TextField(max_length=2000)
    id = models.CharField(max_length=100, primary_key=True)
    
    def __str__(self):
        return self.title

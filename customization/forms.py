# forms.py
from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator

class MultipleURLInput(forms.TextInput):
    widget=forms.Textarea

class MultipleURLField(forms.Field):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('widget', MultipleURLInput())
        super().__init__(*args, **kwargs)

    def clean(self, value):
        value = super().clean(value)
        
        if not value:
            return []

        urls = [url.strip() for url in value.split(',') if url.strip()]
        validator = URLValidator()

        for url in urls:
            try:
                validator(url)
            except ValidationError as e:
                raise ValidationError(f"Invalid URL '{url}': {e.message}")

        return urls

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result
    
class MultipleResponseInput(forms.TextInput):
    widget=forms.Textarea

class MultipleResponseField(forms.Field):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('widget', MultipleResponseInput())
        super().__init__(*args, **kwargs)

    def clean(self, value):
        value = super().clean(value)

        if not value:
            return []

        responses = [response.strip() for response in value.split(',') if response.strip()]
        return responses

class AssistantCustomizationForm(forms.Form):
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

    assistant_name = forms.CharField(label='Assistant Name', max_length=256)
    instructions = forms.CharField(widget=forms.Textarea, label='Assistant Instructions', max_length=2000)
    tools = forms.ChoiceField(label='Tools', choices=ASSISTANT_TOOLS_CHOICES)
    model = forms.ChoiceField(label='Select an LLM', choices=MODEL_CHOICES)
    files = MultipleFileField(label='Upload knowledge files', required=False)
    website = MultipleURLField(label='Website URLs for knowledge base (separate each URL by a comma)', required=False)
    title = forms.CharField(label='Chat Title', max_length=200)
    header_color = forms.CharField(label='Header Color', max_length=7)
    assistant_color = forms.CharField(label='Assistant Color', max_length=7)
    user_color = forms.CharField(label='User Color', max_length=7)
    assistant_start_message = forms.CharField(widget=forms.Textarea, label='Assistant Start Message', max_length=2000)
    suggested_responses = MultipleResponseField(label='Suggested responses (separate each response by a comma)', required=False)

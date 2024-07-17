# forms.py
from django import forms

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

class AssistantCustomizationForm(forms.Form):
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
        ('gpt-3.5-turbo-instruct', 'GPT-3.5 Turbo instruct')
    ]

    assistant_name = forms.CharField(label='Assistant Name', max_length=256)
    instructions = forms.CharField(widget=forms.Textarea, label='Assistant Instructions', max_length=2000)
    tools = forms.ChoiceField(label='Tools', choices=ASSISTANT_TOOLS_CHOICES)
    model = forms.ChoiceField(label='OpenAI Model', choices=OPENAI_MODEL_CHOICES)
    files = MultipleFileField(label='Upload knowledge files', required=False)
    title = forms.CharField(label='Chat Title', max_length=200)
    header_color = forms.CharField(label='Header Color', max_length=7)
    assistant_color = forms.CharField(label='Assistant Color', max_length=7)
    user_color = forms.CharField(label='User Color', max_length=7)
    assistant_start_message = forms.CharField(widget=forms.Textarea, label='Assistant Start Message', max_length=2000)

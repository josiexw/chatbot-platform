import os
import time
import re
from django.http import JsonResponse, HttpResponse
from openai import OpenAI
import json
import logging
from .models import Email
from customization.models import Assistant, Chat
from django.views.decorators.csrf import csrf_exempt

logger = logging.getLogger(__name__)

api_key = os.getenv('REACT_APP_OPENAI_API_KEY')
client = OpenAI(api_key=api_key)

def extract_email(user_input):
    email_regex = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    email_match = re.search(email_regex, user_input)
    return email_match.group(0) if email_match else None

def save_contact(user_input, new_thread_id):
    email = extract_email(user_input)
    if not email:
        return

    try:
        existing_email = Email.objects.filter(email=email).first()

        if existing_email:
            global thread_id
            thread_id = existing_email.thread_id
        else:
            new_email = Email(email=email, thread_id=new_thread_id)
            new_email.save()

    except Exception as e:
        logger.error('Error saving contact to database: %s', str(e))

def remove_source(text):
    text = str(text)
    return re.sub(r'\【.*?\】', '', text).strip()

@csrf_exempt
def get_assistant(request):
    if request.method != 'POST':
        return HttpResponse(status=405, content="Method Not Allowed")

    try:
        data = json.loads(request.body)
        assistant_id = data.get('input')
        assistant = Assistant.objects.get(id=assistant_id)
        chat = Chat.objects.get(id=assistant.id)

        return JsonResponse({
            'assistant_id': assistant.id,
            'assistant_name': assistant.name,
            'title': chat.title,
            'header_color': chat.header_color,
            'assistant_color': chat.assistant_color,
            'user_color': chat.user_color,
            'assistant_start_message': chat.assistant_start_message
        })

    except Assistant.DoesNotExist:
        logger.error('Assistant not found: %s', assistant_id)
        return HttpResponse(status=404, content="Assistant not found")
    except Chat.DoesNotExist:
        logger.error('Chat not found for assistant: %s', assistant_id)
        return HttpResponse(status=404, content="Chat not found")
    except Exception as e:
        logger.error('Error fetching assistant: %s', str(e))
        return HttpResponse(status=500, content=f"An error occurred while fetching assistant: {str(e)}")


@csrf_exempt
def send_message(request):
    data = json.loads(request.body)
    user_input = data.get('input')
    assistant_id = data.get('assistant_id')
    thread_id = data.get('thread_id')

    try:
        if not thread_id:
            thread = client.beta.threads.create()
            thread_id = thread.id

        client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=user_input,
        )

        if '@' in user_input:
            save_contact(user_input, thread_id)

        run = client.beta.threads.runs.create(thread_id=thread_id, assistant_id=assistant_id)

        while True:
            response = client.beta.threads.runs.retrieve(run_id=run.id, thread_id=thread_id)
            if response.status not in ["in_progress", "queued"]:
                break
            time.sleep(2)

        message_list = client.beta.threads.messages.list(thread_id)
        last_message = next((msg for msg in message_list.data if msg.run_id == run.id and msg.role == 'assistant'), None)

        if last_message:
            return JsonResponse({'response': remove_source(last_message.content[0].text.value),
                                 'thread_id': thread_id})
        else:
            return HttpResponse(status=500, content='No response from the assistant.')

    except Exception as e:
        logger.error('Error retrieving response: %s', str(e))
        return HttpResponse(status=500, content=f"An error occurred while retrieving response: {str(e)}")

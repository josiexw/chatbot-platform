from django.shortcuts import render
import os
import time
from django.http import JsonResponse, HttpResponse
from openai import OpenAI
import logging
from .models import Assistant
from .models import Chat
from .forms import AssistantCustomizationForm
from django.views.decorators.csrf import csrf_exempt

logger = logging.getLogger(__name__)
api_key = os.getenv('REACT_APP_OPENAI_API_KEY')
client = OpenAI(api_key=api_key)

def save_assistant(assistant_name, instructions, tools, vector_store_id, model, assistant_id):
    a = Assistant(name=assistant_name,
                  instructions=instructions,
                  tools=tools,
                  vectorStore=vector_store_id,
                  model=model,
                  id=assistant_id)
    a.save()

def save_chat_customization(title, header_color, assistant_color, user_color, assistant_start_message, assistant_id):
    c = Chat(title=title,
             header_color=header_color,
             assistant_color=assistant_color,
             user_color=user_color,
             assistant_start_message=assistant_start_message,
             id=assistant_id)
    c.save()

@csrf_exempt
def make_assistant(request):
    if request.method == "POST":
        form = AssistantCustomizationForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                assistant_name = form.cleaned_data['assistant_name']
                instructions = form.cleaned_data['instructions']
                tools = form.cleaned_data['tools']
                model = form.cleaned_data['model']
                vs_name = f"{assistant_name} vector store"
                files = request.FILES.getlist('files', [])
                expiration = -1  # Set expiration as default for now
                title = form.cleaned_data['title']
                header_color = form.cleaned_data['header_color']
                assistant_color = form.cleaned_data['assistant_color']
                user_color = form.cleaned_data['user_color']
                assistant_start_message = form.cleaned_data['assistant_start_message']

                assistant = client.beta.assistants.create(
                    name=assistant_name,
                    instructions=instructions,
                    tools=[{"type": tools}],
                    model=model,
                )
                assistant_id = assistant.id

                if tools == 'file_search':
                    if expiration == -1:
                        vector_store = client.beta.vector_stores.create(
                            name=vs_name
                        )
                    else:
                        vector_store = client.beta.vector_stores.create(
                            name=vs_name,
                            expires_after={"anchor": "last_active_at", "days": expiration}
                        )
                    vector_store_id = vector_store.id

                    for file in files:
                        file_content = file.read()
                        openai_file = client.files.create(file=(f"{assistant_name} knowledge.txt", file_content), purpose="assistants")
                        client.beta.vector_stores.files.create(vector_store_id=vector_store_id, file_id=openai_file.id)
                        print('successfully added file to vector store')
                        time.sleep(1)

                    client.beta.assistants.update(
                        assistant_id,
                        tool_resources={"file_search": {"vector_store_ids": [vector_store_id]}},
                    )

                logger.debug("Assistant created: %s", assistant_id)
                save_assistant(assistant_name, instructions, tools, vector_store_id, model, assistant_id)
                save_chat_customization(title, header_color, assistant_color, user_color, assistant_start_message, assistant_id)

                return JsonResponse({
                    'assistant_name': assistant_name,
                    'assistant_id': assistant_id
                })
            except Exception as e:
                logger.error('Error creating assistant: %s', str(e))
                return HttpResponse(status=500, content=f"An error occurred while creating assistant: {str(e)}")
        else:
            return HttpResponse(status=400, content="Invalid form data")
    else:
        form = AssistantCustomizationForm()
        form_html = render(request, 'customization/customize_assistant.html', {'form': form}).content.decode('utf-8')
        return JsonResponse({'form_html': form_html})
    
@csrf_exempt
def list_assistants(request):
    try:
        assistants = Assistant.objects.all().values()
        return JsonResponse(list(assistants), safe=False)
    
    except Exception as e:
        logger.error('Error listing assistants: %s', str(e))
        return HttpResponse(status=500, content=f"An error occurred while listing assistants: {str(e)}")
    
@csrf_exempt
def delete_assistant(request):
    if request.method == "POST":
        try:
            assistant_id = request.POST.get('assistant_id')
            assistant = Assistant.objects.get(id=assistant_id)
            assistant.delete()
            client.beta.assistants.delete(assistant_id=assistant_id)
            return JsonResponse({'status': 'success'})
        except Assistant.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Assistant not found'}, status=404)
        except Exception as e:
            logger.error('Error deleting assistant: %s', str(e))
            return HttpResponse(status=500, content=f"An error occurred while deleting the assistant: {str(e)}")
    else:
        return HttpResponse(status=405)

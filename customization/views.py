from django.shortcuts import render
import uuid
from django.http import JsonResponse, HttpResponse
import logging
from .models import Assistant, Chat, File
from .forms import AssistantCustomizationForm
from django.views.decorators.csrf import csrf_exempt

logger = logging.getLogger(__name__)

@csrf_exempt
def make_assistant(request):
    """
    Creates an assistant according to form information.
    """
    if request.method == "POST":
        form = AssistantCustomizationForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                # Extract information from form
                assistant_name = form.cleaned_data['assistant_name']
                instructions = form.cleaned_data['instructions']
                tools = form.cleaned_data['tools']
                model = form.cleaned_data['model']
                files = request.FILES.getlist('files', [])
                websites = form.cleaned_data['website']
                title = form.cleaned_data['title']
                header_color = form.cleaned_data['header_color']
                assistant_color = form.cleaned_data['assistant_color']
                user_color = form.cleaned_data['user_color']
                assistant_start_message = form.cleaned_data['assistant_start_message']
                assistant_id = str(uuid.uuid4())

                # Create and save the Assistant instance
                assistant = Assistant(
                    name=assistant_name,
                    instructions=instructions,
                    tools=tools,
                    websites=websites,
                    model=model,
                    id=assistant_id
                )
                assistant.save()

                # Save each file instances associated with the assistant
                for uploaded_file in files:
                    file_instance = File(
                        assistant=assistant,
                        file=uploaded_file
                    )
                    file_instance.save()

                # Create and save the Chat instance
                chat = Chat(
                    title=title,
                    header_color=header_color,
                    assistant_color=assistant_color,
                    user_color=user_color,
                    assistant_start_message=assistant_start_message,
                    id=assistant_id
                )
                chat.save()

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
    if request.method != 'POST':
        return HttpResponse(status=405, content="Method Not Allowed")
    try:
        assistant_id = request.POST.get('assistant_id')
        assistant = Assistant.objects.get(id=assistant_id)
        assistant.delete()
        return JsonResponse({'status': 'success'})
    except Assistant.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Assistant not found'}, status=404)
    except Exception as e:
        logger.error('Error deleting assistant: %s', str(e))
        return HttpResponse(status=500, content=f"An error occurred while deleting the assistant: {str(e)}")
    
@csrf_exempt
def edit_assistant(request):
    if request.method == 'POST':
        form = AssistantCustomizationForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                # Extract information from form
                files = request.FILES.getlist('files', [])
                assistant_id = request.POST.get('assistant_id')

                # Modify the Assistant instance
                assistant = Assistant.objects.get(id=assistant_id)
                assistant.name = form.cleaned_data['assistant_name']
                assistant.instructions = form.cleaned_data['instructions']
                assistant.tools = form.cleaned_data['tools']
                assistant.model = form.cleaned_data['model']
                assistant.websites = form.cleaned_data['website']
                assistant.save()

                # Save each file instances associated with the assistant
                for uploaded_file in files:
                    file_instance = File(
                        assistant=assistant,
                        file=uploaded_file
                    )
                    file_instance.save()

                # Modify the Chat instance
                chat = Chat.objects.get(id=assistant_id)
                chat.title = form.cleaned_data['title']
                chat.header_color = form.cleaned_data['header_color']
                chat.assistant_color = form.cleaned_data['assistant_color']
                chat.user_color = form.cleaned_data['user_color']
                chat.assistant_start_message = form.cleaned_data['assistant_start_message']
                chat.suggested_responses = form.cleaned_data['suggested_responses']
                chat.save()

                return HttpResponse(status=200, content="Assistant has been saved")
            except Exception as e:
                    logger.error('Error editing assistant: %s', str(e))
                    return HttpResponse(status=500, content=f"An error occurred while editing assistant: {str(e)}")
        else:
            return HttpResponse(status=400, content="Invalid form data")
    else:
        try:
            assistant_id = request.GET.get('assistant_id')
            assistant = Assistant.objects.get(id=assistant_id)
            chat = Chat.objects.get(id=assistant_id)

            # Prefill the form with the current assistant and chat data
            initial_data = {
                'assistant_name': assistant.name,
                'instructions': assistant.instructions,
                'tools': assistant.tools,
                'model': assistant.model,
                'website': ', '.join(assistant.websites),
                'title': chat.title,
                'header_color': chat.header_color,
                'assistant_color': chat.assistant_color,
                'user_color': chat.user_color,
                'assistant_start_message': chat.assistant_start_message,
            }
            form = AssistantCustomizationForm(initial=initial_data)

            form_html = render(request, 'customization/customize_assistant.html', {'form': form, 'assistant_id': assistant_id}).content.decode('utf-8')
            return JsonResponse({'form_html': form_html})
        except Assistant.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Assistant not found'}, status=404)
        except Exception as e:
            logger.error('Error editing assistant: %s', str(e))
            return HttpResponse(status=500, content=f"An error occurred while editing the assistant: {str(e)}")

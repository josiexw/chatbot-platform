import re
import os
from django.http import JsonResponse, HttpResponse
import json
import logging
import uuid
from .models import Email, Thread, ChatMessage
from customization.models import Assistant, Chat
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from langchain_anthropic import ChatAnthropic
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.docstore.document import Document
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import CharacterTextSplitter
from django.views.decorators.csrf import csrf_exempt
from langchain import hub
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

logger = logging.getLogger(__name__)
openai_api_key = os.getenv('OPENAI_API_KEY')
thread_id = None
vector_store = None
llm = None
instructions = None

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
    text = re.sub(r'\【.*?\】', '', text)
    text = re.sub(r'\*+', '', text)
    return text.strip()

def save_message(thread_id, role, content):
    chat = Thread.objects.get(id=thread_id)
    chat_message = ChatMessage(thread_id=chat, role=role, content=content)
    chat_message.save()

def get_past_messages(thread_id):
    chat_messages = ChatMessage.objects.filter(thread_id=thread_id).order_by('timestamp')
    return "\n".join([f"{msg.role}: {msg.content}" for msg in chat_messages])

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

@csrf_exempt
def get_preview(request):
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
            'assistant_start_message': chat.assistant_start_message,
            'suggested_responses': chat.suggested_responses
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
def get_assistant(request):
    if request.method != 'POST':
        return HttpResponse(status=405, content="Method Not Allowed")

    try:
        global vector_store, llm, instructions
        data = json.loads(request.body)
        assistant_id = data.get('input')
        assistant = Assistant.objects.get(id=assistant_id)
        instructions = assistant.instructions
        urls = assistant.websites

        if assistant.tools == 'file_search':
            docs = []

            # Load website if url exists
            if urls:
                print(urls)
                loader = WebBaseLoader(urls)
                websites = loader.load()
                docs.extend(websites)

            # Process and store files for retrieval using Chroma vector database
            text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
            for file_instance in assistant.files.all():
                docs.append(Document(page_content=file_instance.file.read().decode('utf-8'), metadata={"source": "local"}))

            splits = text_splitter.split_documents(docs)
            embeddings = OpenAIEmbeddings(api_key=openai_api_key)
            vector_store = Chroma.from_documents(documents=splits, embedding=embeddings)
        else:
            vector_store = None

        # Create LLM based on model
        if 'gpt' in assistant.model:
            llm = ChatOpenAI(model=assistant.model)
        elif 'llama' in assistant.model:
            llm = ChatGroq(model=assistant.model)
        else:
            llm = ChatAnthropic(model=assistant.model)

        return HttpResponse(status=200, content="Assistant is ready!")

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
    global thread_id, vector_store, llm, instructions
    data = json.loads(request.body)
    user_input = data.get('input')
    thread = data.get('thread_id')

    try:
        if not thread:
            thread_id = str(uuid.uuid4())
            t = Thread(thread_id)
            t.save()

        if '@' in user_input:
            save_contact(user_input, thread_id)

        past_messages = get_past_messages(thread_id)
        system_prompt = (instructions + "\n\n" + past_messages + "{context}")
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                ("human", "{input}"),
            ]
        )

        question_answer_chain = create_stuff_documents_chain(llm, prompt)
        retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 6})
        rag_chain = create_retrieval_chain(retriever, question_answer_chain)

        # Get response from the LLM
        response = rag_chain.invoke({"input": user_input})

        # Save user message
        save_message(thread_id, 'user', user_input)
        # Save assistant response
        save_message(thread_id, 'assistant', response["answer"])

        return JsonResponse({'response': response["answer"], 'thread_id': thread_id})

    except Thread.DoesNotExist:
        logger.error('Thread not found: %s', thread_id)
        return HttpResponse(status=404, content="Thread not found")
    except Exception as e:
        logger.error('Error retrieving response: %s', str(e))
        return HttpResponse(status=500, content=f"An error occurred while retrieving response: {str(e)}")

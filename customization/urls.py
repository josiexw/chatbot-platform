"""
URL configuration for chatbot_server project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from customization.views import make_assistant, list_assistants, delete_assistant, edit_assistant

urlpatterns = [
    path('api/make_assistant', make_assistant, name='make_assistant'),
    path('api/list_assistants', list_assistants, name='list_assistants'),
    path('api/delete_assistant', delete_assistant, name='delete_assistant'),
    path('api/edit_assistant', edit_assistant, name='edit_assistant'),
]

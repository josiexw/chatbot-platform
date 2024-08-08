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
from chatbot.views import get_preview, get_assistant, send_message

urlpatterns = [
    path('api/get_preview', get_preview, name='get_preview'),
    path('api/get_assistant', get_assistant, name='get_assistant'),
    path('api/send_message', send_message, name='send_message'),
]

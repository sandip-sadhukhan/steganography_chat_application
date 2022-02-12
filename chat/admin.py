from django.contrib import admin
from .models import ChatMessage


class ChatMessageAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "message",
        "sender",
        "receiver",
        "fileURL",
    )
    list_display_links = (
        "id",
        "message",
    )


admin.site.register(ChatMessage, ChatMessageAdmin)

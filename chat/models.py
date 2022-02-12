from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User


class ChatMessage(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sender")
    receiver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="receiver"
    )
    message = models.CharField(max_length=1000, null=True, blank=True)
    fileURL = models.URLField(max_length=500, null=True, blank=True)
    is_read = models.BooleanField(default=False)

    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("timestamp",)

    def __str__(self):
        return self.message

    def serialize(self):
        return {
            "sender": self.sender.id,
            "receiver": self.receiver.id,
            "message": self.message,
            "fileURL": self.fileURL,
            "timestamp": self.timestamp.isoformat(),
        }

    @classmethod
    def get_messages(cls, user1, user2):
        messages = ChatMessage.objects.filter(Q(sender=user1) | Q(sender=user2)).filter(
            Q(receiver=user1) | Q(receiver=user2)
        )

        return [message.serialize() for message in messages]


class ImageStore(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="uploads/%Y/%m/%d/")

    def get_image_url(self):
        return self.image.name

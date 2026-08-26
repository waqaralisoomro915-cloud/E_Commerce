from rest_framework import serializers
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'
        read_only_fields = ('user','created_at',)


    def validate_title(self,title):
        title= title.strip()
        if not title:
            raise serializers.ValidationError({'title':"This field is required."})
        return title
    def validate_message(self, message):
        message= message.strip()
        if not message:
            raise serializers.ValidationError({'message':"This field is required."})
        return message


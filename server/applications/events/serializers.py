from rest_framework import serializers
from datetime import datetime

from applications.events.models import Events, Image
from applications.feedback.serializers import CommentSerializer


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'


class EventsSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')
    comments = CommentSerializer(many=True, read_only=True)
    images = ImageSerializer(many=True, read_only=True)  
    video = serializers.FileField(required=False)  

    class Meta:
        model = Events
        fields = '__all__'

    def validate(self, attrs):
        event_date = attrs.get('date')
        today = datetime.now().date()

        if event_date and today > event_date:
            raise serializers.ValidationError('Введите дату в будущем времени')
        return attrs

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['likes'] = instance.likes.filter(like=True).count()
        return rep

    def create(self, validated_data):
        request = self.context.get('request')
        files_data = request.FILES  
        video = files_data.get('video', None)        
        event = Events.objects.create(**validated_data, video=video)

        for image in files_data.getlist('images'):
            Image.objects.create(event=event, image=image)

        return event 
from rest_framework import serializers

from .models import Walk


class WalkSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Walk
        fields = ('distance', 'time', 'date',)

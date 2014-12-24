from rest_framework import serializers

from .models import Walk


class WalkSerializer(serializers.HyperlinkedModelSerializer):
    date = serializers.DateTimeField(
        format='%Y-%m-%d',
        input_formats=[
            '%Y-%m-%d',
        ]
    )

    class Meta:
        model = Walk
        fields = ('distance', 'time', 'date', 'pk')
